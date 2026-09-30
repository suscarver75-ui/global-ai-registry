#!/usr/bin/env python3
from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parent/'recovery-gate.py'; s=importlib.util.spec_from_file_location('recovery',P); r=importlib.util.module_from_spec(s); s.loader.exec_module(r)
L1={'public_boundary','fail_closed_policy'}
L2=L1|{'preview_evidence','idempotency','replay_protection','state_precondition','command_receipt_binding','receipt_chain_integrity','post_change_verification','rollback_verified','independent_readback'}
L3=L2|{'rate_limit','operation_budget','circuit_breaker','audit_retention_verified'}
cases=[
 ('rollback succeeds only with independent readback',r.rollback('sha256:before','sha256:changed','sha256:before','sha256:before'),'ROLLBACK_VERIFIED'),
 ('rollback write failure denied',r.rollback('sha256:before','sha256:changed','sha256:wrong','sha256:before'),'ROLLBACK_FAILED'),
 ('rollback readback mismatch denied',r.rollback('sha256:before','sha256:changed','sha256:before','sha256:wrong'),'ROLLBACK_READBACK_FAILED'),
 ('no change needs no rollback',r.rollback('sha256:same','sha256:same','sha256:same','sha256:same'),'ROLLBACK_NOT_NEEDED'),
 ('L0 to L1 with evidence eligible',r.promote('L0_OBSERVE','L1_PREVIEW',L1),'PROMOTION_ELIGIBLE'),
 ('cannot skip L1',r.promote('L0_OBSERVE','L2_CONTROLLED_MUTATION',L2,True),'DENY_SKIP_LEVEL'),
 ('L2 denied without human approval',r.promote('L1_PREVIEW','L2_CONTROLLED_MUTATION',L2,False),'DENY_HUMAN_APPROVAL'),
 ('L2 eligible with evidence and approval',r.promote('L1_PREVIEW','L2_CONTROLLED_MUTATION',L2,True),'PROMOTION_ELIGIBLE'),
 ('L3 denied when audit evidence missing',r.promote('L2_CONTROLLED_MUTATION','L3_BOUNDED_AUTOMATION',L3-{'audit_retention_verified'},True),'DENY_MISSING_EVIDENCE:audit_retention_verified'),
 ('L3 eligible only when all evidence and approval exist',r.promote('L2_CONTROLLED_MUTATION','L3_BOUNDED_AUTOMATION',L3,True),'PROMOTION_ELIGIBLE')]
failed=0
for name,got,expected in cases:
 ok=got==expected; failed+=not ok; print(('PASS' if ok else 'FAIL')+f' | {name} | expected={expected} got={got}')
print(f'SUMMARY | {len(cases)-failed}/{len(cases)} passed'); raise SystemExit(1 if failed else 0)
