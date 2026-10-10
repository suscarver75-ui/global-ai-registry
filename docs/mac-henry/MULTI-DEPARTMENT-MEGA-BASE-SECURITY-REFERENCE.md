# Mac Henry — Multi-Department MEGA BASE Security Reference
Date: 2026-10-10
Status: REFERENCE / NOT PRODUCTION CERTIFICATION
Classification: PUBLIC-SAFE ARCHITECTURE ONLY

## Authority and scope
Owner -> private Mac Henry Main Brain -> RUN orchestration + MEGA BASE trust layer -> independent site/department managers -> bounded assistants.
The global-ai-registry GitHub site contains multiple departments. Seven-Fold Church is ONE consumer/example, never the system-wide parent or default tenant. Church-specific policy and protected records must not become global defaults.

## Non-negotiable boundaries
- No private Main Brain content, credentials, member/support records, keys, production trust roots, or financial account data in this repository.
- Shared reusable *architecture* does not mean shared tenant identities, keys, encryption domains, permissions, data, worker privileges, or trust roots.
- Public/member chat is not a protected private-support data plane.
- Owner approvals are required for consequential actions; no assistant or worker may self-escalate.
- RUN authorizes/supervises; bounded background workers execute scoped jobs; MEGA BASE protects identity, authorization, data and receipts.
- Do not claim ACTIVE until tested, integrated, connected, E2E exercised, monitored and recovery-verified.

## Fifteen-layer control checklist
1. Edge/API shield: rate limits, request validation, SSRF/egress controls.
2. Identity/session: MFA/passkeys, session expiry, revocation, recovery.
3. Authorization/policy: deny by default, capabilities, purpose, approval gates.
4. Tenant/department isolation: explicit tenant+department scoping on every path.
5. Object ownership: enforce record-level owner/relationship access.
6. Data integrity: constraints, transactions, migrations, provenance.
7. Encryption/keys: encryption in transit/at rest, separate key scopes and rotation.
8. Secret vault: never commit secrets; usage inventory and least privilege.
9. Events/jobs: idempotency, signatures, leases, retries, quarantine and cancellation.
10. Audit/evidence: tamper-evident receipts, independently protected checkpoints.
11. Privacy/retention: consent, minimum-context, deletion and legal-hold separation.
12. Observability: safe telemetry, alerts, cost and anomaly monitoring.
13. Backup/restore: encrypted backups, restore drills and RPO/RTO evidence.
14. Safe mode/recovery: circuit breakers, containment, rollback and game days.
15. Sanitized manager health: minimum-data status only; never private payloads.

## Existing source anchors (reconcile; do not rebuild)
- mega-base/spec.json
- mega-base/rebuild-blueprint.json
- mega-base/core.py
- mega-base/runtime/service.py
- church/runtime/test-megabase-e2e.py
- .github/workflows/church-megabase-e2e.yml
- mac-henry/run-mac-henry.py
- henry/policy-engine.py

## Evidence gates
For each layer record: specification -> implementation -> local tests -> CI -> integration -> live connection -> E2E negative/positive tests -> monitoring/restore -> production verification.
Initial source review: core.py has in-memory tenant capability checks and hash-linked receipts; runtime/service.py has department-scoped service capability checks and database audit receipts. This does not demonstrate object ownership, real session/MFA, vault, private queues or live production operations.
Church E2E is a sample consumer test, not proof of cross-department isolation.

## Next implementation gate
Inventory actual departments, tenant IDs, record types, managers, public/private interfaces, and finance boundaries. Add generic tenant+department+object authorization with negative cross-tenant, cross-department, cross-object and worker escalation tests. Preserve compatibility and require Owner review before merging/deploying.

## Change log
2026-10-10: Corrected hierarchy; Church treated as one department/example; added reusable 15-layer security acceptance checklist. No production mutation or private data transfer.
