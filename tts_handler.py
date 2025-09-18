import edge_tts
import os
import traceback
from dotenv import load_dotenv
import tempfile
from pathlib import Path

from config import DEFAULT_CONFIGS
from utils import LOG_ERROS_DETALHADO

load_dotenv()

# --- Carregamento de Configurações ---
PROXY = os.getenv("PROXY", None)

# --- Mapeamento e Dados de Vozes ---
# Mapeamento de vozes padrão da OpenAI para as vozes do Edge-TTS
MAPEAMENTO_VOZES = {
    'alloy': 'pt-BR-FranciscaNeural',
    'echo': 'pt-BR-AntonioNeural',
    'fable': 'en-US-RogerNeural',
    'onyx': 'en-US-EricNeural',
    'nova': 'en-US-AvaNeural',
    'shimmer': 'en-US-EmmaNeural',
}

# Dados dos modelos para compatibilidade com a API OpenAI
DADOS_MODELOS = [
    {"id": "tts-1", "name": "Text-to-speech v1"},
    {"id": "tts-1-hd", "name": "Text-to-speech v1 HD"},
]

def velocidade_para_taxa(velocidade: float) -> str:
    """Converte um multiplicador de velocidade (ex: 1.5) para o formato de taxa do edge-tts (ex: '+50%')."""
    if not 0.25 <= velocidade <= 2.0:
        raise ValueError("A velocidade deve estar entre 0.25 e 2.0.")
    percentagem = int((velocidade - 1) * 100)
    return f"+{percentagem}%" if percentagem >= 0 else f"{percentagem}%"

async def gerar_audio(texto: str, voz: str, formato_resposta: str, velocidade: float) -> str:
    """
    Gera o áudio usando edge-tts, salva num ficheiro temporário e retorna o caminho para o ficheiro.
    A conversão para outros formatos (além de mp3) não é feita aqui, pois o edge-tts
    só suporta a saída direta para mp3. A API principal lida com a entrega do ficheiro.
    """
    # Verifica se a voz solicitada é um apelido da OpenAI (alloy, etc.) e a converte
    voz_edge_tts = MAPEAMENTO_VOZES.get(voz, voz)
    taxa = velocidade_para_taxa(velocidade)
    
    # Cria um ficheiro temporário para salvar o áudio
    ficheiro_temp = tempfile.NamedTemporaryFile(delete=False, suffix=f".{formato_resposta}")
    caminho_temp_audio = ficheiro_temp.name
    ficheiro_temp.close()

    try:
        # Inicializa o comunicador do edge-tts com o texto e as configurações
        comunicador = edge_tts.Communicate(texto, voz_edge_tts, rate=taxa, proxy=PROXY)
        # Salva o áudio de forma assíncrona no ficheiro temporário
        await comunicador.save(caminho_temp_audio)
    except Exception as e:
        # Se ocorrer um erro, remove o ficheiro temporário para não deixar lixo
        Path(caminho_temp_audio).unlink(missing_ok=True)
        if LOG_ERROS_DETALHADO:
            print(f"Erro detalhado em gerar_audio: {traceback.format_exc()}")
        # Lança uma exceção para ser capturada pela rota da API
        raise RuntimeError(f"Falha na comunicação com o serviço Edge-TTS: {e}")

    # Retorna o caminho do ficheiro de áudio gerado com sucesso
    return caminho_temp_audio

