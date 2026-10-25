# Histórico de Versões (Changelog)

Todas as mudanças notáveis neste projeto serão documentadas neste ficheiro.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] - 2026-10-25

### Corrigido

* Atualização do Edge TTS para 7.3.1, com suporte ao protocolo Sec-MS-GEC v2 exigido pelo serviço atual. A versão 7.0.0 foi testada e reproduziu HTTP 403.
* Validação de JSON, texto, voz, formato e velocidade; erros de entrada preservam respostas 400/413, sem expor mensagens internas do provedor. `model` continua ignorado, como na versão anterior, para não quebrar integrações existentes.
* Cálculo da velocidade com arredondamento: 0.9 resulta em -10%, 1.15 em +15% e 1.2 em +20%, evitando truncamento de ponto flutuante.
* JSON profundamente aninhado tratado como erro de entrada; limpeza do temporário no envio mesmo se a resposta falhar ou for cancelada.
* Conversão assíncrona com FFmpeg e codecs explícitos para Opus/Ogg, AAC/ADTS, FLAC, WAV e PCM s16le, mono, 24 kHz. MP3 dispensa FFmpeg.
* Limpeza de temporários também quando a síntese é cancelada por timeout.
* Inicialização sem emojis incompatíveis com consoles Windows cp1252, preservando os créditos de Samuel e do projeto original em texto ASCII.
* Logo, vídeo de apresentação e link do canal restaurados no README após revisão.
* Documentação dos aliases alinhada a `voices.json`; Thalita preservada como padrão. Após revisão, `fable` usa Giuseppe masculino, `shimmer` usa Emma feminina e `marin` foi incluído usando Emma. Os 13 aliases usam exclusivamente vozes multilíngues; perfis são aproximações editoriais, sem equivalência auditiva comprovada com OpenAI.
* Fallback completo com os 13 aliases multilíngues e rejeição de configuração que associe um alias OpenAI a voz não multilíngue. Vozes técnicas diretas e aliases próprios continuam aceitando vozes regionais.

### Adicionado

* Consulta ao catálogo atual pelo utilitário `voices_catalog.py` e endpoint protegido `/v1/audio/voices` (aliases `/v1/voices` e `/voices`).
* `/health` sem chamadas externas; limites configuráveis de texto, corpo da requisição, concorrência e duração da síntese.
* Dockerfile, Docker Compose, instalador local e proxy Cloudflare Worker com chaves separadas para cliente e origem.
* Testes automatizados do backend, catálogo e proxy; fluxo de integração contínua para Python e Node.

### Alterado

* Instalação sem Docker agora escuta somente em `127.0.0.1` por padrão (variável `HOST`); Docker/Compose definem `HOST=0.0.0.0` dentro do contêiner e continuam publicando só em `127.0.0.1` no host. Quem acessa o serviço de outro aparelho sem Docker deve definir `HOST=0.0.0.0`.
* README reescrito em português e inglês, com instalação em 4 passos, exemplos curl/PowerShell, tabela de vozes e solução de problemas.
* Dependências diretas reduzidas e atualizadas; remoção de pydub e do SDK OpenAI do servidor.
* Instalação documentada para Python 3.10–3.13, com Python 3.12 recomendado, incluindo Windows e Linux.
* Guias de instalação, API, n8n, suporte e deploy revisados para o comportamento implementado.

---

## [2.0.0] - 2025-10-02

Esta é uma grande atualização focada em flexibilidade, qualidade de áudio e experiência do desenvolvedor.

### ✨ Adicionado (Added)

* **Suporte a Vozes Multilinguais:** Introdução de vozes neurais capazes de falar múltiplos idiomas de forma fluente. As novas vozes de destaque são:
    * `pt-BR-ThalitaMultilingualNeural`
    * `it-IT-GiuseppeMultilingualNeural`
    * `en-AU-WilliamMultilingualNeural`
    * `ko-KR-HyunsuMultilingualNeural`
* **Mapeamento de Vozes Externo (`voices.json`):** Agora é possível personalizar os apelidos de voz da OpenAI (`alloy`, `echo`, etc.) editando um simples ficheiro JSON, sem a necessidade de alterar o código Python. Um ficheiro de exemplo (`voices.example.json`) foi adicionado para facilitar a configuração.
* **Criação deste `CHANGELOG.md`:** Para documentar as mudanças entre as versões de forma clara e profissional.

### ♻️ Alterado (Changed)

* **Conversão de Formato de Áudio Real:** O sistema agora utiliza as bibliotecas `pydub` e `ffmpeg` para realizar uma conversão real dos ficheiros de áudio para os formatos solicitados (`opus`, `aac`, `flac`, etc.), em vez de apenas renomear o ficheiro `mp3`. Isso garante a máxima compatibilidade.
* **Atualização da Documentação:** Todos os ficheiros (`README.md`, guias, etc.) foram completamente reescritos para refletir as novas funcionalidades da versão 2.0.0, incluindo as novas logos e instruções de configuração.
* **Dependência Adicionada:** A biblioteca `pydub` foi adicionada ao `requirements.txt`.

### 以前のバージョン (Versões Anteriores)

* As versões anteriores (série 1.x) estabeleceram a base do projeto com compatibilidade com a API da OpenAI, estabilidade e configuração via `.env`.
