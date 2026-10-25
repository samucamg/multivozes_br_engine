const ROUTES = new Map([
  ["/health", "GET"],
  ["/v1/models", "GET"],
  ["/voices", "GET"],
  ["/v1/voices", "GET"],
  ["/v1/audio/voices", "GET"],
  ["/v1/audio/speech", "POST"],
]);
const MAX_BODY_BYTES = 65536;

function error(status, message) {
  return Response.json({ detail: message }, { status, headers: { "Cache-Control": "no-store" } });
}

export default {
  async fetch(request, env) {
    if (!env.PROXY_API_KEY || !env.ORIGIN_API_KEY) return error(503, "Proxy não configurado.");
    if (request.headers.get("Authorization") !== `Bearer ${env.PROXY_API_KEY}`) {
      return error(401, "Chave de API inválida ou ausente.");
    }
    const incoming = new URL(request.url);
    const method = ROUTES.get(incoming.pathname);
    if (!method) return error(404, "Rota não encontrada.");
    if (request.method !== method) return error(405, "Método não permitido.");
    let origin;
    try {
      origin = new URL(env.ORIGIN_URL);
      if (origin.protocol !== "https:" || origin.username || origin.password ||
          origin.pathname !== "/" || origin.search || origin.hash || origin.host === incoming.host) {
        return error(503, "Origem inválida: configure uma origem HTTPS dedicada, sem caminho.");
      }
    } catch { return error(503, "Origem inválida."); }
    let body;
    if (method === "POST") {
      if (Number(request.headers.get("Content-Length")) > MAX_BODY_BYTES) return error(413, "Corpo excede 64 KiB.");
      if (request.headers.get("Content-Type")?.split(";")[0].trim().toLowerCase() !== "application/json") {
        return error(415, "Use Content-Type: application/json.");
      }
      // Limite real mesmo para uploads sem Content-Length.
      const reader = request.body?.getReader();
      const chunks = [];
      let size = 0;
      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          size += value.byteLength;
          if (size > MAX_BODY_BYTES) {
            await reader.cancel();
            return error(413, "Corpo excede 64 KiB.");
          }
          chunks.push(value);
        }
      }
      body = new Uint8Array(size);
      let offset = 0;
      for (const chunk of chunks) { body.set(chunk, offset); offset += chunk.byteLength; }
    }
    const target = new URL(incoming.pathname + incoming.search, origin);
    const headers = new Headers({ Authorization: `Bearer ${env.ORIGIN_API_KEY}` });
    if (body) headers.set("Content-Type", "application/json");
    const configuredTimeout = Number(env.ORIGIN_TIMEOUT_MS || 120000);
    const timeout = Number.isFinite(configuredTimeout) && configuredTimeout > 0
      ? Math.min(configuredTimeout, 300000) : 120000;
    let response;
    try {
      response = await fetch(target, {
        method, headers, body, redirect: "manual", signal: AbortSignal.timeout(timeout),
        cf: { cacheTtl: 0, cacheEverything: false },
      });
    } catch (cause) {
      return error(cause.name === "TimeoutError" || cause.name === "AbortError" ? 504 : 502,
        "Não foi possível obter resposta do servidor de voz.");
    }
    // Nunca siga redirects com o segredo do backend nem revele sua URL ao cliente.
    if (response.status >= 300 && response.status < 400) return error(502, "A origem respondeu com redirecionamento.");
    const output = new Headers(response.headers);
    output.set("Cache-Control", "no-store");
    output.delete("Set-Cookie");
    output.delete("Server");
    output.delete("Location");
    return new Response(response.body, { status: response.status, headers: output });
  },
};
