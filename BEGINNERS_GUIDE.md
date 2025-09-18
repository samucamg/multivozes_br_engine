# -*- coding: utf-8 -*-

"""
Este ficheiro armazena o conteúdo do Guia de Instalação para Iniciantes
em formato Markdown, dentro de uma string Python.
"""

guide_content = """
# 📘 Guia de Instalação para Iniciantes - Multivozes BR Engine

Olá! 👋 Bem-vindo ao Multivozes BR Engine! Este guia foi feito para você que está a começar e quer instalar o projeto passo a passo, sem complicações. Vamos explicar os conceitos básicos e mostrar como instalar em diferentes ambientes.

---

### 🤔 Antes de Começar: Conceitos Básicos

Se alguns termos como "VPS" ou "Terminal" são novos para você, não se preocupe! Aqui está um resumo rápido:

* **Servidor / VPS (Servidor Virtual Privado):** Pense nele como um computador que você aluga na internet e que fica ligado 24 horas por dia, 7 dias por semana. É ideal para hospedar projetos como este.
* **Terminal (ou Linha de Comando):** É aquela "tela preta" onde digitamos comandos para o computador executar tarefas, em vez de usar o mouse. É a nossa principal ferramenta.
* **SSH (Secure Shell):** É a "chave" que nos permite aceder e controlar o nosso servidor (VPS) de forma segura a partir do nosso computador.
* **Ambiente Virtual (venv):** É como criar uma "bolha" ou uma "pasta isolada" para o nosso projeto Python. Isso garante que as dependências dele não se misturem com outros projetos no sistema.

---

### 💻 Opção 1: Instalação em Servidor (VPS) com Ubuntu/Debian

Esta é a opção recomendada para produção, para que o seu motor de voz esteja sempre online.

#### 1. Aceder ao seu Servidor via SSH
Para se conectar ao seu servidor, você precisará de um cliente de SSH.

* **No Windows:** Use o [PuTTY](https://www.putty.org/) ou o próprio Terminal do Windows.
* **No Linux/macOS:** Use o Terminal.

Digite o comando, substituindo com os seus dados:
```bash
ssh seu_usuario@IP_DO_SERVIDOR
```
Ser-lhe-á pedida a senha para entrar.

#### 2. Atualizar o Servidor
É uma boa prática garantir que todos os pacotes do sistema estão atualizados.
```bash
sudo apt update && sudo apt upgrade -y
```

#### 3. Instalar as Ferramentas Essenciais
Vamos instalar o `git` (para copiar o projeto), o `python3` e o `venv` (para criar o nosso ambiente isolado) e o `ffmpeg` (para os formatos de áudio).
```bash
sudo apt install git python3 python3-venv ffmpeg -y
```

#### 4. Instalar o Multivozes BR Engine
Agora que o servidor está pronto, siga os passos do `README.md` principal (que vamos replicar aqui para facilitar):

```bash
# 1. Clone o projeto do GitHub
git clone [https://github.com/samucamg/multivozes_br_engine.git](https://github.com/samucamg/multivozes_br_engine.git)

# 2. Entre na pasta do projeto
cd multivozes_br_engine

# 3. Crie o ambiente virtual (a "bolha")
python3 -m venv venv

# 4. Ative o ambiente virtual
source venv/bin/activate

# 5. Instale as dependências exatas do projeto
pip install -r requirements.txt

# 6. Copie o ficheiro de exemplo de configuração
cp .env.example .env
```
Pronto! Agora só falta configurar o seu ficheiro `.env` e iniciar o servidor, como explicado no `README.md` principal.

---

### 🖥️ Opção 2: Instalação no Windows com WSL2 (Recomendado para testes locais)

WSL2 (Subsistema do Windows para Linux) permite que você tenha um ambiente Linux completo dentro do seu Windows. É a forma mais fácil e compatível de rodar o projeto localmente.

#### 1. Instalar/Ativar o WSL2
Abra o PowerShell ou o Terminal do Windows como **Administrador** e execute:
```bash
wsl --install
```
Isso instalará o Ubuntu por padrão. Reinicie o seu computador quando solicitado.

#### 2. Abrir o Terminal do Ubuntu
Após reiniciar, procure por "Ubuntu" no seu Menu Iniciar e abra-o. Na primeira vez, ele irá configurar algumas coisas.

#### 3. Siga os Passos do Servidor (Opção 1)
A partir daqui, você está num ambiente Linux! 🎉 Os passos são **exatamente os mesmos** da **Opção 1**:
1.  Atualize o sistema (`sudo apt update && sudo apt upgrade -y`).
2.  Instale as ferramentas (`sudo apt install git python3 python3-venv ffmpeg -y`).
3.  Clone o projeto, crie e ative o venv, e instale as dependências.

---

### 🎉 E agora?

Com o ambiente preparado e as dependências instaladas, você está pronto para a parte final!

Volte para o [`README.md` principal](https://github.com/samucamg/multivozes_br_engine/blob/main/README.md) e siga as seções **"Configurar suas variáveis de ambiente"** e **"Executando o Servidor"** para colocar o seu motor de voz para funcionar.

Bom trabalho! 💪
"""
