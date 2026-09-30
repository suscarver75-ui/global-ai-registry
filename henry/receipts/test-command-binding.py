#!/usr/bin/env python3
from pathlib import Path
import importlib.util,copy
P=Path(__file__).resolve().parent/'chain.py'; s=importlib.util.spec_from_file_location('chain',P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def cmd(cid,target='henry/health.json',payload=None): return {'command_id':cid,'contract_version':'henry.command-contract.v1','issued_at':'2026-09-30T05:00:00Z','expires_at':'2026-09-30T05:10:00Z','action':'VERIFY_PUBLIC_ARTIFACT','mode':'EXECUTE','target':target,'payload':payload or {},'expected_state':'sha256:before','idempotency_key':'idem-'+cid}
def rec(cid): return {'receipt_id':'R-'+cid,'command_id':cid,'contract_version':'henry.command-contract.v1','action':'VERIFY_PUBLIC_ARTIFACT','decision':'ALLOW_EXECUTE','target':'henry/health.json','started_at':'2026-09-30T05:01:00Z','completed_at':'2026-09-30T05:01:01Z','before_state_reference':'sha256:before','after_state_reference':'sha256:after','verification_status':'VERIFIED','evidence_references':['henry/health.json'],'error_code_if_any':None}
a=cmd('CMD-A'); b=cmd('CMD-B'); sealed=m.seal(rec('CMD-A'),command=a)
cases=[('correct command binding accepted',m.verify(sealed,command=a),True),('different command rejected',m.verify(sealed,command=b),False),('same id changed target rejected',m.verify(sealed,command=cmd('CMD-A','henry/capabilities.json')),False),('same id changed payload rejected',m.verify(sealed,command=cmd('CMD-A',payload={'changed':True})),False)]
forged=copy.deepcopy(sealed); forged['command_fingerprint']=m.command_fingerprint(b); cases.append(('fingerprint edit without reseal rejected',m.verify(forged,command=b),False))
try:
 m.seal(rec('CMD-A'),command=b); mismatch_rejected=False
except ValueError: mismatch_rejected=True
cases.append(('seal rejects mismatched command id',mismatch_rejected,True))
failed=0
for name,got,expected in cases:
 ok=got is expected; failed+=not ok; print(('PASS' if ok else 'FAIL')+f' | {name} | expected={expected} got={got}')
print(f'SUMMARY | {len(cases)-failed}/{len(cases)} passed'); raise SystemExit(1 if failed else 0)
