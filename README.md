Multivozes BR Engine 🇧🇷

<p align="center">
  <img src="https://img.shields.io/badge/Versão-1.0.0-blue?style=for-the-badge" alt="Versão">
  <img src="https://img-shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.com/github/license/samucamg/multivozes_br_engine?style=for-the-badge&color=green" alt="Licença">
  <img src="https://img.shields.io/badge/Canal-Samuca_Tutoriais-red?style=for-the-badge&logo=youtube" alt="Canal Samuca Tutoriais">
</p>

Uma API de TTS (Text-to-Speech) auto-hospedada, 100% compatível com a OpenAI, que utiliza as vozes neurais de alta qualidade e gratuitas da Microsoft Edge. Rápida, eficiente e feita para a comunidade brasileira.

Este projeto foi criado por **Samuel de Sousa Santos** ([youtube.com/c/samucatutoriais](https://youtube.com/c/samucatutoriais)) e é baseado no excelente trabalho de [travisvn/openai-edge-tts](https://github.com/travisvn/openai-edge-tts).

## 🚀 Principais Funcionalidades

- **✅ 100% Compatível com a API OpenAI:** Substitua o endpoint `api.openai.com` pelo seu e nada mais precisa ser alterado. Perfeito para integrações com n8n, Make, e outros sistemas.
- **⚡ Performance Otimizada:** A geração de áudio ocorre em um processo assíncrono e utiliza um arquivo temporário, garantindo estabilidade e respostas rápidas mesmo com múltiplas requisições.
- **🧠 Filtro de Texto Inteligente:** Remove automaticamente emojis e formatação Markdown do texto de entrada, evitando que a IA "leia" caracteres indesejados e garantindo um áudio limpo.
- **🎵 Suporte a Múltiplos Formatos:** Gere áudio nos formatos `mp3`, `opus`, `aac`, `flac`, `wav` e `pcm` (requer FFmpeg).
- **🗣️ Seleção de Voz Flexível:** Use os nomes de voz padrão da OpenAI (`alloy`, `shimmer`, etc.) ou escolha diretamente qualquer uma das centenas de vozes do Edge-TTS (ex: `pt-BR-FranciscaNeural`).
- **🔐 Segurança:** Proteja seu servidor com autenticação via chave de API (Bearer Token).
- **⚙️ Totalmente Configurável:** Altere portas, chaves, vozes e outras configurações facilmente através de um arquivo `.env`.
- **🇧🇷 Feito no Brasil:** Todo o código, comentários e documentação em português para facilitar o uso e a contribuição da comunidade.
- **📚 Guia de Integração:** Quer usar no n8n? Siga nosso guia passo a passo para integrar a API em seus fluxos de trabalho.
  [Clique aqui para ver o guia de integração com o n8n](https://github.com/samucamg/multivozes_br_engine/blob/main/N8N-INTEGRATION.md)

## ✨ A Cereja do Bolo: Integração com o Painel MultiVozes

O **Multivozes BR Engine** foi projetado para ser o motor perfeito para o [Painel MultiVozes](https://github.com/samucamg/multivozes), transformando uma simples API em uma plataforma de produção de áudio completa e profissional.

| Funcionalidade | Usar a API Sozinha | Aliança MultiVozes + Engine |
| :--- | :---: | :---: |
| Vozes de Alta Qualidade | ✓ | ✓ |
| Geração Rápida e Gratuita | ✓ | ✓ |
| **Gestão de Múltiplos Usuários** | ❌ | ✓ |
| **Controle de Uso (Créditos)** | ❌ | ✓ |
| **Interface Visual para Diálogos**| ❌ | ✓ |
| **Histórico de Áudios Pessoal** | ❌ | ✓ |
| **Painel de Administração** | ❌ | ✓ |

---

## 📋 Pré-requisitos

- **Python 3.8 ou superior**
- **FFmpeg** (Obrigatório para conversão de formatos de áudio)
- Git (para clonar o repositório)

### Instalando o FFmpeg

- **Para Debian/Ubuntu:**
  ```bash
  sudo apt update && sudo apt install ffmpeg -y
  ```
- **Para CentOS/RHEL/AlmaLinux:**
  ```bash
  sudo dnf install https://rpms.remirepo.net/enterprise/remi-release-8.rpm -y
  sudo dnf install --enablerepo=remi ffmpeg -y
  ```
- **Para Windows:**
  1. Baixe a última versão no site oficial: [ffmpeg.org](https://ffmpeg.org/download.html)
  2. Descompacte o arquivo (ex: `C:\\ffmpeg`).
  3. Adicione a pasta `bin` (ex: `C:\\ffmpeg\\bin`) à variável de ambiente `Path` do seu sistema.

---

## 🛠️ Guia de Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/samucamg/multivozes_br_engine.git
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

3.  **Instale as dependências:**
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

---

## ▶️ Executando o Servidor

Com o ambiente virtual ativado, inicie o servidor com o comando:

```bash
python main.py
```

Você deverá ver uma mensagem indicando que o servidor está rodando na porta especificada. O endpoint principal estará disponível em `http://localhost:5050/v1/audio/speech`.

---

## ⚙️ Deploy como Serviço (Autostart)

Para rodar o servidor em produção de forma contínua, é recomendado configurá-lo como um serviço.

### Linux (systemd)

1.  Copie o conteúdo do arquivo `multivozes_br_engine.service` que acompanha este projeto.
2.  Crie o arquivo de serviço no seu servidor:
    ```bash
    sudo nano /etc/systemd/system/multivozes_br_engine.service
    ```
3.  Cole o conteúdo e **edite os campos obrigatórios** (`User`, `WorkingDirectory`, `ExecStart`) com os seus dados.
4.  Recarregue o daemon do systemd, habilite e inicie o serviço:
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

---

## 🎤 Referência de Vozes

### Mapeamento de Vozes OpenAI (Recomendado)

| Nome OpenAI | Voz Edge-TTS Mapeada | Gênero |
| :--- | :--- | :--- |
| `alloy` | `en-US-JennyNeural` | Feminino (EUA) |
| `echo` | `en-US-GuyNeural` | Masculino (EUA) |
| `fable` | `en-GB-SoniaNeural` | Feminino (Britânico) |
| `onyx` | `en-US-EricNeural` | Masculino (EUA) |
| `nova` | `en-US-AvaNeural` | Feminino (EUA) |
| `shimmer`| `en-US-EmmaNeural` | Feminino (EUA) |

---

### Multilinguais e Outras Vozes

#### Multilinguais (EN e DE/FR)

| Voz (Nome Técnico) | Descrição | Gênero |
| :--- | :--- | :--- |
| `en-US-AndrewMultilingualNeural` | Andrew (Masc - Multilingue EN) | Masculino |
| `en-US-AvaMultilingualNeural` | Ava (Fem - Multilingue EN) | Feminino |
| `en-US-BrianMultilingualNeural` | Brian (Masc - Multilingue EN) | Masculino |
| `en-US-EmmaMultilingualNeural` | Emma (Fem - Multilingue EN) | Feminino |
| `de-DE-FlorianMultilingualNeural` | Florian (Masc - Multilingue Alemão) | Masculino |
| `de-DE-SeraphinaMultilingualNeural` | Seraphina (Fem - Multilingue Alemão) | Feminino |
| `fr-FR-RemyMultilingualNeural` | Remy (Masc - Multilingue Francês) | Masculino |
| `fr-FR-VivienneMultilingualNeural` | Vivienne (Fem - Multilingue Francês) | Feminino |

#### Português (Brasil)

| Voz (Nome Técnico) | Descrição | Gênero |
| :--- | :--- | :--- |
| `pt-BR-AntonioNeural` | Antonio (PT-BR) | Masculino |
| `pt-BR-FranciscaNeural` | Francisca (PT-BR) | Feminino |
| `pt-BR-ThalitaNeural` | Thalita (PT-BR) | Feminino |

#### Inglês (US e Outros)

| Voz (Nome Técnico) | Descrição | Gênero |
| :--- | :--- | :--- |
| `en-US-AndrewNeural` | Andrew (Masc - Inglês US) | Masculino |
| `en-US-AnaNeural` | Ana (Fem - Inglês US) | Feminino |
| `en-AU-NatashaNeural` | Natasha (Fem - Inglês Austrália) | Feminino |
| `en-AU-WilliamNeural` | William (Masc - Inglês Austrália) | Masculino |
| `en-CA-ClaraNeural` | Clara (Fem - Inglês Canadá) | Feminino |
| `en-CA-LiamNeural` | Liam (Masc - Inglês Canadá) | Masculino |
| `en-GB-LibbyNeural` | Libby (Fem - Inglês Britânico) | Feminino |
| `en-GB-MaisieNeural` | Maisie (Criança - Inglês Brit) | Feminino |
| `en-GB-RyanNeural` | Ryan (Masc - Inglês Britânico) | Masculino |
| `en-GB-SoniaNeural` | Sonia (Fem - Inglês Britânico) | Feminino |
| `en-GB-ThomasNeural` | Thomas (Masc - Inglês Britânico) | Masculino |
| `en-HK-SamNeural` | Sam (Masc - Inglês Hong Kong) | Masculino |
| `en-HK-YanNeural` | Yan (Fem - Inglês Hong Kong) | Feminino |
| `en-IE-ConnorNeural` | Connor (Masc - Inglês Irlandês) | Masculino |
| `en-IE-EmilyNeural` | Emily (Fem - Inglês Irlandês) | Feminino |
| `en-IN-NeerjaExpressiveNeural` | Priya (Fem - Inglês Indiano Exp) | Feminino |
| `en-IN-NeerjaNeural` | Neerja (Fem - Inglês Indiano) | Feminino |
| `en-IN-PrabhatNeural` | Prabhat (Masc - Inglês Indiano) | Masculino |
| `en-KE-AsiliaNeural` | Asilia (Fem - Inglês Quênia) | Feminino |
| `en-KE-ChilembaNeural` | Chilemba (Masc - Inglês Quênia) | Masculino |
| `en-NG-AbeoNeural` | Abeo (Masc - Inglês Nigéria) | Masculino |
| `en-NG-EzinneNeural` | Ezinne (Fem - Inglês Nigéria) | Feminino |
| `en-NZ-MitchellNeural` | Mitchell (Masc - Inglês Nova Zelândia) | Masculino |
| `en-NZ-MollyNeural` | Molly (Fem - Inglês Nova Zelândia) | Feminino |
| `en-PH-JamesNeural` | James (Masc - Inglês Filipina) | Masculino |
| `en-PH-RosaNeural` | Rosa (Fem - Inglês Filipina) | Feminino |
| `en-SG-LunaNeural` | Luna (Fem - Inglês Singapura) | Feminino |
| `en-SG-WayneNeural` | Wayne (Masc - Inglês Singapura) | Masculino |
| `en-TZ-ElimuNeural` | Elimu (Masc - Inglês Tanzânia) | Masculino |
| `en-TZ-ImaniNeural` | Imani (Fem - Inglês Tanzânia) | Feminino |
| `en-US-AriaNeural` | Aria (Fem - Inglês US) | Feminino |
| `en-US-AvaNeural` | Ava (Fem - Inglês US) | Feminino |
| `en-US-ChristopherNeural` | Christopher (Masc - Inglês US) | Masculino |
| `en-US-EmmaNeural` | Emma (Fem - Inglês US) | Feminino |
| `en-US-EricNeural` | Eric (Masc - Inglês US) | Masculino |
| `en-US-GuyNeural` | Guy (Masc - Inglês US) | Masculino |
| `en-US-JennyNeural` | Jenny (Fem - Inglês US) | Feminino |
| `en-US-MichelleNeural` | Michelle (Fem - Inglês US) | Feminino |
| `en-US-RogerNeural` | Roger (Masc - Inglês US) | Masculino |
| `en-US-SteffanNeural` | Steffan (Masc - Inglês US) | Masculino |
| `en-ZA-LeahNeural` | Leah (Fem - Inglês Africano) | Feminino |
| `en-ZA-LukeNeural` | Luke (Masc - Inglês Africano) | Masculino |

---

## 📄 Licença e Suporte

Este projeto é distribuído gratuitamente sob a licença MIT, o que significa que você tem total liberdade para usar, modificar e distribuir o código.

Ele foi testado e está funcional em ambientes como **Ubuntu 22.04 (64-bit)** e **Windows 10 com WSL2**. No entanto, devido à natureza do software livre, **não oferecemos garantias de funcionamento** em todos os ambientes e configurações. A comunidade é o nosso maior motor, mas o suporte oficial do desenvolvedor não está incluso na licença.

Para questões mais complexas, como a resolução de bugs, implementação de novas funcionalidades, ou consultoria técnica detalhada para o seu projeto, os serviços do desenvolvedor **podem ser contratados**.

Para orçamentos ou para agendar uma consultoria, entre em contato via WhatsApp: **33999928964**.

O desenvolvedor não atende, não tira dúvidas, nem resolve problemas via outros canais sem a contratação de uma consultoria ou hora técnica.

