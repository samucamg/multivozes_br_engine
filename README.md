# Multivozes BR Engine 🇧🇷

<p align="center">
  <img src="https://img.shields.io/badge/Versão-1.1.0_Estável-blue?style=for-the-badge" alt="Versão">
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge" alt="Licença">
  <img src="https://img.shields.io/badge/Canal-Samuca_Tutoriais-red?style=for-the-badge&logo=youtube" alt="Canal Samuca Tutoriais">
</p>

Uma API de TTS (Text-to-Speech) auto-hospedada, 100% compatível com a OpenAI, que utiliza as vozes neurais de alta qualidade e gratuitas da Microsoft Edge. Rápida, eficiente e feita para a comunidade brasileira.

Este projeto foi criado por **Samuel de Sousa Santos** ([youtube.com/c/samucatutoriais](https://youtube.com/c/samucatutoriais)) e é baseado no excelente trabalho de [travisvn/openai-edge-tts](https://github.com/travisvn/openai-edge-tts).

## ⚠️ Nota Importante sobre Versões

Este projeto foi estabilizado com versões específicas das bibliotecas listadas no `requirements.txt`, especialmente a **`edge-tts==6.1.10`**. Versões mais recentes desta biblioteca apresentaram incompatibilidades que podem causar erros no servidor.

Para garantir o funcionamento correto, é **crucial** instalar as dependências usando o ficheiro `requirements.txt` fornecido, sem alterá-lo.

## 🚀 Principais Funcionalidades

* **✅ 100% Compatível com a API OpenAI:** Substitua o endpoint `api.openai.com` pelo seu e nada mais precisa ser alterado. Perfeito para integrações com n8n, Make, e outros sistemas.

* **⚡ Estabilidade Garantida:** A geração de áudio ocorre em um processo assíncrono e utiliza um arquivo temporário, garantindo estabilidade e respostas rápidas mesmo com múltiplas requisições.

* **🧠 Filtro de Texto Inteligente:** Remove automaticamente emojis e formatação Markdown do texto de entrada, evitando que a IA "leia" caracteres indesejados e garantindo um áudio limpo.

* **🎵 Suporte a Múltiplos Formatos:** Gere áudio nos formatos `mp3`, `opus`, `aac`, `flac`, `wav` e `pcm`.

* **🗣️ Seleção de Voz Flexível:** Use os nomes de voz padrão da OpenAI (`alloy`, `shimmer`, etc.) ou escolha diretamente qualquer uma das centenas de vozes do Edge-TTS (ex: `pt-BR-FranciscaNeural`).

* **🔐 Segurança:** Proteja seu servidor com autenticação via chave de API (Bearer Token).

* **⚙️ Totalmente Configurável:** Altere portas, chaves, vozes e outras configurações facilmente através de um arquivo `.env`.

* **🇧🇷 Feito no Brasil:** Todo o código, comentários e documentação em português para facilitar o uso e a contribuição da comunidade.

* **📚 Guia de Integração:** Quer usar no n8n? Siga nosso guia passo a passo para integrar a API em seus fluxos de trabalho.
  [**Conheça o Guia de Integração com o n8n**](N8N-INTEGRATION.md)

## ✨ A Cereja do Bolo: Integração com o Painel MultiVozes

O **Multivozes BR Engine** foi projetado para ser o motor perfeito para o [Painel MultiVozes](https://github.com/samucamg/multivozes), transformando uma simples API em uma plataforma de produção de áudio completa e profissional.

| Funcionalidade | Usar a API Sozinha | Aliança MultiVozes + Engine |
| --- | :---: | :---: |
| Vozes de Alta Qualidade | ✓ | ✓ |
| Geração Rápida e Gratuita | ✓ | ✓ |
| **Gestão de Múltiplos Usuários** | ❌ | ✓ |
| **Controle de Uso (Créditos)** | ❌ | ✓ |
| **Interface Visual para Diálogos**| ❌ | ✓ |
| **Histórico de Áudios Pessoal** | ❌ | ✓ |
| **Painel de Administração** | ❌ | ✓ |

## 📚 Documentação Completa

Para tirar o máximo proveito do projeto, consulte os nossos guias detalhados:

* [**Guia de Instalação para Iniciantes**](BEGINNERS_GUIDE.md): Passo a passo para instalar o projeto em VPS, Windows e WSL2.
* [**Guia de Uso da API e Exemplos**](API_USAGE_GUIDE.md): Aprenda a usar a API com exemplos práticos em `curl` e Python.
* [**Guia de Integração com o n8n**](N8N-INTEGRATION.md): Conecte o Multivozes aos seus fluxos de trabalho no n8n.

## 📋 Pré-requisitos

* **Python 3.8 ou superior**
* **FFmpeg** (Opcional, mas necessário para converter para formatos diferentes de MP3)
* Git (para clonar o repositório)

#### ⚙️ Requisitos de Servidor Recomendados

Para uma boa performance do **Multivozes BR Engine**, recomendamos um servidor (VPS) com as seguintes especificações mínimas:

* **CPU:** 2 vCores
* **RAM:** 4 GB
* **Disco:** 20 GB de espaço livre

O projeto foi testado e funciona perfeitamente nos seguintes sistemas operacionais (64 bits):
* **Linux:**
    * Ubuntu 22.04 / 24.04 LTS
    * Debian 11 / 12
    * AlmaLinux 8 / 9
    * Sistemas ARM64 com Ubuntu (ex: Oracle Cloud)
* **Windows:**
    * Windows 10 / 11, utilizando WSL2 com Ubuntu 22.04 ou 24.04

### Instalando o FFmpeg

- **Para Debian/Ubuntu:**
  ```bash
  sudo apt update && sudo apt install ffmpeg -y
  ```
- **Para CentOS/RHEL/AlmaLinux:**
  ```bash
  sudo dnf install [https://rpms.remirepo.net/enterprise/remi-release-8.rpm](https://rpms.remirepo.net/enterprise/remi-release-8.rpm) -y
  sudo dnf install --enablerepo=remi ffmpeg -y
  ```
- **Para Windows:**
  1. Baixe a última versão no site oficial: [ffmpeg.org](https://ffmpeg.org/download.html)
  2. Descompacte o arquivo (ex: `C:\\ffmpeg`).
  3. Adicione a pasta `bin` (ex: `C:\\ffmpeg\\bin`) à variável de ambiente `Path` do seu sistema.

## 🛠️ Guia de Instalação
*Para um guia mais detalhado, focado em iniciantes e cobrindo a instalação em VPS, Windows e WSL2, consulte o nosso [**Guia de Instalação para Iniciantes**](BEGINNERS_GUIDE.md)!*

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/samucamg/multivozes_br_engine.git](https://github.com/samucamg/multivozes_br_engine.git)
    cd multivozes_br_engine
    ```

2.  **Crie e ative um ambiente virtual (Recomendado):**
    ```bash
    # Para Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\\venv\\Scripts\\activate
    ```

3.  **Instale as dependências EXATAS:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure suas variáveis de ambiente:**
    - Copie o arquivo de exemplo: `cp .env.example .env` (ou `copy .env.example .env` no Windows).
    - Edite o arquivo `.env` e defina pelo menos a sua `API_KEY`.
    ```dotenv
    # Exemplo de .env
    PORT=5050
    API_KEY=sua-chave-super-secreta-aqui
    REQUIRE_API_KEY=True
    DEFAULT_VOICE=pt-BR-FranciscaNeural
    ```

## ▶️ Executando o Servidor

Com o ambiente virtual ativado, inicie o servidor com o comando:
```bash
python main.py
```
Você deverá ver uma mensagem indicando que o servidor está rodando na porta especificada. O endpoint principal estará disponível em `http://localhost:5050/v1/audio/speech`.

## ⚙️ Deploy como Serviço (Autostart)

Para rodar o servidor em produção de forma contínua, é recomendado configurá-lo como um serviço.

### Linux (systemd)

1. Use o ficheiro `multivozes_br_engine.service` que acompanha o projeto.
2. Copie o ficheiro para o diretório de serviços do systemd:
   ```bash
   sudo cp multivozes_br_engine.service /etc/systemd/system/
   ```
3. **Edite o ficheiro copiado** e ajuste os campos `User` e `WorkingDirectory` para corresponder ao seu ambiente.
   ```bash
   sudo nano /etc/systemd/system/multivozes_br_engine.service
   ```
4. Recarregue o daemon, habilite e inicie o serviço:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable multivozes_br_engine
   sudo systemctl start multivozes_br_engine
   sudo systemctl status multivozes_br_engine
   ```

### Windows (NSSM)

A forma mais robusta de criar um serviço no Windows é usando o [NSSM (Non-Sucking Service Manager)](https://nssm.cc/download).

1.  Baixe o NSSM e coloque o `nssm.exe` em um local acessível.
2.  Abra o `cmd` como Administrador e execute:
    ```cmd
    nssm.exe install MultivozesBREngine
    ```
3.  Uma janela de configuração irá abrir. Preencha os campos:
    - **Path:** Caminho para o `python.exe` dentro do seu ambiente virtual (`venv`). Ex: `C:\\caminho\\para\\multivozes_br_engine\\venv\\Scripts\\python.exe`
    - **Startup directory:** Caminho para a pasta raiz do projeto. Ex: `C:\\caminho\\para\\multivozes_br_engine`
    - **Arguments:** `main.py`
4.  Clique em "Install service" e inicie o serviço pelo painel de Serviços do Windows (`services.msc`).

## 🎤 Referência de Vozes

### Mapeamento de Vozes OpenAI (Padrão)
Esta tabela reflete o mapeamento de vozes configurado no código.

| Nome OpenAI | Voz Edge-TTS Mapeada | Gênero e Idioma |
| --- | :--- | :--- |
| `alloy` | `pt-BR-FranciscaNeural` | Feminino (PT-BR) |
| `echo` | `pt-BR-AntonioNeural` | Masculino (PT-BR) |
| `fable` | `en-US-RogerNeural` | Masculino (Inglês EUA) |
| `onyx` | `en-US-EricNeural` | Masculino (Inglês EUA) |
| `nova` | `en-US-AvaNeural` | Feminino (Inglês EUA) |
| `shimmer`| `en-US-EmmaNeural` | Feminino (Inglês EUA) |

### Outras Vozes Disponíveis (Exemplos)

#### Português (Brasil)
| Voz (Nome Técnico) | Gênero |
| --- | :--- |
| `pt-BR-AntonioNeural` | Masculino |
| `pt-BR-FranciscaNeural`| Feminino |
| `pt-BR-ThalitaNeural` | Feminino |

#### Inglês (US)
| Voz (Nome Técnico) | Gênero |
| --- | :--- |
| `en-US-AriaNeural` | Feminino |
| `en-US-GuyNeural` | Masculino |
| `en-US-JennyNeural` | Feminino |

## 📄 Licença e Suporte

Este projeto é distribuído gratuitamente sob a licença MIT. Ele foi testado e está funcional em **Ubuntu 22.04**, **AlmaLinux 9** e **Windows 10/11 com WSL2**.

Devido à natureza do software livre, **não oferecemos garantias de funcionamento** em todos os ambientes e configurações. Para questões complexas, resolução de bugs ou consultoria técnica, os serviços do desenvolvedor **podem ser contratados**.

Contato para consultoria via WhatsApp: **33999928964**.

