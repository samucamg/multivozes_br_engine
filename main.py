import fastapi
from fastapi import Request, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import traceback
import uvicorn

from config import DEFAULT_CONFIGS
from handle_text import preparar_texto_para_tts
from tts_handler import gerar_audio, DADOS_MODELOS
from utils import (obter_env_bool, TIPOS_MIME_AUDIO, 
                   LOG_ERROS_DETALHADO, EXIGIR_CHAVE_API, CHAVE_API)

# Inicializa a aplicação FastAPI e carrega as variáveis de ambiente.
app = fastapi.FastAPI()
load_dotenv()

# --- Carregamento de Configurações ---
PORTA = int(os.getenv('PORT', DEFAULT_CONFIGS.get("PORT")))
VOZ_PADRAO = os.getenv('DEFAULT_VOICE', DEFAULT_CONFIGS.get("DEFAULT_VOICE"))
FORMATO_RESPOSTA_PADRAO = os.getenv('DEFAULT_RESPONSE_FORMAT', DEFAULT_CONFIGS.get("DEFAULT_RESPONSE_FORMAT"))
VELOCIDADE_PADRAO = float(os.getenv('DEFAULT_SPEED', DEFAULT_CONFIGS.get("DEFAULT_SPEED")))
REMOVER_FILTRO = obter_env_bool('REMOVE_FILTER', DEFAULT_CONFIGS.get("REMOVE_FILTER"))


# --- Função de Segurança (Dependência) ---
async def verificar_chave_api(request: Request):
    """
    Verifica se a chave de API fornecida no cabeçalho 'Authorization' é válida.
    Esta função é usada como uma dependência nas rotas protegidas.
    """
    if not EXIGIR_CHAVE_API:
        return
    if not CHAVE_API:
        raise HTTPException(status_code=500, detail="Servidor não configurado para autenticação. A variável API_KEY não foi definida.")
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Chave de API ausente ou em formato inválido. Use o cabeçalho 'Authorization: Bearer SUA_CHAVE'.")
    
    token_fornecido = auth_header.split('Bearer ')[1]
    if token_fornecido != CHAVE_API:
        raise HTTPException(status_code=401, detail="Chave de API inválida.")


# --- Rota Principal de Geração de Áudio ---
@app.post("/v1/audio/speech", dependencies=[Depends(verificar_chave_api)])
async def text_to_speech(request: Request, background_tasks: BackgroundTasks):
    """
    Endpoint principal que recebe texto e retorna o áudio sintetizado.
    Compatível com a API da OpenAI.
    """
    try:
        dados = await request.json()
        texto = dados.get('input')
        if not texto:
            raise HTTPException(status_code=400, detail="O campo 'input' é obrigatório.")

        # Aplica o filtro de texto se não estiver desativado
        if not REMOVER_FILTRO:
            texto = preparar_texto_para_tts(texto)

        # Obtém os parâmetros da requisição ou usa os padrões
        voz = dados.get('voice', VOZ_PADRAO)
        formato_resposta = dados.get('response_format', FORMATO_RESPOSTA_PADRAO)
        velocidade = float(dados.get('speed', VELOCIDADE_PADRAO))
        tipo_mime = TIPOS_MIME_AUDIO.get(formato_resposta, "audio/mpeg")

        # Gera o áudio de forma assíncrona
        caminho_ficheiro_audio = await gerar_audio(texto, voz, formato_resposta, velocidade)
        
        # Agenda a exclusão do ficheiro temporário após o envio da resposta
        background_tasks.add_task(os.unlink, caminho_ficheiro_audio)
        
        return FileResponse(path=caminho_ficheiro_audio, media_type=tipo_mime, filename=f"speech.{formato_resposta}")

    except Exception as e:
        if LOG_ERROS_DETALHADO:
            print(f"Erro inesperado: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {e}")


# --- Rota para Listar Modelos ---
@app.get("/v1/models")
def listar_modelos():
    """
    Endpoint para listar os modelos de TTS disponíveis (para compatibilidade com OpenAI).
    """
    return {"data": [{"id": m["id"], "object": "model"} for m in DADOS_MODELOS]}


# --- Bloco de Inicialização do Servidor ---
if __name__ == '__main__':
    print("=====================================================================")
    print("      🔊 Iniciando o Multivozes BR Engine 🇧🇷 (Modo Estável)")
    print("=====================================================================")
    print(f"🐍 Criado por: Samuel de Sousa Santos (samucatutoriais)")
    print(f"🔧 Baseado no projeto de: travisvn/openai-edge-tts")
    print(f"⚙️  Servidor: Uvicorn (FastAPI)")
    print(f"🌐 Servidor a correr em: http://0.0.0.0:{PORTA}")
    print(f"🔑 Exigir chave de API: {'Sim' if EXIGIR_CHAVE_API else 'Não'}")
    print("=====================================================================")
    
    uvicorn.run(app, host='0.0.0.0', port=PORTA)

