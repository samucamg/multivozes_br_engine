# Multivozes BR Engine 🇧🇷

<p align="center">
  <a href="https://multivozes.com/" target="_blank">
    <img src="https://multivozes.com/assets/images/Logo_Multivozes.png" alt="Logo Painel Multivozes" width="150"/>
  </a>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=L4nuFUAW-Is" target="_blank">
    <img src="https://img.youtube.com/vi/L4nuFUAW-Is/maxresdefault.jpg" alt="Vídeo de apresentação / Presentation video" width="600"/>
  </a>
  <br/>
  <a href="https://www.youtube.com/watch?v=L4nuFUAW-Is">Assista ao vídeo / Watch the video</a>
</p>

<p align="center">
  <a href="https://www.youtube.com/c/samucatutoriais" target="_blank">
    <img src="https://multivozes.com/assets/images/banner-youtube.png" alt="Canal Samuca Tutoriais" width="150"/>
  </a>
</p>

<p align="center"><b><a href="#-português">🇧🇷 Português</a> · <a href="#-english">🇺🇸 English</a></b></p>

---

# 🇧🇷 Português

Transforma texto em voz (MP3, WAV, Opus...) no **seu próprio computador ou servidor**, com a mesma "porta de entrada" da OpenAI (`/v1/audio/speech`). Funciona com **n8n**, com o [Painel MultiVozes](https://multivozes.com/) e com qualquer programa que fale com a API de voz da OpenAI. Feito por **Samuel de Sousa Santos**, baseado em [travisvn/openai-edge-tts](https://github.com/travisvn/openai-edge-tts). A voz vem do serviço gratuito do Microsoft Edge através da biblioteca [edge-tts](https://github.com/rany2/edge-tts); não precisa de conta OpenAI nem de cartão.

> ⚠️ O serviço do Edge é externo e a Microsoft pode mudar as regras (já aconteceu: erro **403**). Se parar de funcionar, veja [Problemas comuns](#problemas-comuns).

## Instalação em 4 passos (recomendado: Docker)

**1. Instale o Docker.** Windows/macOS: [Docker Desktop](https://www.docker.com/products/docker-desktop/). Linux: Docker Engine com Compose.

**2. Baixe o projeto.** Com Git: `git clone https://github.com/samucamg/multivozes_br_engine.git`. Sem Git: botão verde **Code → Download ZIP** no GitHub e extraia a pasta.

**3. Crie sua senha (chave de API).** Abra um terminal **dentro da pasta** do projeto.

| Sistema | Comando |
| --- | --- |
| Windows (PowerShell) | `Copy-Item .env.example .env` |
| Linux / macOS | `cp .env.example .env` |

Abra o arquivo `.env` no Bloco de Notas e escreva uma senha longa depois de `API_KEY=`, por exemplo `API_KEY=minha-senha-bem-grande-9482`. Você usará essa senha nos pedidos. *(Se você tem Python, `python scripts/setup.py --configure-only` faz isso sozinho e gera uma senha aleatória.)*

**4. Ligue o serviço.**

```sh
docker compose up -d --build
```

A primeira vez demora alguns minutos. Pronto: o serviço está em `http://localhost:5050`. Para desligar: `docker compose down`. Para ver mensagens: `docker compose logs -f --tail=100`.

## Instalação sem Docker (Windows, Linux, macOS)

Precisa de **Python 3.10 a 3.13** (recomendado 3.12) e, para formatos diferentes de MP3, do **FFmpeg** (Windows: `winget install Gyan.FFmpeg`; Ubuntu/Debian: `sudo apt install ffmpeg`; macOS: `brew install ffmpeg`).

```sh
git clone https://github.com/samucamg/multivozes_br_engine.git
cd multivozes_br_engine
python scripts/setup.py
```

(No Linux/macOS use `python3`. No Windows, se `python` não funcionar, tente `py -3.12`.) O instalador cria o ambiente, instala tudo e gera o `.env` com uma senha aleatória. Depois, para ligar:

| Sistema | Comando |
| --- | --- |
| Windows (PowerShell) | `.\.venv\Scripts\python.exe main.py` |
| Linux / macOS | `.venv/bin/python main.py` |

Deixe a janela aberta enquanto usa. Por segurança o serviço só aceita acessos **deste computador**. Se outro aparelho da rede precisar usar, coloque `HOST=0.0.0.0` no `.env` e proteja com firewall/HTTPS. Início automático no Linux: [BEGINNERS_GUIDE.md](BEGINNERS_GUIDE.md).

## Testando com curl

Troque `SUA_SENHA` pelo valor de `API_KEY` do seu `.env`. No Windows 10/11 use `curl.exe` (o `curl` do PowerShell é outro programa). Os exemplos abaixo usam aspas simples do Linux/macOS/Git Bash; para PowerShell veja o [exemplo logo depois](#no-windows-powershell).

**1. O serviço está ligado?** (não precisa de senha)

```sh
curl http://localhost:5050/health
# {"status":"ok"}
```

**2. Gerar um MP3 simples** (o arquivo `ola.mp3` aparece na pasta atual):

```sh
curl http://localhost:5050/v1/audio/speech \
  -H "Authorization: Bearer SUA_SENHA" \
  -H "Content-Type: application/json" \
  -d '{"input": "Olá! Meu serviço de voz está funcionando."}' \
  --output ola.mp3
```

**3. Escolher voz, velocidade e formato:**

```sh
curl http://localhost:5050/v1/audio/speech \
  -H "Authorization: Bearer SUA_SENHA" \
  -H "Content-Type: application/json" \
  -d '{"input": "Bom dia, tudo bem?", "voice": "alloy", "speed": 1.15, "response_format": "wav"}' \
  --output bomdia.wav
```

**4. Texto misturando português e inglês** (as vozes multilíngues leem os dois):

```sh
curl http://localhost:5050/v1/audio/speech \
  -H "Authorization: Bearer SUA_SENHA" \
  -H "Content-Type: application/json" \
  -d '{"input": "Hoje vamos aprender a palavra \"beautiful\" em inglês.", "voice": "pt-BR-ThalitaMultilingualNeural"}' \
  --output misto.mp3
```

**5. Listar vozes disponíveis** (só as multilíngues; tire `multilingual=true` para ver todas; `locale=pt-BR` filtra por idioma):

```sh
curl "http://localhost:5050/v1/audio/voices?multilingual=true" -H "Authorization: Bearer SUA_SENHA"
```

#### No Windows (PowerShell)

```powershell
$h = @{ Authorization = "Bearer SUA_SENHA" }
$corpo = '{"input": "Olá! Meu serviço de voz está funcionando.", "voice": "alloy"}'
Invoke-WebRequest -Uri http://localhost:5050/v1/audio/speech -Method Post -Headers $h `
  -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($corpo)) -OutFile ola.mp3
```

Também dá para testar pelo navegador em [http://localhost:5050/docs](http://localhost:5050/docs) (botão **Authorize**, depois **Try it out**).

> `/health` só prova que o programa está ligado. **Só gerar um áudio prova que a conexão com o Edge funciona.**

### O que você pode enviar

| Campo | Obrigatório | Valores |
| --- | --- | --- |
| `input` | sim | Texto, até 10.000 caracteres. Emojis e Markdown são removidos antes de falar |
| `voice` | não | Apelido (tabela abaixo) ou nome do Edge, como `pt-BR-FranciscaNeural`. Padrão: `pt-BR-ThalitaMultilingualNeural` |
| `response_format` | não | `mp3` (padrão), `wav`, `opus`, `aac`, `flac`, `pcm`. Fora o MP3, precisam de FFmpeg (já vem no Docker) |
| `speed` | não | De `0.25` a `2.0` (1.0 = normal) |
| `model` | não | Ignorado (aceita `tts-1`, `tts-1-hd` ou qualquer nome); existe só por compatibilidade |

### Apelidos de voz (compatíveis com a OpenAI)

Todos usam vozes multilíngues, que leem bem português e inglês. Edite `voices.json` para trocar (reinicie depois). Gênero e perfil são aproximações; confira o som no seu caso.

| Apelido | Voz | Apelido | Voz |
| --- | --- | --- | --- |
| `alloy` | Thalita (pt-BR, F) | `onyx` | Rémy (fr-FR, M) |
| `ash` | Andrew (en-US, M) | `nova` | Seraphina (de-DE, F) |
| `ballad` | Brian (en-US, M) | `sage` | Vivienne (fr-FR, F) |
| `cedar` | William (en-AU, M) | `shimmer` | Emma (en-US, F) |
| `coral` | Ava (en-US, F) | `marin` | Emma (en-US, F) |
| `echo` | Giuseppe (it-IT, M) | `verse` | Hyunsu (ko-KR, M) |
| `fable` | Giuseppe (it-IT, M) | | |

Lista completa e detalhes: [VOICES.md](VOICES.md).

## Usando no n8n e em outros programas

Em qualquer programa que peça dados da OpenAI: **Base URL** `http://localhost:5050/v1`, **chave** = sua `API_KEY`, **modelo** `tts-1`, **voz** um apelido. Se o n8n roda em Docker, `localhost` é o próprio n8n: use o nome do serviço ou um endereço HTTPS. Detalhes: [N8N-INTEGRATION.md](N8N-INTEGRATION.md) e [API_USAGE_GUIDE.md](API_USAGE_GUIDE.md) (inclui Python).

## Acesso pela internet (opcional)

Por padrão só o seu computador acessa (`127.0.0.1`). Para usar de fora, coloque na frente um proxy HTTPS (Nginx, Caddy...) ou um **Cloudflare Tunnel**. Nunca deixe a porta aberta sem senha. O Cloudflare Worker incluído é opcional. Passo a passo: [DEPLOY.md](DEPLOY.md).

## Configuração (arquivo `.env`)

| Variável | Para que serve | Padrão |
| --- | --- | --- |
| `API_KEY` | Sua senha; obrigatória | (você define) |
| `PORT` | Porta | `5050` |
| `HOST` | Quem acessa (sem Docker) | `127.0.0.1` |
| `DEFAULT_VOICE` / `DEFAULT_RESPONSE_FORMAT` / `DEFAULT_SPEED` | Padrões quando o pedido não informa | Thalita / `mp3` / `1.0` |
| `REMOVE_FILTER` | `True` desliga a limpeza de emojis e Markdown | `False` |
| `MAX_INPUT_CHARS`, `TTS_TIMEOUT_SECONDS`, `MAX_CONCURRENT_TTS` | Limites de texto, tempo e pedidos simultâneos | 10000 / 90 / 4 |
| `PROXY` | Proxy de **saída** até a Microsoft, se sua rede exigir | vazio |

Todas as opções estão comentadas em [.env.example](.env.example). Nunca publique seu `.env`.

## Problemas comuns

| Sintoma | Causa e solução |
| --- | --- |
| `401` | Senha errada ou ausente. Use `Authorization: Bearer SUA_SENHA` com o valor do `.env` |
| `502` ao gerar áudio | O Edge recusou ou a conexão falhou (erro **403** do serviço = biblioteca desatualizada). Atualize o projeto (`git pull`) e reconstrua (`docker compose up -d --build`) ou rode `python scripts/setup.py` |
| `503` | `API_KEY` vazia no servidor, ou muitos pedidos ao mesmo tempo; tente de novo |
| `504` | Demorou demais; texto menor ou aumente `TTS_TIMEOUT_SECONDS` |
| `400` | Pedido inválido (texto vazio, voz/formato/velocidade inválidos). A resposta diz o motivo |
| Formato ≠ MP3 falha | FFmpeg não instalado (fora do Docker) |
| Porta ocupada | Troque `PORT` no `.env` |
| `docker compose` reclama de API_KEY | Falta preencher `API_KEY` no `.env` |

Mais ajuda: [Issues](https://github.com/samucamg/multivozes_br_engine/issues).

## Atualizar, testar e contribuir

Guarde uma cópia do seu `.env` e `voices.json`, depois: `git pull` e `docker compose up -d --build` (ou `python scripts/setup.py` sem Docker). Testes: `python -m pip install -r requirements-dev.txt` e `python -m unittest discover -s tests -v` (não chamam o Edge). Histórico: [CHANGELOG.md](CHANGELOG.md).

Licença [MIT](LICENSE).

---

# 🇺🇸 English

Turns text into speech (MP3, WAV, Opus...) on **your own computer or server**, using the same endpoint as OpenAI (`/v1/audio/speech`). Works with **n8n**, the [MultiVozes panel](https://multivozes.com/) and any program that talks to the OpenAI speech API. Created by **Samuel de Sousa Santos**, based on [travisvn/openai-edge-tts](https://github.com/travisvn/openai-edge-tts). Voices come from Microsoft Edge's free service through the [edge-tts](https://github.com/rany2/edge-tts) library: no OpenAI account or credit card needed.

> ⚠️ The Edge service is external and Microsoft may change its rules (it has happened: **403** errors). If it stops working, see [Troubleshooting](#troubleshooting).

## 4-step install (recommended: Docker)

**1. Install Docker.** Windows/macOS: [Docker Desktop](https://www.docker.com/products/docker-desktop/). Linux: Docker Engine with Compose.

**2. Get the project.** With Git: `git clone https://github.com/samucamg/multivozes_br_engine.git`. Without Git: green **Code → Download ZIP** button on GitHub, then extract.

**3. Create your password (API key).** Open a terminal **inside the project folder**.

| System | Command |
| --- | --- |
| Windows (PowerShell) | `Copy-Item .env.example .env` |
| Linux / macOS | `cp .env.example .env` |

Open `.env` in a text editor and type a long password after `API_KEY=`, e.g. `API_KEY=my-very-long-password-9482`. You will send it with every request. *(If you have Python, `python scripts/setup.py --configure-only` does this for you with a random password.)*

**4. Start it.**

```sh
docker compose up -d --build
```

The first run takes a few minutes. Done: the service is at `http://localhost:5050`. Stop with `docker compose down`; view logs with `docker compose logs -f --tail=100`.

## Install without Docker (Windows, Linux, macOS)

Needs **Python 3.10–3.13** (3.12 recommended) and, for formats other than MP3, **FFmpeg** (Windows: `winget install Gyan.FFmpeg`; Ubuntu/Debian: `sudo apt install ffmpeg`; macOS: `brew install ffmpeg`).

```sh
git clone https://github.com/samucamg/multivozes_br_engine.git
cd multivozes_br_engine
python scripts/setup.py
```

(Use `python3` on Linux/macOS; on Windows try `py -3.12` if `python` fails.) The installer creates the environment, installs everything and writes `.env` with a random password. To start:

| System | Command |
| --- | --- |
| Windows (PowerShell) | `.\.venv\Scripts\python.exe main.py` |
| Linux / macOS | `.venv/bin/python main.py` |

Keep the window open while using it. For safety the service only accepts connections from **this computer**. If another device on your network needs it, set `HOST=0.0.0.0` in `.env` and protect it with a firewall/HTTPS. Linux autostart: [BEGINNERS_GUIDE.md](BEGINNERS_GUIDE.md).

## Testing with curl

Replace `YOUR_PASSWORD` with the `API_KEY` from your `.env`. On Windows 10/11 use `curl.exe` (PowerShell's `curl` is a different program). Examples use Linux/macOS/Git Bash quoting; see the [PowerShell example](#on-windows-powershell) below.

**1. Is it running?** (no password needed)

```sh
curl http://localhost:5050/health
# {"status":"ok"}
```

**2. Generate a simple MP3** (`hello.mp3` is created in the current folder):

```sh
curl http://localhost:5050/v1/audio/speech \
  -H "Authorization: Bearer YOUR_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello! My voice service is working."}' \
  --output hello.mp3
```

**3. Choose voice, speed and format:**

```sh
curl http://localhost:5050/v1/audio/speech \
  -H "Authorization: Bearer YOUR_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"input": "Good morning, how are you?", "voice": "coral", "speed": 1.15, "response_format": "wav"}' \
  --output morning.wav
```

**4. Mixed Portuguese and English text** (multilingual voices read both):

```sh
curl http://localhost:5050/v1/audio/speech \
  -H "Authorization: Bearer YOUR_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"input": "Hoje vamos aprender a palavra \"beautiful\" em inglês.", "voice": "pt-BR-ThalitaMultilingualNeural"}' \
  --output mixed.mp3
```

**5. List available voices** (multilingual only; drop `multilingual=true` for all; `locale=en-US` filters by language):

```sh
curl "http://localhost:5050/v1/audio/voices?multilingual=true" -H "Authorization: Bearer YOUR_PASSWORD"
```

#### On Windows (PowerShell)

```powershell
$h = @{ Authorization = "Bearer YOUR_PASSWORD" }
$body = '{"input": "Hello! My voice service is working.", "voice": "coral"}'
Invoke-WebRequest -Uri http://localhost:5050/v1/audio/speech -Method Post -Headers $h `
  -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($body)) -OutFile hello.mp3
```

You can also test in the browser at [http://localhost:5050/docs](http://localhost:5050/docs) (**Authorize** button, then **Try it out**).

> `/health` only proves the program is running. **Only generating audio proves the connection to Edge works.**

### What you can send

| Field | Required | Values |
| --- | --- | --- |
| `input` | yes | Text, up to 10,000 characters. Emojis and Markdown are stripped before speaking |
| `voice` | no | An alias (table below) or an Edge name such as `en-US-AvaMultilingualNeural`. Default: `pt-BR-ThalitaMultilingualNeural` |
| `response_format` | no | `mp3` (default), `wav`, `opus`, `aac`, `flac`, `pcm`. Everything but MP3 needs FFmpeg (included in Docker) |
| `speed` | no | `0.25` to `2.0` (1.0 = normal) |
| `model` | no | Ignored (accepts `tts-1`, `tts-1-hd` or any name); kept for compatibility only |

### Voice aliases (OpenAI-compatible)

All map to multilingual voices, which read Portuguese and English well. Edit `voices.json` to change them (restart afterwards). Gender and profile are approximations; listen before relying on them.

| Alias | Voice | Alias | Voice |
| --- | --- | --- | --- |
| `alloy` | Thalita (pt-BR, F) | `onyx` | Rémy (fr-FR, M) |
| `ash` | Andrew (en-US, M) | `nova` | Seraphina (de-DE, F) |
| `ballad` | Brian (en-US, M) | `sage` | Vivienne (fr-FR, F) |
| `cedar` | William (en-AU, M) | `shimmer` | Emma (en-US, F) |
| `coral` | Ava (en-US, F) | `marin` | Emma (en-US, F) |
| `echo` | Giuseppe (it-IT, M) | `verse` | Hyunsu (ko-KR, M) |
| `fable` | Giuseppe (it-IT, M) | | |

Full list and details: [VOICES.md](VOICES.md).

## Using it with n8n and other tools

In any tool that asks for OpenAI settings: **Base URL** `http://localhost:5050/v1`, **key** = your `API_KEY`, **model** `tts-1`, **voice** an alias. If n8n runs in Docker, `localhost` means n8n itself: use the service name or an HTTPS address. Details: [N8N-INTEGRATION.md](N8N-INTEGRATION.md) and [API_USAGE_GUIDE.md](API_USAGE_GUIDE.md) (includes Python).

## Internet access (optional)

By default only your computer can reach it (`127.0.0.1`). To use it remotely, put an HTTPS proxy (Nginx, Caddy...) or a **Cloudflare Tunnel** in front. Never leave the port open without a password. The bundled Cloudflare Worker is optional. Step by step: [DEPLOY.md](DEPLOY.md).

## Settings (`.env` file)

| Variable | Purpose | Default |
| --- | --- | --- |
| `API_KEY` | Your password; required | (you set it) |
| `PORT` | Port | `5050` |
| `HOST` | Who can connect (non-Docker) | `127.0.0.1` |
| `DEFAULT_VOICE` / `DEFAULT_RESPONSE_FORMAT` / `DEFAULT_SPEED` | Defaults when a request omits them | Thalita / `mp3` / `1.0` |
| `REMOVE_FILTER` | `True` disables emoji/Markdown cleaning | `False` |
| `MAX_INPUT_CHARS`, `TTS_TIMEOUT_SECONDS`, `MAX_CONCURRENT_TTS` | Text, time and simultaneous-request limits | 10000 / 90 / 4 |
| `PROXY` | **Outgoing** proxy to Microsoft, if your network needs one | empty |

All options are commented in [.env.example](.env.example). Never publish your `.env`.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `401` | Wrong or missing password. Send `Authorization: Bearer YOUR_PASSWORD` with the `.env` value |
| `502` when generating audio | Edge refused or the connection failed (a service **403** = outdated library). Update the project (`git pull`) and rebuild (`docker compose up -d --build`) or run `python scripts/setup.py` |
| `503` | Empty `API_KEY` on the server, or too many simultaneous requests; retry |
| `504` | Took too long; use shorter text or raise `TTS_TIMEOUT_SECONDS` |
| `400` | Invalid request (empty text, bad voice/format/speed). The response says why |
| Non-MP3 format fails | FFmpeg missing (outside Docker) |
| Port in use | Change `PORT` in `.env` |
| `docker compose` complains about API_KEY | Fill in `API_KEY` in `.env` |

More help: [Issues](https://github.com/samucamg/multivozes_br_engine/issues).

## Update, test and contribute

Keep a copy of your `.env` and `voices.json`, then: `git pull` and `docker compose up -d --build` (or `python scripts/setup.py` without Docker). Tests: `python -m pip install -r requirements-dev.txt` and `python -m unittest discover -s tests -v` (they do not call Edge). History: [CHANGELOG.md](CHANGELOG.md).

License [MIT](LICENSE).
