import os
from dotenv import load_dotenv
from config import DEFAULT_CONFIGS

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

def obter_env_bool(nome_variavel: str, valor_padrao: bool = False) -> bool:
    """Lê uma variável de ambiente e a converte para um valor booleano."""
    valor = os.getenv(nome_variavel, str(valor_padrao))
    return valor.lower() in ("yes", "y", "true", "1", "t")

# --- Carrega as configurações a partir das variáveis de ambiente ou dos padrões ---
CHAVE_API = os.getenv('API_KEY', DEFAULT_CONFIGS.get("API_KEY"))
EXIGIR_CHAVE_API = obter_env_bool('REQUIRE_API_KEY', DEFAULT_CONFIGS.get("REQUIRE_API_KEY"))
LOG_ERROS_DETALHADO = obter_env_bool('DETAILED_ERROR_LOGGING', DEFAULT_CONFIGS.get("DETAILED_ERROR_LOGGING"))

# Dicionário com os tipos MIME para cada formato de áudio suportado.
TIPOS_MIME_AUDIO = {
    "mp3": "audio/mpeg",
    "opus": "audio/opus",
    "aac": "audio/aac",
    "flac": "audio/flac",
    "wav": "audio/wav",
    "pcm": "audio/L16"
}

