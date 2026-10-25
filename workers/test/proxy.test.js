import test from "node:test";
import assert from "node:assert/strict";
import worker from "../src/index.js";
const env = { PROXY_API_KEY: "client-key", ORIGIN_API_KEY: "backend-key", ORIGIN_URL: "https://origin.example.com" };
const request = (path = "/v1/audio/speech", options = {}) => new Request(`https://proxy.example.com${path}`, {
  method: "POST", headers: { Authorization: "Bearer client-key", "Content-Type": "application/json" },
  body: '{"input":"Olá"}', ...options,
});
test("rejects unauthenticated requests and missing secrets", async () => {
  assert.equal((await worker.fetch(request("/v1/audio/speech", { headers: {} }), env)).status, 401);
  assert.equal((await worker.fetch(request(), {})).status, 503);
});
test("rejects unknown routes, methods, untrusted origins and oversized bodies", async () => {
  assert.equal((await worker.fetch(request("/admin"), env)).status, 404);
  assert.equal((await worker.fetch(request("/health"), env)).status, 405);
  for (const ORIGIN_URL of ["http://origin.example.com", "https://proxy.example.com", "https://a:b@origin.example.com", "https://origin.example.com/prefix"]) {
    assert.equal((await worker.fetch(request(), { ...env, ORIGIN_URL })).status, 503);
  }
  assert.equal((await worker.fetch(request("/v1/audio/speech", { body: "a".repeat(65537) }), env)).status, 413);
  assert.equal((await worker.fetch(request("/v1/audio/speech", { headers: { Authorization: "Bearer client-key" } }), env)).status, 415);
});
test("streams binary audio, substitutes backend secret and forwards selected headers", async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async (target, options) => {
      assert.equal(target.href, "https://origin.example.com/v1/audio/speech?x=1");
      assert.equal(options.headers.get("Authorization"), "Bearer backend-key");
      assert.equal(options.headers.get("Cookie"), null);
      assert.equal(options.redirect, "manual");
      assert.equal(new TextDecoder().decode(options.body), '{"input":"Olá"}');
      return new Response(new Uint8Array([73, 68, 51, 255]), { headers: { "Content-Type": "audio/mpeg", "Set-Cookie": "secret=1" } });
    };
    const response = await worker.fetch(request("/v1/audio/speech?x=1"), env);
    assert.equal(response.headers.get("Content-Type"), "audio/mpeg");
    assert.equal(response.headers.get("Set-Cookie"), null);
    assert.equal(response.headers.get("Cache-Control"), "no-store");
    assert.deepEqual(new Uint8Array(await response.arrayBuffer()), new Uint8Array([73, 68, 51, 255]));
  } finally { globalThis.fetch = originalFetch; }
});
test("preserves upstream errors and blocks redirects, network failures and timeouts", async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async () => Response.json({ detail: "Voz inválida" }, { status: 400 });
    assert.equal((await worker.fetch(request(), env)).status, 400);
    globalThis.fetch = async () => new Response(null, { status: 302, headers: { Location: "https://elsewhere.example" } });
    assert.equal((await worker.fetch(request(), env)).status, 502);
    globalThis.fetch = async () => { throw new TypeError("network"); };
    assert.equal((await worker.fetch(request(), env)).status, 502);
    globalThis.fetch = async () => { throw new DOMException("timeout", "TimeoutError"); };
    assert.equal((await worker.fetch(request(), env)).status, 504);
  } finally { globalThis.fetch = originalFetch; }
});
test("GET voices preserves query and does not send a body", async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async (target, options) => {
      assert.equal(target.href, "https://origin.example.com/v1/audio/voices?locale=pt-BR");
      assert.equal(options.body, undefined);
      return Response.json([]);
    };
    const response = await worker.fetch(request("/v1/audio/voices?locale=pt-BR", { method: "GET", body: undefined }), env);
    assert.equal(response.status, 200);
  } finally { globalThis.fetch = originalFetch; }
});
