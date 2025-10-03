# Multivozes BR Engine 🇧🇷

<p align="center">
  <a href="https://multivozes.com" target="_blank">
    <img src="https://multivozes.com/assets/images/Logo_Multivozes.png" alt="Logo Painel Multivozes" width="150"/>
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Versão-2.0.0_Multilingual-blue?style=for-the-badge" alt="Versão">
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge" alt="Licença">
</p>

<p align="center">
  <a href="https://www.youtube.com/c/samucatutoriais" target="_blank">
    <img src="https://multivozes.com/assets/images/banner-youtube.png" alt="Canal Samuca Tutoriais" width="150"/>
  </a>
</p>

Uma API de TTS (Text-to-Speech) auto-hospedada, 100% compatível com a OpenAI, que utiliza as vozes neurais de alta qualidade e gratuitas da Microsoft Edge. Agora com **suporte a vozes multilinguais**, configuração simplificada e conversão real de formatos de áudio.

Este projeto foi criado por **Samuel de Sousa Santos** e é baseado no excelente trabalho de [travisvn/openai-edge-tts](https://github.com/travisvn/openai-edge-tts).

---

## 🌟 Novidades da Versão 2.0.0

A versão 2.0 traz melhorias significativas focadas em flexibilidade e qualidade:

* **🗣️ Novas Vozes Multilinguais:** Use vozes capazes de falar múltiplos idiomas de forma fluida, incluindo Português, Inglês, Italiano e mais.
* **✍️ Mapeamento de Vozes Simplificado:** Personalize facilmente os apelidos de voz da OpenAI (`alloy`, `echo`, etc.) através de um ficheiro externo `voices.json`.
* **🎵 Conversão de Áudio Real:** Garantia de que o formato de áudio solicitado (`mp3`, `opus`, `flac`, etc.) é gerado corretamente usando `pydub` e `ffmpeg`.

Para ver todos os detalhes, consulte o nosso [**CHANGELOG.md**](CHANGELOG.md).

## 🚀 Principais Funcionalidades

* **✅ 100% Compatível com a API OpenAI:** Substitua o endpoint e comece a usar. Perfeito para n8n, Make, e outros sistemas.
* **⚡ Estabilidade Garantida:** Geração de áudio assíncrona para respostas rápidas e estáveis.
* **🧠 Filtro de Texto Inteligente:** Limpeza automática de emojis e Markdown para um áudio puro.
* **🔐 Segurança:** Proteção via chave de API (Bearer Token).
* **⚙️ Totalmente Configurável:** Altere portas, chaves, e vozes padrão via ficheiro `.env`.
* **🇧🇷 Feito no Brasil:** Todo o projeto e documentação em português.

## ✨ A Cereja do Bolo: Integração com o Painel MultiVozes

O **Multivozes BR Engine** foi projetado para ser o motor perfeito para o [Painel MultiVozes](https://multivozes.com/), transformando uma simples API em uma plataforma de produção de áudio completa e profissional.

| Funcionalidade | Usar a API Sozinha | Aliança MultiVozes + Engine |
| :--- | :---: | :---: |
| Vozes de Alta Qualidade | ✓ | ✓ |
| Geração Rápida e Gratuita | ✓ | ✓ |
| **Gestão de Múltiplos Usuários** | ❌ | ✓ |
| **Controle de Uso (Créditos)** | ❌ | ✓ |
| **Interface Visual para Diálogos**| ❌ | ✓ |
| **Histórico de Áudios Pessoal** | ❌ | ✓ |
| **Painel de Administração** | ❌ | ✓ |

## 📚 Documentação Completa

Para tirar o máximo proveito do projeto, consulte os nossos guias detalhados:

* [**Guia de Instalação para Iniciantes**](BEGINNERS_GUIDE.md)
* [**Guia de Uso da API e Exemplos**](API_USAGE_GUIDE.md)
* [**Guia de Integração com o n8n**](N8N-INTEGRATION.md)
* [**Guia de Vozes Disponíveis**](VOICES.md)
* [**Histórico de Versões (Changelog)**](CHANGELOG.md)
* [**Auxílio e Suporte**](SUPPORT.md)

## 📋 Pré-requisitos

* **Python 3.8 ou superior**
* **Git**
* **FFmpeg** (Essencial para a conversão de formatos de áudio)

## 🛠️ Guia de Instalação Rápida

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/samucamg/multivozes_br_engine.git](https://github.com/samucamg/multivozes_br_engine.git)
    cd multivozes_br_engine
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure o `.env`:** Copie `.env.example` para `.env` e defina sua `API_KEY`.
    ```bash
    cp .env.example .env
    ```
5.  **(Novo!) Crie e personalize as vozes:** Copie `voices.example.json` para `voices.json` para definir seus mapeamentos de voz.
    ```bash
    cp voices.example.json voices.json
    ```

## ▶️ Executando o Servidor

Com o ambiente virtual ativado, inicie o servidor com:
```bash
python main.py
```

## 🎤 Referência de Vozes

Para uma lista completa de vozes recomendadas e testadas, divididas por idioma e funcionalidade, consulte o nosso [**Guia de Vozes (VOICES.md)**](VOICES.md).

---

## 📄 Licença e Política de Suporte

Este projeto é distribuído sob a **licença MIT**. Para entender as opções de suporte gratuito (comunitário) e comercial (pago), por favor, consulte a nossa página de [**Auxílio e Suporte (SUPPORT.md)**](SUPPORT.md).