# Histórico de Versões (Changelog)

Todas as mudanças notáveis neste projeto serão documentadas neste ficheiro.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

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