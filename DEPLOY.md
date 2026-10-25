# Deploy auto-hospedado e proxy opcional

## Arquitetura recomendada

```text
Cliente/n8n → acesso local ou proxy HTTPS → servidor próprio: Python + Edge TTS + FFmpeg
```

O produto principal é **auto-hospedado**, com Docker ou instalação Python. Cloudflare não é uma dependência de execução: pode-se acessar pela rede local ou usar um proxy HTTPS próprio, como Nginx, Caddy ou Traefik. O serviço continua dependendo de acesso ao Edge TTS para sintetizar novos áudios.

**Se optar pela Cloudflare**, o caminho mais simples para um servidor próprio é Tunnel nomeado + autenticação Bearer. O conector `cloudflared` inicia conexões de saída; não é necessário publicar a porta 5050 na Internet. O servidor precisa continuar ligado e com saída para Cloudflare e Microsoft. Tunnel transporta as requisições; não hospeda nem acelera a síntese.

| Opção | Quando usar |
| --- | --- |
| Tunnel + chave do motor | Caminho inicial mais simples para clientes que enviam Bearer, com origem sem porta pública |
| Tunnel + Access Service Auth + chave do motor | Integrações controladas que conseguem enviar também as credenciais de serviço do Access |
| Worker → Tunnel → motor | Quando precisar trocar a chave do cliente pela da origem ou acrescentar regras no proxy |
| Worker → origem HTTPS existente | Quando a origem já possui HTTPS; um Worker isoladamente não fecha portas nem torna a origem privada |

O Worker incluído é um **proxy reverso opcional**. O motor continua hospedado em uma VPS, servidor local acessível via Tunnel ou plataforma que execute o Dockerfile. O repositório não contém uma versão do motor capaz de rodar integralmente no runtime Workers.

Python Workers usa Pyodide/WebAssembly e pacotes compatíveis. Isso não equivale a executar este servidor CPython com FFmpeg nativo e subprocessos. Rodar o Dockerfile exige um host de contêineres; Cloudflare Containers é um produto separado, não é habilitado pelo proxy incluído e não foi validado nesta revisão. Não há promessa de hospedagem gratuita, SLA ou disponibilidade do provedor de voz.

### Tunnel não é a política de autenticação

Um hostname público via Tunnel ainda permite requisições da Internet. A chave Bearer do aplicativo deve continuar habilitada. **Access** é a camada adicional de identidade/autorização do Cloudflare Zero Trust; configure-a separadamente se desejar acesso restrito.

Para n8n/serviços automáticos, use política **Service Auth**, com `CF-Access-Client-Id` e `CF-Access-Client-Secret`, além do Bearer da API. O nó HTTP Request pode enviar os cabeçalhos; confirme se o cliente OpenAI utilizado permite cabeçalhos adicionais. Uma tela de login de navegador não serve como autenticação automática de uma API.

O Worker atual **não envia as credenciais Service Auth**. Apontá-lo para uma origem protegida por Access exige acrescentar esses dois segredos e cabeçalhos ao proxy e testar a integração. A arquitetura Worker → Access → Tunnel é uma possibilidade futura, não uma configuração pronta no código entregue.

Para uma API acessível somente numa rede privada, Tunnel com acesso privado por cliente Cloudflare One/WARP também é uma alternativa; exige configurar essa conectividade nos consumidores, e difere de publicar um hostname HTTPS acessível por qualquer integração externa.

### Tempo de geração e filas

O backend usa timeout de **90 segundos**. O Worker entregue usa **120 segundos** por configuração própria. A documentação Cloudflare consultada em 25/10/2026 informa Proxy Read Timeout padrão de **125 segundos**; limites do plano e de cada etapa devem ser conferidos na instalação real. Aumentar o timeout do Worker não elimina um timeout na origem ou na conexão através do proxy.

O Worker HTTP não tem um prazo universal de poucos segundos de duração enquanto o cliente permanece conectado; limites de CPU e duração da conexão são medidas diferentes. A incompatibilidade deste motor com um Worker convencional é de ambiente de execução/dependências, não uma suposta proibição universal de esperar pelo TTS.

Para trabalhos demorados, a evolução recomendada é enviar um job e receber HTTP 202 rapidamente, consultar o estado e baixar o áudio ao concluir. Essa fila ainda é **proposta**, não foi implementada. O endpoint `/v1/audio/speech` deve continuar retornando áudio para preservar clientes atuais.

## 1. Hospedar o motor

**VPS:** siga a [instalação Docker do README](README.md#instalação-em-4-passos-recomendado-docker) ou [systemd](BEGINNERS_GUIDE.md#início-automático-com-systemd-linux). Mantenha `REQUIRE_API_KEY=True`. Exponha a origem por HTTPS com certificado válido.

**Plataforma de contêineres:** selecione este repositório/Dockerfile, configure `API_KEY`, `REQUIRE_API_KEY=True` e a porta interna 5050. O processo também respeita `PORT` fornecido pela plataforma. Configure `/health` como healthcheck. O host precisa permitir saída HTTPS/WebSocket para Microsoft e espaço temporário gravável. Não há dependência de disco persistente para áudios; eles são temporários e removidos após a resposta.

**Servidor em casa ou porta privada:** use um Cloudflare Tunnel nomeado com hostname HTTPS, direcionado a `http://localhost:5050`. O processo `cloudflared` deve estar no mesmo host; dentro de Docker, `localhost` se refere ao próprio contêiner, portanto use uma rede Docker compartilhada e o hostname do serviço. Configure o Tunnel pelo painel Cloudflare Zero Trust conforme a [documentação oficial](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/get-started/). Mantenha a chave do backend; não publique o token do Tunnel no Git.

Teste a origem primeiro: `/health`, autenticação e geração real de um MP3. Não configure o Worker apontando para ele mesmo, nem para um hostname que encaminha de volta ao Worker.

## 2. Configurar o Worker

Requer conta Cloudflare e **Node.js 22+**, compatível com o Wrangler fixado neste projeto.

```sh
cd workers
npm ci
```

Edite `wrangler.jsonc`:

- `name`: nome do Worker.
- `ORIGIN_URL`: origem HTTPS dedicada, como `https://tts-origin.seudominio.com`, **sem caminho, query, usuário ou senha**.
- `ORIGIN_TIMEOUT_MS`: espera pela resposta da origem, padrão 120000 ms. Mantenha acima de `TTS_TIMEOUT_SECONDS` do motor; o proxy limita a configuração a 300000 ms. O backend precisa completar a síntese antes de começar a resposta.

Configure os segredos pelos prompts, sem gravá-los em `wrangler.jsonc`:

```sh
npx wrangler login
npx wrangler secret put ORIGIN_API_KEY
npx wrangler secret put PROXY_API_KEY
npm run check
npm run deploy
```

`ORIGIN_API_KEY` é a `API_KEY` do motor. `PROXY_API_KEY` é uma chave diferente que você entrega aos clientes. O proxy exige essa chave em **todas as rotas**, inclusive `/health`; substitui o token antes de chamar a origem. O CLI pode oferecer criar o Worker ao adicionar o primeiro segredo: confirme a criação do recurso quando desejar publicar. `npm run check` apenas empacota; não publica.

Após deploy, use a URL HTTPS retornada pelo Wrangler. Em clientes OpenAI/n8n, Base URL: `https://SEU_WORKER.workers.dev/v1`; chave: `PROXY_API_KEY`. Para domínio próprio, use a configuração de Custom Domains no painel Workers. Mantenha origem e Worker em hostnames diferentes.

## 3. Teste após publicação

```sh
curl --fail-with-body https://SEU_WORKER.workers.dev/health \
  -H 'Authorization: Bearer CHAVE_DO_PROXY'
curl --fail-with-body 'https://SEU_WORKER.workers.dev/v1/audio/voices?multilingual=true' \
  -H 'Authorization: Bearer CHAVE_DO_PROXY'
```

Faça também a chamada de áudio do [guia da API](API_USAGE_GUIDE.md), trocando a URL e chave. O teste real publicado depende de sua conta/domínio e não é executado pelo instalador.

## Desenvolvimento local do Worker

Copie `workers/.dev.vars.example` para `workers/.dev.vars` e preencha os dois segredos. Use uma origem HTTPS real de teste; o proxy rejeita origens HTTP, inclusive localhost.

```sh
cd workers
npm run dev
```

O Wrangler informa a URL local. `/docs` não é exposto pelo proxy: a documentação interativa fica na origem/local. O Worker libera somente GET `/health`, `/v1/models`, `/v1/audio/voices` (aliases `/v1/voices`, `/voices`) e POST `/v1/audio/speech`.

## Limites e proteção

O proxy limita JSON a **64 KiB**, exige `application/json`, bloqueia outros métodos/rotas, não segue redirects da origem e não faz cache de texto ou áudio. A resposta binária é repassada como stream, sem carregar o áudio inteiro no Worker. Isso não muda a geração completa de arquivo no backend. O backend também aplica seus limites de caracteres, concorrência e timeout. Uploads do cliente não têm um timeout de aplicação separado; aplicam-se os limites da plataforma.

Não há rate limit por usuário, contabilidade, fila, CORS para aplicações web ou armazenamento de áudios no proxy. Para tráfego público, configure limites/rate limiting/WAF adequados à sua conta e carga. O proxy não impede acesso direto à origem por quem tiver a chave do backend; mantenha-a privada e, quando necessário, restrinja a origem com sua infraestrutura. Se usar Cloudflare Access, será necessário adaptar o proxy para enviar credenciais de serviço; este exemplo envia apenas o Bearer do motor.

O código deixa observabilidade do Worker desligada por padrão e não registra texto/chaves. Confira também políticas de logs da origem e plataforma. Limites e custos de Workers/Tunnel/host dependem do plano e devem ser conferidos antes de produção.

## Atualizar e reverter

Guarde o commit/imagem anterior e uma cópia privada de configurações. Backend: faça rebuild e reinicie, testando um MP3 e um formato convertido. Worker: `npm ci`, `npm run check`, `npm run deploy`. `npm run check` valida o pacote sem publicar; testes automatizados não acompanham este repositório. Após publicar, confira autenticação, catálogo e geração real de áudio. Para reverter o Worker, use a versão anterior em Workers → Deployments; para o backend, volte à imagem/commit anterior e reinstale as dependências correspondentes. Nunca reverta a chave por uma chave de exemplo pública.

## Referências consultadas

- [Cloudflare Tunnel](https://developers.cloudflare.com/tunnel/)
- [Access Service Tokens](https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/)
- [Limites de conexão e Proxy Read Timeout](https://developers.cloudflare.com/fundamentals/reference/connection-limits/)
- [Erro 524 e consulta periódica de estado](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-524/)
- [Cloudflare Containers, produto distinto](https://developers.cloudflare.com/containers/)
- [Como Python Workers funciona](https://developers.cloudflare.com/workers/languages/python/how-python-workers-work/)
- [Pacotes Python suportados](https://developers.cloudflare.com/workers/languages/python/packages/)
- [Streams e respostas](https://developers.cloudflare.com/workers/runtime-apis/streams/)
- [Requests e redirects](https://developers.cloudflare.com/workers/runtime-apis/request/)
- [Segredos do Wrangler](https://developers.cloudflare.com/workers/configuration/secrets/)
- [Limites de Workers](https://developers.cloudflare.com/workers/platform/limits/)
