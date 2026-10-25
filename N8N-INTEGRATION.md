# Integração com n8n

Use a URL do motor ou do [Worker](DEPLOY.md), com sua respectiva chave. A compatibilidade cobre geração de fala; este serviço não implementa chat/transcrição. Os nomes das opções do n8n variam por versão.

## Nó OpenAI

Na credencial OpenAI, configure API Key com a chave do motor e Base URL terminando em `/v1`, por exemplo `https://voz.seudominio.com/v1`. Se usar o Worker, informe `PROXY_API_KEY`, não a chave da origem. Não informe Organization ID.

Selecione a operação de geração de áudio/fala, modelo `tts-1`, texto e um apelido (`alloy`, `echo`, etc.). O mapeamento atual é definido em [voices.json](voices.json); confira [VOICES.md](VOICES.md) em vez de manter outra tabela desatualizada. `tts-1-hd` usa o mesmo motor. Se a versão do nó exigir operações não implementadas ou não permitir Base URL personalizada, use HTTP Request.

## Nó HTTP Request (alternativa direta)

1. Method: `POST`.
2. URL: `http://HOST:5050/v1/audio/speech` ou sua URL HTTPS equivalente.
3. Authentication: credencial Header Auth, nome `Authorization`, valor `Bearer SUA_CHAVE`. Guarde a chave nas credenciais do n8n.
4. Body: JSON; Content-Type `application/json`.
5. JSON de exemplo:

```json
{
  "model": "tts-1",
  "input": "Olá! Seu áudio está pronto.",
  "voice": "pt-BR-ThalitaMultilingualNeural",
  "response_format": "mp3",
  "speed": 1.0
}
```

6. Response Format: **File**, saída binária com nome, por exemplo, `data`.
7. Timeout: acima de 90 segundos (por exemplo 120000 ms para acesso direto; 150000 ms pelo Worker com timeout de origem 120000).
8. Execute com texto curto e confira HTTP 200 e arquivo de áudio antes de enviá-lo ao próximo nó.

Para texto de outro nó, use a interface de expressões do n8n ao preencher `input`; evite concatenar JSON manualmente, pois aspas/quebras de linha podem invalidar o corpo. Limite o tamanho do texto antes da chamada.

## Rede Docker

`localhost` dentro do contêiner n8n aponta para o próprio n8n. Em uma rede Docker compartilhada, use o nome do serviço, como `http://multivozes:5050/v1`. Contêineres de projetos Compose separados não compartilham rede automaticamente. Outra opção é o endereço HTTPS do servidor/Worker.

Não use HTTP aberto na Internet para enviar credenciais ou texto de usuários. Mantenha retries limitados e respeite `Retry-After` para 503; 400/401 exigem corrigir a chamada. Consulte [API_USAGE_GUIDE.md](API_USAGE_GUIDE.md) para limites e formatos.
