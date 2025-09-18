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

Este projeto foi estabilizado com versões específicas das bibliotecas listadas no `requirements.txt`, especialmente a **`edge-tts==7.0.0`**. Versões mais recentes desta biblioteca apresentaram incompatibilidades que podem causar erros no servidor.

Para garantir o funcionamento correto, é **crucial** instalar as dependências usando o ficheiro `requirements.txt` fornecido.

## 🚀 Principais Funcionalidades

* **✅ 100% Compatível com a API OpenAI:** Substitua o endpoint `api.openai.com` pelo seu e nada mais precisa ser alterado. Perfeito para integrações com n8n, Make, e outros sistemas.
* **⚡ Estabilidade Garantida:** A geração de áudio ocorre em um processo assíncrono e utiliza um arquivo temporário, garantindo estabilidade e respostas rápidas.
* **🧠 Filtro de Texto Inteligente:** Remove automaticamente emojis e formatação Markdown do texto de entrada, garantindo um áudio limpo.
* **🎵 Suporte a Múltiplos Formatos:** Gere áudio nos formatos `mp3`, `opus`, `aac`, `flac`, `wav` e `pcm`.
* **🗣️ Seleção de Voz Flexível:** Use os nomes de voz padrão da OpenAI (`alloy`, `shimmer`, etc.) ou escolha diretamente qualquer uma das centenas de vozes do Edge-TTS.
* **🔐 Segurança:** Proteja seu servidor com autenticação via chave de API (Bearer Token).
* **⚙️ Totalmente Configurável:** Altere portas, chaves, vozes e outras configurações facilmente através de um arquivo `.env`.
* **🇧🇷 Feito no Brasil:** Todo o código, comentários e documentação em português.

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

## 📚 Documentação Completa

Para tirar o máximo proveito do projeto, consulte os nossos guias detalhados:

* [**Guia de Instalação para Iniciantes**](BEGINNERS_GUIDE.md): Passo a passo para instalar o projeto em VPS, Windows e WSL2.
* [**Guia de Uso da API e Exemplos**](API_USAGE_GUIDE.md): Aprenda a usar a API com exemplos práticos em `curl` e Python.
* [**Guia de Integração com o n8n**](N8N-INTEGRATION.md): Conecte o Multivozes aos seus fluxos de trabalho no n8n.

## 📋 Pré-requisitos

#### ⚙️ Requisitos de Servidor Recomendados
* **CPU:** 2 vCores
* **RAM:** 4 GB
* **Disco:** 20 GB de espaço livre

#### ✅ Sistemas Operacionais Testados (64 bits)
* **Linux:** Ubuntu 22.04/24.04, Debian 11/12, AlmaLinux 8/9, e sistemas ARM64 com Ubuntu.
* **Windows:** Windows 10/11 (utilizando WSL2 com Ubuntu).

#### 📦 Dependências de Software
* **Python 3.8 ou superior**
* **Git** (para clonar o repositório)
* **FFmpeg** (Opcional, mas necessário para converter para formatos diferentes de MP3)

## 🛠️ Guia de Instalação

*Para um guia mais detalhado, consulte o nosso [**Guia de Instalação para Iniciantes**](BEGINNERS_GUIDE.md)!*

1.  **Clone o repositório:** `git clone https://github.com/samucamg/multivozes_br_engine.git`
2.  **Crie e ative um ambiente virtual:** `python3 -m venv venv` e `source venv/bin/activate`
3.  **Instale as dependências:** `pip install -r requirements.txt`
4.  **Configure o `.env`:** Copie `.env.example` para `.env` e defina sua `API_KEY`.

## ▶️ Executando o Servidor
Com o ambiente virtual ativado, inicie com: `python main.py`

## 🎤 Referência de Vozes

### Mapeamento de Vozes OpenAI (Padrão)
| Nome OpenAI | Voz Edge-TTS Mapeada | Gênero e Idioma |
| :--- | :--- | :--- |
| `alloy` | `pt-BR-FranciscaNeural` | Feminino (PT-BR) |
| `echo` | `pt-BR-AntonioNeural` | Masculino (PT-BR) |
| `fable` | `en-US-RogerNeural` | Masculino (Inglês EUA) |
| `onyx` | `en-US-EricNeural` | Masculino (Inglês EUA) |
| `nova` | `en-US-AvaNeural` | Feminino (Inglês EUA) |
| `shimmer`| `en-US-EmmaNeural` | Feminino (Inglês EUA) |

### Outras Vozes Disponíveis (Lista Completa)

#### Multilíngue
| Voz (Nome Técnico) | Descrição |
| :--- | :--- |
| `en-US-AndrewMultilingualNeural` | Andrew (Masc - Multilíngue EN) |
| `en-US-AvaMultilingualNeural` | Ava (Fem - Multilíngue EN) |
| `en-US-BrianMultilingualNeural` | Brian (Masc - Multilíngue EN) |
| `en-US-EmmaMultilingualNeural` | Emma (Fem - Multilíngue EN) |
| `de-DE-FlorianMultilingualNeural` | Florian (Masc - Multilíngue Alemão) |
| `de-DE-SeraphinaMultilingualNeural` | Seraphina (Fem - Multilíngue Alemão) |
| `fr-FR-RemyMultilingualNeural` | Remy (Masc - Multilíngue Francês) |
| `fr-FR-VivienneMultilingualNeural` | Vivienne (Fem - Multilíngue Francês) |

#### Português (Brasil)
| Voz (Nome Técnico) | Descrição |
| :--- | :--- |
| `pt-BR-AntonioNeural` | Antonio (Masc) |
| `pt-BR-FranciscaNeural`| Francisca (Fem) |
| `pt-BR-ThalitaNeural` | Thalita (Fem) |

#### Espanhol
| Voz (Nome Técnico) | Descrição |
| :--- | :--- |
| `es-ES-SofiaNeural` | Sofia (Fem - Espanha) |
| `es-ES-AlvaroNeural` | Alvaro (Masc - Espanha) |
| `es-MX-DaliaNeural` | Dalia (Fem - México) |
| `es-MX-JorgeNeural` | Jorge (Masc - México) |

#### Inglês
| Voz (Nome Técnico) | Descrição |
| :--- | :--- |
| `en-US-AriaNeural` | Aria (Fem - EUA) |
| `en-US-GuyNeural` | Guy (Masc - EUA) |
| `en-US-JennyNeural` | Jenny (Fem - EUA) |
| `en-GB-SoniaNeural` | Sonia (Fem - Britânico) |
| `en-AU-NatashaNeural` | Natasha (Fem - Austrália) |
| `en-CA-ClaraNeural` | Clara (Fem - Canadá) |

## 📄 Licença e Política de Suporte

Este projeto é distribuído sob a licença MIT, oferecido gratuitamente "como está". Você tem total liberdade para usar, modificar e distribuir o código.

**Política de Suporte:**
O software é fornecido sem qualquer tipo de suporte gratuito por parte do desenvolvedor. A comunidade é encorajada a colaborar, mas para manter o projeto sustentável e permitir que o desenvolvedor se concentre em novas funcionalidades, a assistência individual funciona da seguinte forma:

* **O desenvolvedor não oferece suporte gratuito, não responde a dúvidas técnicas nem auxilia na resolução de problemas através do WhatsApp ou qualquer outro canal.**
* Qualquer tipo de ajuda, incluindo depuração de erros, consultoria para integrações ou implementação de funcionalidades personalizadas, **requer a contratação de uma consultoria ou de horas técnicas.**

Para orçamentos ou para agendar uma consultoria, o contato deve ser feito via email samucamg@gmail.com ou WhatsApp: **33999928964**.
