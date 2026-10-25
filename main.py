"""OpenAI-compatible HTTP adapter for Edge Read Aloud."""
import asyncio
import hmac
import json
import logging
import math
import os
import re
from pathlib import Path
import fastapi
import uvicorn
from fastapi import Depends, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer
from config import DEFAULT_CONFIGS
from handle_text import preparar_texto_para_tts
from tts_handler import DADOS_MODELOS, MAPEAMENTO_VOZES, gerar_audio
from utils import CHAVE_API, EXIGIR_CHAVE_API, TIPOS_MIME_AUDIO, obter_env_bool

app = fastapi.FastAPI(title='Multivozes BR Engine', version='2.1.0')
logger = logging.getLogger('multivozes')
PORTA = int(os.getenv('PORT', DEFAULT_CONFIGS['PORT']))
# Padrão seguro: só o próprio computador acessa. Docker define HOST=0.0.0.0.
HOST = os.getenv('HOST', '127.0.0.1')
VOZ_PADRAO = os.getenv('DEFAULT_VOICE', DEFAULT_CONFIGS['DEFAULT_VOICE'])
FORMATO_RESPOSTA_PADRAO = os.getenv('DEFAULT_RESPONSE_FORMAT', 'mp3')
VELOCIDADE_PADRAO = float(os.getenv('DEFAULT_SPEED', '1.0'))
REMOVER_FILTRO = obter_env_bool('REMOVE_FILTER', False)
MAX_INPUT_CHARS = int(os.getenv('MAX_INPUT_CHARS', '10000'))
MAX_REQUEST_BYTES = int(os.getenv('MAX_REQUEST_BYTES', '131072'))
TTS_TIMEOUT_SECONDS = float(os.getenv('TTS_TIMEOUT_SECONDS', '90'))
MAX_CONCURRENT_TTS = int(os.getenv('MAX_CONCURRENT_TTS', '4'))
if not math.isfinite(TTS_TIMEOUT_SECONDS) or min(MAX_INPUT_CHARS, MAX_REQUEST_BYTES, TTS_TIMEOUT_SECONDS, MAX_CONCURRENT_TTS) <= 0:
    raise ValueError('Os limites e timeout de TTS devem ser positivos.')
_synthesis_slots = asyncio.Semaphore(MAX_CONCURRENT_TTS)
_bearer_auth = HTTPBearer(
    auto_error=False, scheme_name='BearerAuth',
    description='Informe API_KEY. Obrigatória quando REQUIRE_API_KEY=true no servidor.',
)


class TemporaryAudioResponse(FileResponse):
    """Always remove generated audio, even when sending fails or is cancelled."""
    async def __call__(self, scope, receive, send):
        try:
            await super().__call__(scope, receive, send)
        finally:
            try:
                Path(self.path).unlink(missing_ok=True)
            except OSError as error:
                logger.warning('Falha na limpeza de audio (%s)', type(error).__name__)


async def verificar_chave_api(request: Request, _credentials=Depends(_bearer_auth)):
    if not EXIGIR_CHAVE_API:
        return
    if not CHAVE_API:
        raise HTTPException(503, 'Defina API_KEY no servidor antes de usar a API.')
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer ') or not hmac.compare_digest(auth[7:].encode('utf-8'), CHAVE_API.encode('utf-8')):
        raise HTTPException(401, 'Chave de API ausente ou inválida.')

async def _read_payload(request):
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > MAX_REQUEST_BYTES:
            raise HTTPException(413, 'Requisição excede o tamanho permitido.')
    try:
        data = json.loads(body)
    except (ValueError, UnicodeDecodeError, RecursionError):
        raise HTTPException(400, 'JSON inválido.')
    if not isinstance(data, dict):
        raise HTTPException(400, 'O corpo JSON deve ser um objeto.')
    return data

@app.post(
    '/v1/audio/speech', dependencies=[Depends(verificar_chave_api)],
    response_class=TemporaryAudioResponse,
    responses={200: {'description': 'Arquivo de áudio sintetizado.', 'content': {
        mime: {'schema': {'type': 'string', 'format': 'binary'}}
        for mime in TIPOS_MIME_AUDIO.values()
    }}},
    openapi_extra={'requestBody': {'required': True, 'content': {'application/json': {
        'schema': {
            'type': 'object', 'required': ['input'],
            'properties': {
                'input': {'type': 'string', 'minLength': 1, 'maxLength': MAX_INPUT_CHARS},
                'model': {'type': 'string', 'default': 'tts-1',
                          'description': 'Campo ignorado para compatibilidade. Qualquer nome usa o mesmo motor Edge.'},
                'voice': {'type': 'string', 'default': VOZ_PADRAO,
                          'description': 'Apelido de voices.json ou ShortName do catálogo Edge.'},
                'response_format': {'type': 'string', 'enum': list(TIPOS_MIME_AUDIO), 'default': FORMATO_RESPOSTA_PADRAO},
                'speed': {'type': 'number', 'minimum': 0.25, 'maximum': 2.0, 'default': VELOCIDADE_PADRAO},
            },
        },
        'example': {'input': 'Olá! Esta é a voz brasileira. Hello, this is a multilingual voice.',
                    'model': 'tts-1', 'voice': VOZ_PADRAO,
                    'response_format': 'mp3', 'speed': 1.0},
    }}}},
)
async def text_to_speech(request: Request):
    data = await _read_payload(request)
    text = data.get('input')
    if not isinstance(text, str) or not text.strip():
        raise HTTPException(400, "O campo 'input' deve conter texto.")
    if len(text) > MAX_INPUT_CHARS:
        raise HTTPException(413, f'O texto excede {MAX_INPUT_CHARS} caracteres.')
    if not REMOVER_FILTRO:
        text = preparar_texto_para_tts(text)
    if not text.strip():
        raise HTTPException(400, 'O texto ficou vazio após remover a formatação.')
    voice = data.get('voice', VOZ_PADRAO)
    if not isinstance(voice, str) or len(voice) > 150 or (voice not in MAPEAMENTO_VOZES and not re.fullmatch(r'[a-z]{2,3}(?:-[A-Za-z0-9]+)+Neural', voice)):
        raise HTTPException(400, 'Voz inválida. Use um apelido ou nome do catálogo Edge.')
    format_name = data.get('response_format', FORMATO_RESPOSTA_PADRAO)
    if not isinstance(format_name, str) or format_name.lower() not in TIPOS_MIME_AUDIO:
        raise HTTPException(400, 'Formato de áudio não suportado.')
    format_name = format_name.lower()
    speed = data.get('speed', VELOCIDADE_PADRAO)
    try:
        if isinstance(speed, bool):
            raise ValueError
        speed = float(speed)
        if not math.isfinite(speed) or not 0.25 <= speed <= 2.0:
            raise ValueError
    except (ValueError, TypeError, OverflowError):
        raise HTTPException(400, 'A velocidade deve estar entre 0.25 e 2.0.')
    if _synthesis_slots.locked():
        raise HTTPException(503, 'Servidor ocupado. Tente novamente em instantes.', headers={'Retry-After': '5'})
    async with _synthesis_slots:
        try:
            path = await asyncio.wait_for(gerar_audio(text, voice, format_name, speed), TTS_TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            raise HTTPException(504, 'O provedor de voz excedeu o tempo limite.')
        except Exception as error:
            logger.warning('Falha na síntese de áudio (%s)', type(error).__name__)
            raise HTTPException(502, 'Falha no provedor de voz ou na conversão. Confira a versão do edge-tts, a voz e o FFmpeg.')
    return TemporaryAudioResponse(path, media_type=TIPOS_MIME_AUDIO[format_name], filename=f'speech.{format_name}')

@app.get('/health')
def health():
    """Process liveness only: external synthesis and credentials are not tested."""
    return {'status': 'ok'}

@app.get('/v1/models')
def listar_modelos():
    return {'data': [{'id': m['id'], 'object': 'model'} for m in DADOS_MODELOS]}

@app.get('/voices', dependencies=[Depends(verificar_chave_api)], include_in_schema=False)
@app.get('/v1/voices', dependencies=[Depends(verificar_chave_api)], include_in_schema=False)
@app.get('/v1/audio/voices', dependencies=[Depends(verificar_chave_api)])
async def listar_vozes(locale: str | None = None, multilingual: bool = False):
    from voices_catalog import get_voices
    try:
        return {'data': await get_voices(locale=locale, multilingual=multilingual)}
    except asyncio.TimeoutError:
        raise HTTPException(504, 'Consulta de vozes excedeu o tempo limite.')
    except Exception as error:
        logger.warning('Falha na consulta de vozes (%s)', type(error).__name__)
        raise HTTPException(502, 'Não foi possível consultar o catálogo de vozes.')

if __name__ == '__main__':
    print('Multivozes BR Engine - Samuel de Sousa Santos (samucatutoriais)')
    print('Baseado em travisvn/openai-edge-tts; sintese por rany2/edge-tts')
    uvicorn.run(app, host=HOST, port=PORTA)
