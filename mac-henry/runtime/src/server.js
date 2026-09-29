import http from 'node:http';
import crypto from 'node:crypto';
import { decidePolicy } from './policy.js';

const PORT = Number(process.env.PORT || 8787);
const OWNER_TOKEN = process.env.MAC_HENRY_OWNER_TOKEN || '';
const MAX_BODY = 64 * 1024;
const seenIdempotency = new Map();

function send(res, status, body, extraHeaders = {}) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'cache-control': 'no-store',
    'x-content-type-options': 'nosniff',
    'referrer-policy': 'no-referrer',
    'content-security-policy': "default-src 'none'; frame-ancestors 'none'",
    ...extraHeaders
  });
  res.end(payload);
}

function authenticated(req) {
  if (!OWNER_TOKEN) return false;
  const header = req.headers.authorization || '';
  if (!header.startsWith('Bearer ')) return false;
  const supplied = Buffer.from(header.slice(7));
  const expected = Buffer.from(OWNER_TOKEN);
  return supplied.length === expected.length && crypto.timingSafeEqual(supplied, expected);
}

async function readJson(req) {
  let size = 0, raw = '';
  for await (const chunk of req) {
    size += chunk.length;
    if (size > MAX_BODY) throw new Error('BODY_TOO_LARGE');
    raw += chunk;
  }
  return JSON.parse(raw || '{}');
}

function validateCommand(c) {
  const required = ['command_id','correlation_id','idempotency_key','actor','lane','action_class','connector_id','target','intent','impact'];
  return required.every(k => typeof c?.[k] === 'string' && c[k].trim());
}

function auditEnvelope(command, policy, status, resultSummary, error = null) {
  return {
    execution_id: `MHE-${crypto.randomUUID()}`,
    correlation_id: command?.correlation_id || null,
    status,
    policy_decision: policy?.decision || 'DENY',
    result_summary: resultSummary,
    evidence_ref: null,
    rollback_ref: null,
    error,
    timestamp: new Date().toISOString()
  };
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/health') {
    return send(res, 200, { service: 'mac-henry-private-runtime', status: 'building', secrets_exposed: false });
  }

  if (!authenticated(req)) {
    return send(res, 401, { error: 'UNAUTHORIZED' }, { 'www-authenticate': 'Bearer' });
  }

  if (req.method === 'POST' && req.url === '/v1/execute') {
    try {
      const command = await readJson(req);
      if (!validateCommand(command)) return send(res, 400, { error: 'INVALID_COMMAND' });

      if (seenIdempotency.has(command.idempotency_key)) {
        return send(res, 200, seenIdempotency.get(command.idempotency_key));
      }

      const policy = decidePolicy(command);
      if (policy.decision === 'DENY') {
        const result = auditEnvelope(command, policy, 'DENIED', policy.reason);
        seenIdempotency.set(command.idempotency_key, result);
        return send(res, 403, result);
      }

      if (policy.decision === 'REQUIRE_APPROVAL' && !command.owner_approval_ref) {
        const result = auditEnvelope(command, policy, 'DENIED', 'Fresh Owner approval is required before execution.');
        return send(res, 409, result);
      }

      // v1 deliberately implements no privileged external connector execution yet.
      // The first connector will be a scoped, read-only private operations adapter.
      const result = auditEnvelope(command, policy, 'FAILED', 'Validated by runtime; connector adapter not installed.', 'CONNECTOR_NOT_IMPLEMENTED');
      seenIdempotency.set(command.idempotency_key, result);
      return send(res, 501, result);
    } catch (err) {
      const code = err?.message === 'BODY_TOO_LARGE' ? 413 : 400;
      return send(res, code, { error: err?.message || 'BAD_REQUEST' });
    }
  }

  return send(res, 404, { error: 'NOT_FOUND' });
});

server.listen(PORT, () => {
  console.log(`Mac Henry private runtime listening on ${PORT}`);
});
