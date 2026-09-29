# Mac Henry — Private Runtime v1

Status: BUILDING — specification and runtime contract only. This directory contains no secrets and is not itself the private runtime.

## Purpose
Create the authenticated execution boundary between the Owner, Mac Henry, private operations state, and approved connectors.

## Runtime pipeline
1. Authenticate Owner session.
2. Accept a structured command.
3. Assign correlation ID + idempotency key.
4. Validate command schema and target.
5. Resolve principal permissions and connector scope.
6. Run policy/preflight decision: ALLOW / REQUIRE_APPROVAL / DENY.
7. Require fresh Owner approval for consequential actions.
8. Execute only through server-side scoped connector credentials.
9. Run postflight verification.
10. Write result, evidence reference, errors and rollback/compensating action to the execution ledger.
11. Mark VERIFIED only after evidence proves the intended result.

## Deny-by-default rules
- No unauthenticated private commands.
- No secrets in browser code, GitHub Pages, prompts, Notion ledgers, logs or evidence records.
- No independent money movement, contract acceptance, credential mutation or destructive production deletion.
- No action outside connector scope.
- No retry of consequential actions without idempotency protection.
- No VERIFIED state without result evidence.

## Minimum private host requirements
- TLS/HTTPS.
- Server-side session handling with secure, HttpOnly, SameSite cookies or equivalent.
- MFA/step-up authentication for critical actions.
- Encrypted secret manager/environment injection; never expose raw secrets to the client.
- CSRF protection for browser state-changing requests.
- Rate limiting and abuse controls.
- Durable audit/event storage.
- Explicit connector allowlist and least-privilege scopes.
- Credential rotation/revocation path.
- Backup/recovery plan.
- Health endpoint that exposes no sensitive data.

## Command contract
```json
{
  "command_id": "uuid",
  "correlation_id": "uuid",
  "idempotency_key": "opaque-unique-value",
  "actor": "owner|mac-henry",
  "lane": "CONTROL|MONEY|BUILD|CONTENT|RESEARCH|SECURITY|PUBLIC",
  "action_class": "READ|WRITE|PUBLISH|DELETE|MONEY|CONTRACT|CREDENTIAL|SECURITY",
  "connector_id": "MHC-...",
  "target": "named-resource",
  "intent": "plain-language requested outcome",
  "impact": "LOW|MEDIUM|HIGH|CRITICAL",
  "owner_approval_ref": null
}
```

## Result contract
```json
{
  "execution_id": "MHE-...",
  "status": "SUCCEEDED|FAILED|DENIED",
  "policy_decision": "ALLOW|REQUIRE_APPROVAL|DENY",
  "result_summary": "non-secret result",
  "evidence_ref": "reference-only",
  "rollback_ref": "reference-only-or-null",
  "error": null
}
```

## First verification target
The first end-to-end runtime test must be harmless and reversible: authenticated Owner session -> READ an approved Mac Henry operational record -> policy ALLOW -> return the record -> create an execution/audit entry -> verify the returned evidence. No money, publishing, credential or destructive action is permitted for the first test.

## Public/private boundary
This repository documents the contract and may contain non-secret client assets. Authentication logic, secret material, private operational data and privileged connector execution belong only in the future authenticated server-side runtime.
