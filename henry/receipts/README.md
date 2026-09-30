# Henry Evidence Receipts

Henry operations use evidence receipts rather than unverified success claims.

A receipt is public-safe operational evidence. It MUST NOT contain credentials, private Main Brain prompts/reasoning, wallet secrets, confidential records, or unnecessary personal information.

## Receipt lifecycle
1. RECEIVE — validate command envelope and contract version.
2. DECIDE — default DENY; allow only allowlisted action + public target.
3. PREVIEW — required before mutation.
4. EXECUTE — only after gates/preconditions remain satisfied.
5. VERIFY — inspect resulting public state.
6. RECEIPT — record decision, before/after references and verification result.
7. EVALUATE — controller decides whether the objective was actually achieved.

## Required properties
Receipts identify command/action/target, timestamps, decision, before and after state references, verification state, evidence references and error code where applicable. Receipts are not credentials and grant no authority.

## Failure semantics
A failed verification must remain failed. Do not rewrite evidence to manufacture success. Retry requires a new attempt/receipt linked to the prior result. Ambiguity fails closed.
