import re
import emoji

def preparar_texto_para_tts(texto: str) -> str:
    """
    Prepara o texto para a API de TTS, limpando Markdown, emojis e
    outros caracteres que o motor de voz não deve pronunciar.

    Args:
        texto (str): O texto bruto contendo Markdown, emojis, etc.

    Returns:
        str: O texto limpo e otimizado para a síntese de voz.
    """
    # Garante que a entrada é uma string, evitando erros
    if not isinstance(texto, str):
        return ""

    # Remove emojis
    # Usando a biblioteca 'emoji' para um tratamento mais robusto de diferentes versões
    texto = emoji.replace_emoji(texto, replace='')

    # Expressões regulares para remover formatação Markdown
    # Remove links de Markdown, mantendo o texto âncora: [clique aqui](http://site.com) -> clique aqui
    texto = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', texto)
    # Remove imagens de Markdown, mantendo o texto alternativo (alt text): ![descrição da imagem](imagem.png) -> descrição da imagem
    texto = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', texto)
    # Remove símbolos de formatação (negrito, itálico, etc.), mantendo o conteúdo
    texto = re.sub(r'(\*\*|__|\*|_|~~)', '', texto)
    # Remove blocos de código (multi-linha)
    texto = re.sub(r'```[\s\S]+?```', '', texto)
    # Remove código inline (single-line)
    texto = re.sub(r'`([^`]+)`', r'\1', texto)
    # Remove cabeçalhos de Markdown, mantendo apenas o texto: ### Título -> Título
    texto = re.sub(r'^\s*#{1,6}\s+', '', texto, flags=re.MULTILINE)
    # Remove tags HTML
    texto = re.sub(r'</?[^>]+(>|$)', '', texto)

    # Limpeza final
    # Normaliza quebras de linha para garantir parágrafos consistentes
    texto = re.sub(r'\n{2,}', '\n\n', texto)
    # Substitui espaços múltiplos por um único espaço
    texto = re.sub(r' {2,}', ' ', texto)
    # Remove espaços em branco no início e no fim do texto
    texto = texto.strip()

    return texto

