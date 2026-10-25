DEFAULT_CONFIGS = {
    # --- Configurações do Servidor ---
    "PORT": 5050,
    "API_KEY": None,

    # --- Configurações de TTS ---
    "DEFAULT_VOICE": "pt-BR-ThalitaMultilingualNeural",
    "DEFAULT_RESPONSE_FORMAT": "mp3",
    "DEFAULT_SPEED": 1.0,
    "DEFAULT_LANGUAGE": "pt-BR",

    # --- Funcionalidades (Flags) ---
    "REQUIRE_API_KEY": True,
    "REMOVE_FILTER": False,
    "DETAILED_ERROR_LOGGING": True,
}

# Recuperação quando voices.json estiver ausente. Os aliases OpenAI usam somente
# vozes multilíngues; nomes técnicos continuam disponíveis para outros usos.
DEFAULT_OPENAI_VOICES = {
    "alloy": "pt-BR-ThalitaMultilingualNeural",
    "ash": "en-US-AndrewMultilingualNeural",
    "ballad": "en-US-BrianMultilingualNeural",
    "cedar": "en-AU-WilliamMultilingualNeural",
    "coral": "en-US-AvaMultilingualNeural",
    "echo": "it-IT-GiuseppeMultilingualNeural",
    "fable": "it-IT-GiuseppeMultilingualNeural",
    "marin": "en-US-EmmaMultilingualNeural",
    "onyx": "fr-FR-RemyMultilingualNeural",
    "nova": "de-DE-SeraphinaMultilingualNeural",
    "sage": "fr-FR-VivienneMultilingualNeural",
    "shimmer": "en-US-EmmaMultilingualNeural",
    "verse": "ko-KR-HyunsuMultilingualNeural",
}


