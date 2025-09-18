# -*- coding: utf-8 -*-

"""
Criado por: Samuel de Sousa Santos (youtube.com/c/samucatutoriais)
Baseado no projeto de: travisvn/openai-edge-tts

Este ficheiro centraliza todas as configurações padrão do servidor.
Estes valores são usados como "plano B" se não forem definidos no ficheiro .env.
"""

DEFAULT_CONFIGS = {
    # --- Configurações do Servidor ---
    "PORT": 5050,
    "API_KEY": None,

    # --- Configurações de TTS ---
    "DEFAULT_VOICE": "pt-BR-FranciscaNeural",
    "DEFAULT_RESPONSE_FORMAT": "mp3",
    "DEFAULT_SPEED": 1.0,
    "DEFAULT_LANGUAGE": "pt-BR",

    # --- Funcionalidades (Flags) ---
    "REQUIRE_API_KEY": True,
    "REMOVE_FILTER": False,
    "DETAILED_ERROR_LOGGING": True,
}
