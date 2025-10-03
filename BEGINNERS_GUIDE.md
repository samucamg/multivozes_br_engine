 📘 Guia de Instalação para Iniciantes - Multivozes BR Engine

Olá! 👋 Bem-vindo ao Multivozes BR Engine! Este guia foi feito para você que está a começar e quer instalar o projeto passo a passo, sem complicações.

---

### 🤔 Antes de Começar: Conceitos Básicos

* **Servidor / VPS:** Um computador alugado na internet que fica ligado 24/7, ideal para hospedar este projeto.
* **Terminal:** A "tela preta" onde digitamos comandos.
* **SSH:** A "chave" para aceder e controlar o seu servidor de forma segura.
* **Ambiente Virtual (venv):** Uma "bolha" isolada para o nosso projeto Python, para que as dependências não se misturem com outros projetos.

---

### 💻 Opção 1: Instalação em Servidor (VPS) com Ubuntu/Debian (Recomendado)

1.  **Aceder ao seu Servidor via SSH:**
    ```bash
    ssh seu_usuario@IP_DO_SERVIDOR
    ```
2.  **Atualizar o Servidor:**
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
3.  **Instalar as Ferramentas Essenciais:**
    ```bash
    sudo apt install git python3 python3-venv ffmpeg -y
    ```
4.  **Instalar o Multivozes BR Engine:**
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

    # 6. Copie os ficheiros de exemplo de configuração
    cp .env.example .env
    cp voices.example.json voices.json
    ```
    **Muito importante:** Após copiar, abra o ficheiro `.env` para definir a sua `API_KEY` e o `voices.json` para personalizar as vozes, se desejar.

---

### 🖥️ Opção 2: Instalação no Windows com WSL2 (Testes Locais)

WSL2 (Subsistema do Windows para Linux) permite que você tenha um ambiente Linux completo dentro do seu Windows. É a forma mais fácil e compatível de rodar o projeto localmente.

1.  **Instalar/Ativar o WSL2:**
    Abra o PowerShell ou o Terminal do Windows como **Administrador** e execute:
    ```bash
    wsl --install
    ```
    Isso instalará o Ubuntu por padrão. Reinicie o seu computador quando solicitado.

2.  **Abrir o Terminal do Ubuntu:**
    Após reiniciar, procure por "Ubuntu" no seu Menu Iniciar e abra-o.

3.  **Siga os Passos do Servidor (Opção 1):**
    A partir daqui, você está num ambiente Linux! 🎉 Os passos são **exatamente os mesmos** da **Opção 1** (atualizar o sistema, instalar ferramentas, clonar, etc.).

---

### 🎉 E agora?

Com tudo instalado, volte para o [`README.md`](./README.md) principal e siga a seção **"Executando o Servidor"** para colocar o seu motor de voz para funcionar.
"""