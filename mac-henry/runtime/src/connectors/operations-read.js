const ALLOWED_FIELDS = new Set(['operation_id','command','lane','state','priority','risk','system','updated']);

function pickAllowed(record = {}) {
  return Object.fromEntries(Object.entries(record).filter(([key]) => ALLOWED_FIELDS.has(key)));
}

export async function readOperation(target) {
  const base = process.env.MAC_HENRY_OPERATIONS_READ_URL || '';
  const token = process.env.MAC_HENRY_OPERATIONS_READ_TOKEN || '';
  if (!base || !token) {
    return { ok: false, code: 'CONNECTOR_NOT_CONFIGURED', summary: 'Read-only operations connector is installed but has no private endpoint configuration.' };
  }

  const url = new URL('/v1/operations/read', base);
  url.searchParams.set('target', target);
  const response = await fetch(url, {
    method: 'GET',
    headers: { authorization: `Bearer ${token}`, accept: 'application/json' },
    redirect: 'error',
    signal: AbortSignal.timeout(5000)
  });

  if (!response.ok) {
    return { ok: false, code: `UPSTREAM_${response.status}`, summary: 'Private operations read failed.' };
  }
  const data = await response.json();
  return { ok: true, record: pickAllowed(data), evidence_ref: data.evidence_ref || null };
}
