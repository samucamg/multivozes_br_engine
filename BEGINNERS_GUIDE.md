# Instalação e diagnóstico

Comece pelo [README](README.md). Este guia detalha dependências e execução contínua. O serviço depende de acesso HTTPS/WebSocket ao Edge; não funciona totalmente offline.

## Windows sem Docker

Instale Python 3.12 e Git, habilitando Python no PATH. Para outros formatos além de MP3:

```powershell
winget install --id Gyan.FFmpeg --exact
```

Abra um novo terminal após a instalação e confira `ffmpeg -version`.

```powershell
git clone https://github.com/samucamg/multivozes_br_engine.git
cd multivozes_br_engine
py -3.12 scripts/setup.py
.\.venv\Scripts\python.exe main.py
```

O script gera a chave no `.env` e não exige ativar o ambiente virtual, evitando mudanças na política de execução do PowerShell. Ao fechar o terminal, o processo termina. Para persistência no Windows, prefira Docker Desktop configurado para iniciar com o sistema.

## Debian/Ubuntu sem Docker

```sh
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ffmpeg git
git clone https://github.com/samucamg/multivozes_br_engine.git
cd multivozes_br_engine
python3 scripts/setup.py
.venv/bin/python main.py
```

Confira `python3 --version`: deve ser 3.10–3.13. Se a distribuição fornecer outra versão, use Python 3.12 ou Docker. Não instale dependências do projeto no Python global do sistema.

## macOS sem Docker

Com Homebrew instalado:

```sh
brew install python@3.12 ffmpeg git
git clone https://github.com/samucamg/multivozes_br_engine.git
cd multivozes_br_engine
python3.12 scripts/setup.py
.venv/bin/python main.py
```

## Docker

Use os passos do [README](README.md#instalação-em-4-passos-recomendado-docker). O contêiner roda sem privilégios, com sistema de arquivos somente leitura e espaço temporário limitado. Síntese e conversões usam `/tmp`; ajuste `tmpfs` em `compose.yaml` se o uso exigir mais espaço.

No Windows com WSL2, use a integração da distribuição com o Docker Desktop; não é necessário instalar outro Docker Engine no Ubuntu. No PowerShell, `docker context show` deve indicar o contexto do Docker Desktop (normalmente `desktop-linux`). Compare `docker info --format '{{.ID}}'` no Windows e na distribuição WSL: identificadores iguais confirmam que ambos usam o mesmo servidor Docker. Se o comando não funcionar no WSL, confira a integração da distribuição nas configurações do Docker Desktop.

Por padrão apenas o próprio computador acessa a porta publicada. Para acesso remoto prefira [proxy HTTPS/Tunnel](DEPLOY.md). `BIND_ADDRESS=0.0.0.0` no `.env` publica nas interfaces de rede: configure firewall e HTTPS antes.

## Início automático com systemd (Linux)

Use uma instalação dedicada em `/opt/multivozes_br_engine`; execute a instalação local antes. O arquivo de serviço usa usuário sem root. Ajuste os caminhos no arquivo se instalar em outro local.

```sh
sudo useradd --system --user-group --home-dir /opt/multivozes_br_engine --shell /usr/sbin/nologin multivozes
sudo chown -R multivozes:multivozes /opt/multivozes_br_engine
sudo chmod 600 /opt/multivozes_br_engine/.env
sudo cp multivozes_br_engine.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now multivozes_br_engine
sudo systemctl status multivozes_br_engine
```

Se o usuário já existir, pule `useradd`. A mudança de proprietário vale apenas para a instalação dedicada em `/opt`, não uma pasta compartilhada com outros projetos. O aplicativo lê `.env`; não duplique segredos no serviço.

```sh
sudo journalctl -u multivozes_br_engine -f
sudo systemctl restart multivozes_br_engine
sudo systemctl stop multivozes_br_engine
```

## Confirmar funcionamento

1. `/health`: processo iniciou.
2. `/v1/models`: cliente alcança o servidor.
3. `/v1/voices` com chave: catálogo consulta Edge.
4. `/v1/audio/speech` com texto curto gera MP3: síntese real funciona.
5. Repita com `wav`: confirma FFmpeg e conversão.

Exemplos em [API_USAGE_GUIDE.md](API_USAGE_GUIDE.md). Saúde não consulta Microsoft e não comprova síntese.

## Problemas frequentes

| Sintoma | Verificação |
| --- | --- |
| Conexão recusada | Processo ativo, porta e endereço corretos? `docker compose ps` e logs |
| HTTP 401 | Envie `Authorization: Bearer CHAVE_DO_ENV`; no Worker use a chave do proxy |
| Falha ao autenticar | Chave vazia com autenticação habilitada? Configure e reinicie |
| MP3 funciona, WAV/Opus falha | Confira `ffmpeg -version` no ambiente do servidor |
| Edge 403/NoAudioReceived | Versão edge-tts, relógio, proxy de saída e voz do catálogo; catálogo Azure não prova disponibilidade Edge |
| Timeout/502/503 | Texto curto e voz pt-BR; confira acesso externo no host e logs |
| Porta ocupada | Ajuste `PORT` e reinicie; Compose exige recriar o contêiner |
| n8n em Docker não acessa localhost | localhost é o contêiner n8n; use rede compartilhada ou endereço HTTPS |

Para diagnóstico, informe commit (`git rev-parse HEAD`), sistema/Python, versão edge-tts e erro com texto público. Nunca envie `.env`, tokens, texto de clientes ou URL de proxy com senha.
