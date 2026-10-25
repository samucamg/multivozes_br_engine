# Guia da API

Compatibilidade com o endpoint de geração de fala da OpenAI. Não fornece chat, transcrição, clonagem de voz ou toda a API OpenAI. `tts-1` e `tts-1-hd` usam o mesmo motor Edge.

## Rotas

| Método e rota | Autenticação no backend | Resultado |
| --- | --- | --- |
| `GET /health` | Pública | Saúde do processo, sem testar Edge |
| `GET /v1/models` | Pública | Modelos de compatibilidade |
| `GET /v1/audio/voices` | Bearer | Catálogo Edge atual em `data` |
| `POST /v1/audio/speech` | Bearer | Arquivo binário de áudio |

`/voices` e `/v1/voices` são aliases do catálogo. `/docs` contém a documentação interativa local. O Worker exige autenticação também em saúde/modelos e não expõe `/docs`.

Catálogo: `?locale=pt-BR` filtra a localidade; `?locale=pt` inclui variantes de português; `?multilingual=true` filtra vozes cujo nome contém MultilingualNeural. Sem filtros, lista todas. A consulta usa o serviço Edge, sem cache persistente.

## JSON de geração

| Campo | Regra |
| --- | --- |
| `input` | Texto obrigatório; limite padrão 10000 caracteres |
| `model` | Opcional e ignorado, preservando compatibilidade anterior. Nomes como `tts-1`, `tts-1-hd`, `gpt-4o-mini-tts` e `tts-1-1106` usam o mesmo motor Edge; isso não disponibiliza modelos OpenAI reais |
| `voice` | Apelido de `voices.json` ou ShortName exato do catálogo; padrão do `.env` |
| `response_format` | `mp3` (padrão), `opus`, `aac`, `flac`, `wav`, `pcm` |
| `speed` | 0.25 a 2.0; padrão 1.0 |

MP3 é recebido do Edge. Outros formatos exigem FFmpeg. Opus usa contêiner Ogg, AAC usa ADTS e PCM é áudio bruto **signed 16-bit little-endian, mono, 24000 Hz**, sem cabeçalho WAV. Converter em FLAC/WAV não recupera informação perdida no MP3 original.

## Bash/curl

```sh
curl --fail-with-body http://localhost:5050/v1/audio/speech \
  -H 'Authorization: Bearer SUA_CHAVE' \
  -H 'Content-Type: application/json' \
  -d '{"model":"tts-1","input":"Olá. Hello!","voice":"pt-BR-ThalitaMultilingualNeural","response_format":"mp3","speed":1.0}' \
  --output fala.mp3
```

Se o comando falhar, o arquivo de saída pode conter JSON de erro; confira o status antes de tratá-lo como áudio.

## Windows PowerShell

```powershell
$headers = @{ Authorization = 'Bearer SUA_CHAVE' }
$payload = @{
    model = 'tts-1'
    input = 'Olá. Hello!'
    voice = 'pt-BR-ThalitaMultilingualNeural'
    response_format = 'mp3'
} | ConvertTo-Json
Invoke-WebRequest -Uri 'http://localhost:5050/v1/audio/speech' -Method Post `
    -Headers $headers -ContentType 'application/json; charset=utf-8' `
    -Body ([System.Text.Encoding]::UTF8.GetBytes($payload)) -OutFile 'fala.mp3'
```

## Python sem bibliotecas adicionais

```python
import json
import os
from urllib.request import Request, urlopen

payload = json.dumps({"input": "Olá!", "voice": "alloy"}).encode("utf-8")
request = Request(
    "http://localhost:5050/v1/audio/speech",
    data=payload,
    headers={"Authorization": "Bearer " + os.environ["MULTIVOZES_API_KEY"],
             "Content-Type": "application/json"},
)
with urlopen(request, timeout=120) as response:
    with open("fala.mp3", "wb") as output:
        output.write(response.read())
```

Defina `MULTIVOZES_API_KEY` no ambiente do cliente; não inclua a chave no código compartilhado. No SDK OpenAI, use `base_url='http://localhost:5050/v1'`, sua chave local e a operação `audio.speech.create`. O campo `model` não seleciona outro provedor ou qualidade: a síntese sempre usa Edge TTS.

## Erros e limites

- `400`: JSON/campo/voz/formato/velocidade inválido.
- `401`: chave ausente/incorreta.
- `413`: texto/corpo excede limite (backend 128 KiB de JSON; Worker 64 KiB).
- `502`: falha no Edge ou na conversão; confira catálogo, rede e FFmpeg.
- `503`: chave do servidor não configurada ou concorrência esgotada; respeite `Retry-After` quando presente.
- `504`: síntese/consulta excedeu o timeout.

Tempo de síntese padrão: 90 segundos; concorrência máxima padrão: quatro gerações por processo. O limite não é uma fila persistente. Ajuste timeout do cliente/proxy acima do backend e use repetição limitada com espera para falhas transitórias. Não repita automaticamente erros 400/401. Para aplicações web, configure CORS conscientemente na infraestrutura: este projeto não libera origens arbitrárias por padrão.
