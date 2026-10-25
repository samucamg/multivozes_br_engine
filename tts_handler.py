"""Edge synthesis with cancellable, explicitly encoded FFmpeg conversions."""
import asyncio
import json
import os
import shutil
import tempfile
from pathlib import Path
import edge_tts
from dotenv import load_dotenv
from config import DEFAULT_OPENAI_VOICES

load_dotenv()
PROXY = os.getenv('PROXY') or None

def carregar_mapeamento_vozes():
    path = Path(__file__).with_name('voices.json')
    if not path.exists():
        return dict(DEFAULT_OPENAI_VOICES)
    with path.open(encoding='utf-8') as stream:
        mapping = json.load(stream)
    if not isinstance(mapping, dict) or not all(
        isinstance(alias, str) and alias and isinstance(voice, str) and voice
        for alias, voice in mapping.items()
    ):
        raise ValueError('voices.json deve mapear nomes para vozes em texto.')
    for alias, voice in mapping.items():
        if alias in DEFAULT_OPENAI_VOICES and not voice.endswith('MultilingualNeural'):
            raise ValueError(f'O alias OpenAI {alias!r} deve usar uma voz MultilingualNeural.')
    return mapping

MAPEAMENTO_VOZES = carregar_mapeamento_vozes()
DADOS_MODELOS = [{'id': 'tts-1', 'name': 'Text-to-speech v1'}, {'id': 'tts-1-hd', 'name': 'Text-to-speech v1 HD'}]
CONVERSION_ARGS = {
    'opus': ['-c:a', 'libopus', '-f', 'ogg'],
    'aac': ['-c:a', 'aac', '-f', 'adts'],
    'flac': ['-c:a', 'flac', '-f', 'flac'],
    'wav': ['-c:a', 'pcm_s16le', '-f', 'wav'],
    'pcm': ['-c:a', 'pcm_s16le', '-ar', '24000', '-ac', '1', '-f', 's16le'],
}

def velocidade_para_taxa(velocidade: float) -> str:
    if not 0.25 <= velocidade <= 2.0:
        raise ValueError('A velocidade deve estar entre 0.25 e 2.0.')
    return f'{round((velocidade - 1) * 100):+d}%'

def _temporary_path(suffix):
    descriptor, path = tempfile.mkstemp(suffix=suffix)
    os.close(descriptor)
    return path

async def _convert(source, destination, format_name):
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        raise RuntimeError('FFmpeg não está instalado para converter áudio.')
    process = await asyncio.create_subprocess_exec(
        ffmpeg, '-nostdin', '-hide_banner', '-loglevel', 'error', '-y',
        '-i', source, '-vn', *CONVERSION_ARGS[format_name], destination,
        stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL,
    )
    try:
        if await process.wait() != 0:
            raise RuntimeError('FFmpeg não conseguiu converter o áudio.')
    except BaseException:
        if process.returncode is None:
            process.kill()
            await process.wait()
        raise

async def gerar_audio(texto: str, voz: str, formato_resposta: str, velocidade: float) -> str:
    formato_resposta = formato_resposta.lower()
    if formato_resposta not in {'mp3', *CONVERSION_ARGS}:
        raise ValueError('Formato de áudio não suportado.')
    taxa = velocidade_para_taxa(velocidade)
    source = _temporary_path('.mp3')
    destination = source
    try:
        communicator = edge_tts.Communicate(texto, MAPEAMENTO_VOZES.get(voz, voz), rate=taxa, proxy=PROXY)
        await communicator.save(source)
        if not Path(source).stat().st_size:
            raise RuntimeError('O provedor retornou áudio vazio.')
        if formato_resposta != 'mp3':
            destination = _temporary_path(f'.{formato_resposta}')
            await _convert(source, destination, formato_resposta)
            Path(source).unlink(missing_ok=True)
        return destination
    except BaseException:
        # Cancellation from request timeout must also remove partial output.
        Path(source).unlink(missing_ok=True)
        Path(destination).unlink(missing_ok=True)
        raise
