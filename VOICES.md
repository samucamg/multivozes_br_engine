# Vozes do Multivozes BR Engine

A fonte de verdade é o catálogo **do Microsoft Edge**, consultado ao vivo. O catálogo do Azure Speech é diferente: uma voz anunciada no Azure não se torna automaticamente utilizável por `edge-tts`.

## Resultado verificado em 25/10/2026

Com `edge-tts==7.3.1`, foram retornadas **322 vozes**, das quais **12** contêm `MultilingualNeural` no nome. Não encontramos outras vozes multilíngues no catálogo consultado. O adaptador agora oferece **13 aliases OpenAI**, com alguns destinos repetidos para manter os perfis escolhidos usando somente vozes multilíngues.

Além de consultar o catálogo, geramos um MP3 não vazio com cada uma dessas 12 vozes usando o texto: “Olá! Este é um teste de voz em português do Brasil.” Isso confirma a síntese nessa consulta, sem avaliação auditiva de sotaque ou qualidade e sem garantir disponibilidade futura.

## Aliases e vozes multilíngues

O parâmetro `voice` aceita o alias ou o nome técnico completo. Os aliases abaixo são os valores reais de [voices.json](voices.json), personalizáveis sem alterar o código. **Todos os destinos dos aliases são `MultilingualNeural`**. Reinicie a API depois de editar esse arquivo.

O carregamento rejeita destinos não multilíngues para os 13 aliases OpenAI. Se `voices.json` estiver ausente, os 13 padrões multilíngues de `config.py` são usados. Apelidos próprios, como `narrador`, e nomes técnicos diretos podem continuar usando vozes regionais.

| Alias | Nome técnico | Gênero | Localidade principal |
| --- | --- | --- | --- |
| `alloy` | `pt-BR-ThalitaMultilingualNeural` | Feminino | Brasil |
| `ash` | `en-US-AndrewMultilingualNeural` | Masculino | EUA |
| `ballad` | `en-US-BrianMultilingualNeural` | Masculino | EUA |
| `cedar` | `en-AU-WilliamMultilingualNeural` | Masculino | Austrália |
| `coral` | `en-US-AvaMultilingualNeural` | Feminino | EUA |
| `echo` | `it-IT-GiuseppeMultilingualNeural` | Masculino | Itália |
| `fable` | `it-IT-GiuseppeMultilingualNeural` | Masculino | Itália |
| `marin` | `en-US-EmmaMultilingualNeural` | Feminino | EUA |
| `onyx` | `fr-FR-RemyMultilingualNeural` | Masculino | França |
| `nova` | `de-DE-SeraphinaMultilingualNeural` | Feminino | Alemanha |
| `sage` | `fr-FR-VivienneMultilingualNeural` | Feminino | França |
| `shimmer` | `en-US-EmmaMultilingualNeural` | Feminino | EUA |
| `verse` | `ko-KR-HyunsuMultilingualNeural` | Masculino | Coreia do Sul |

O prefixo indica a localidade principal, não limita uma voz multilíngue àquele idioma. A síntese usa o texto recebido; ela não traduz. Envie texto em português para produzir fala em português. Textos com idiomas misturados precisam ser testados com as vozes e os termos usados na sua aplicação.

### Critério de aproximação com os nomes OpenAI

A lista de 13 nomes vem da [documentação OpenAI](https://developers.openai.com/api/docs/guides/text-to-speech). A coluna gênero acima descreve o metadado `Gender` **do Edge**, conferido no catálogo; não é uma classificação oficial das vozes OpenAI.

A seleção local busca uma aproximação de perfil vocal: masculino para `ash`, `ballad`, `cedar`, `echo`, `fable`, `onyx` e `verse`; feminino para `coral`, `marin`, `nova`, `sage` e `shimmer`. Esses perfis são uma decisão editorial do projeto. Para priorizar coerência de gênero, `fable` passou de Emma para Giuseppe e `shimmer` passou de Florian para Emma. `marin` foi incluída com Emma. Os demais destinos foram preservados, incluindo `alloy` com Thalita para manter o padrão brasileiro; não afirmamos uma equivalência neutra para `alloy`.

Não foi feita comparação auditiva entre as vozes OpenAI e Edge, nem medição de semelhança de timbre. O gênero compatível é um primeiro critério de aproximação, sem garantia de equivalência sonora. Não há uma correspondência oficial entre os dois fornecedores; nomes, sotaques e entonação podem soar diferentes. Os aliases não reproduzem as vozes comerciais da OpenAI. Ajuste a escolha depois de ouvir amostras no idioma utilizado.

Destinos repetidos são intencionais: `echo` e `fable` usam Giuseppe; `marin` e `shimmer` usam Emma. O catálogo também mantém `de-DE-FlorianMultilingualNeural`, utilizável pelo nome técnico, embora ele não seja mais destino de `shimmer`. As vozes regionais listadas adiante continuam disponíveis pelo nome completo; elas não são usadas para mapear aliases OpenAI.

Mudanças futuras do catálogo exigem nova consulta (`python voices_catalog.py --check-aliases`); presença no catálogo não prova disponibilidade remota permanente.

## Português

| Nome técnico | Gênero | Variante |
| --- | --- | --- |
| `pt-BR-ThalitaMultilingualNeural` | Feminino | Brasil, multilíngue, padrão do projeto |
| `pt-BR-AntonioNeural` | Masculino | Brasil |
| `pt-BR-FranciscaNeural` | Feminino | Brasil |
| `pt-PT-DuarteNeural` | Masculino | Portugal |
| `pt-PT-RaquelNeural` | Feminino | Portugal |

`pt-BR-ThalitaNeural` não apareceu no catálogo consultado; use o nome completo `pt-BR-ThalitaMultilingualNeural`.

## Descobrir e validar vozes

Na pasta do projeto, com o ambiente Python ativado:

```bash
python voices_catalog.py
python voices_catalog.py --locale pt
python voices_catalog.py --multilingual
python voices_catalog.py --locale pt-BR --json
python voices_catalog.py --check-aliases
```

`--check-aliases` consulta o catálogo completo e encerra com código 1 se algum alias estiver indisponível; código 2 indica falha ao consultar o serviço. A opção `--locale` filtra a localidade principal: por exemplo, `--locale pt` não inclui Andrew, mesmo que ele consiga falar português.

O utilitário lê `PROXY` do `.env`, se configurado, e limita cada consulta a 30 segundos. Ele não modifica o mapeamento e não gera áudio. Você também pode usar `edge-tts --list-voices` diretamente, passando `--proxy URL` quando necessário.

Pela API, use `GET /v1/audio/voices?locale=pt` ou `GET /v1/audio/voices?multilingual=true`, com o mesmo cabeçalho de autenticação da síntese. A resposta traz `data` com os metadados atuais das vozes.

## Testar uma voz antes de usá-la

```bash
edge-tts --voice pt-BR-ThalitaMultilingualNeural --text "Olá! Hello! Como você está?" --write-media teste.mp3
```

Ou envie à API:

```json
{
  "model": "tts-1",
  "voice": "pt-BR-ThalitaMultilingualNeural",
  "input": "Olá! Hello! Como você está?",
  "response_format": "mp3",
  "speed": 1.0
}
```

Presença no catálogo e geração de áudio são verificações distintas. Em caso de falha, teste primeiro uma frase curta com `pt-BR-FranciscaNeural`, confira a conexão/proxy e a versão instalada do `edge-tts`. Não substitua silenciosamente uma voz: isso altera o resultado esperado pelo usuário.

## Fontes

- [Projeto upstream e comando de listagem](https://github.com/rany2/edge-tts#changing-the-voice)
- [Implementação da consulta ao catálogo Edge](https://github.com/rany2/edge-tts/blob/master/src/edge_tts/voices.py)
- [Explicação do mantenedor sobre Edge e Azure](https://github.com/rany2/edge-tts/discussions/224)
- [Catálogo Azure Speech, referência separada](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)

Vozes `DragonHDLatestNeural` e outras novidades do Azure exigem confirmação no catálogo Edge para serem utilizadas por este projeto. A API atual não implementa um provedor Azure Speech autenticado.
