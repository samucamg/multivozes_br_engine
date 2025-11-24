# 📘 Guia de Instalação para Iniciantes - Multivozes BR Engine

Olá! 👋 Bem-vindo ao Multivozes BR Engine! Este guia foi feito para você que está a começar e quer instalar o projeto passo a passo, sem complicações.

---

## 🤔 Antes de Começar: Conceitos Básicos

* **Servidor / VPS:** Um computador alugado na internet que fica ligado 24/7, ideal para hospedar este projeto.
* **Terminal:** A "tela preta" onde digitamos comandos.
* **SSH:** A "chave" para aceder e controlar o seu servidor de forma segura.
* **Ambiente Virtual (venv):** Uma "bolha" isolada para o nosso projeto Python, para que as dependências não se misturem com outros projetos.
* **Bearer Token:** Uma chave de segurança que protege sua API de acessos não autorizados.

---

## 💻 Opção 1: Instalação em Servidor (VPS) com Ubuntu/Debian (Recomendado)

### Passo 1: Aceder ao seu Servidor via SSH

```
ssh seu_usuario@IP_DO_SERVIDOR
```

### Passo 2: Atualizar o Servidor

```
sudo apt update && sudo apt upgrade -y
```

### Passo 3: Instalar as Ferramentas Essenciais

```
sudo apt install git python3 python3-venv python3-pip ffmpeg -y
```

### Passo 4: Clonar e Configurar o Projeto

```
# 1. Clone o projeto do GitHub
cd /opt
git clone https://github.com/samucamg/multivozes_br_engine.git

# 2. Entre na pasta do projeto
cd multivozes_br_engine

# 3. Crie o ambiente virtual (a "bolha")
python3 -m venv venv

# 4. Ative o ambiente virtual
source venv/bin/activate

# 5. Instale as dependências exatas do projeto
pip install -r requirements.txt

# 6. Copie os ficheiros de exemplo de configuração
cp .env.example .env
```

### Passo 5: Gerar sua Chave de API (Bearer Token)

Você precisa criar uma chave de API única e segura. Execute este comando para gerar uma automaticamente:

```
# Gera uma chave aleatória e segura com 64 caracteres
echo "API_KEY=sk-$(openssl rand -hex 32)" | tee -a .env
```

**Ou crie manualmente:** Abra o arquivo `.env` e defina sua própria chave:

```
nano .env
```

Edite a linha `API_KEY=` para algo como:
```
API_KEY=sk-sua-chave-secreta-aqui-123456789
```

**Dica:** Use uma chave longa e complexa. A chave gerada automaticamente é mais segura!

---

## ▶️ Executando o Servidor

Após a instalação, escolha como deseja executar:

### Opção A: Teste Rápido (Terminal Aberto)

Ideal para testar. Se fechar o terminal, o servidor para.

```
# Certifique-se de estar na pasta do projeto
cd /opt/multivozes_br_engine

# Ative o ambiente virtual
source venv/bin/activate

# Inicie o servidor
python main.py
```

### Opção B: Persistente com Tmux

O Tmux mantém o servidor rodando mesmo se você desconectar do SSH.

```
# Instale o Tmux
sudo apt install tmux -y

# Crie uma sessão
tmux new -s multivozes

# Dentro do Tmux, inicie o servidor
cd /opt/multivozes_br_engine
source venv/bin/activate
python main.py
```

**Para sair sem parar o servidor:** Pressione `Ctrl+B`, solte, depois pressione `D`

**Para voltar à sessão:**
```
tmux attach -t multivozes
```

### Opção C: Produção com Systemd (Instalação em Uma Linha) 🏆

Esta é a forma mais profissional. O servidor inicia automaticamente no boot e reinicia sozinho se houver falhas.

**Instalação Automática em Uma Única Linha:**

```
sudo bash -c "cat > /etc/systemd/system/multivozes.service <<EOF
[Unit]
Description=Multivozes BR Engine Service
After=network.target

[Service]
User=$USER
WorkingDirectory=/opt/multivozes_br_engine
ExecStart=/opt/multivozes_br_engine/venv/bin/python main.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF" && sudo systemctl daemon-reload && sudo systemctl enable --now multivozes && echo "✅ Serviço instalado e iniciado com sucesso!"
```

**Gerenciar o Serviço:**

```
# Ver status
sudo systemctl status multivozes

# Ver logs em tempo real
sudo journalctl -u multivozes -f

# Parar o serviço
sudo systemctl stop multivozes

# Reiniciar o serviço
sudo systemctl restart multivozes

# Desabilitar inicialização automática
sudo systemctl disable multivozes
```

---

## 🖥️ Opção 2: Instalação no Windows com WSL2 (Testes Locais)

WSL2 (Subsistema do Windows para Linux) permite que você tenha um ambiente Linux completo dentro do seu Windows. É a forma mais fácil e compatível de rodar o projeto localmente.

### Passo 1: Instalar/Ativar o WSL2

Abra o **PowerShell** ou o **Terminal do Windows** como **Administrador** e execute:

```
wsl --install
```

Isso instalará o Ubuntu por padrão. **Reinicie o computador** quando solicitado.

### Passo 2: Abrir o Terminal do Ubuntu

Após reiniciar, procure por **"Ubuntu"** no Menu Iniciar e abra-o.

### Passo 3: Configurar o Ubuntu

Na primeira vez, você precisará criar um usuário e senha para o Ubuntu.

### Passo 4: Seguir os Passos da Opção 1

A partir daqui, você está num ambiente Linux! 🎉 

Execute os comandos da **Opção 1** (Passos 2 a 5) normalmente no terminal do Ubuntu.

**Nota para Windows:** No WSL2, sua pasta do Windows fica em `/mnt/c/Users/SeuUsuario/`

---

## 🌐 Testando a API

Após iniciar o servidor, acesse a documentação interativa:

**Se instalou localmente (Windows/WSL2):**
- http://localhost:5050/docs

**Se instalou em servidor:**
- http://SEU_IP_DO_SERVIDOR:5050/docs

### Teste Rápido com cURL

```
curl -X POST http://localhost:5050/v1/audio/speech \
  -H "Authorization: Bearer SUA_CHAVE_API_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "Olá, este é um teste do Multivozes BR Engine!",
    "voice": "pt-BR-FranciscaNeural"
  }' \
  --output teste.mp3
```

**Lembre-se:** Substitua `SUA_CHAVE_API_AQUI` pela chave que você definiu no arquivo `.env`!

---

## 🆘 Problemas Comuns

### "docker: command not found"
Se você quiser usar Docker, instale com:
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### "Permission denied" ao executar comandos
Use `sudo` antes do comando ou verifique as permissões do diretório.

### Porta 5050 já está em uso
Altere a porta no arquivo `.env`:
```
nano .env
# Mude PORT=5050 para PORT=8080 (ou outra porta livre)
```

### O servidor para quando fecho o terminal
Use o **Tmux** (Opção B) ou **Systemd** (Opção C) para manter rodando em segundo plano.

---

## 🎉 Próximos Passos

Com tudo instalado e funcionando:

1. ✅ Configure suas vozes personalizadas em `voices.json`
2. ✅ Integre com n8n, Make ou outras plataformas
3. ✅ Explore o [Painel MultiVozes](https://multivozes.com) para uma interface completa
4. ✅ Leia o [Guia de Uso da API](API_USAGE_GUIDE.md) para comandos avançados

**Dúvidas?** Consulte o [SUPPORT.md](SUPPORT.md) ou o canal no YouTube!
```

**Pronto! Copie TUDO de uma única vez!** 🎯

