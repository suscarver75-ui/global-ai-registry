#!/usr/bin/env python3
from pathlib import Path
import copy, importlib.util
P=Path(__file__).resolve().parent/'chain.py'; s=importlib.util.spec_from_file_location('henry_receipt_chain',P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def receipt(i,cmd): return {'receipt_id':f'R-{i}','command_id':cmd,'contract_version':'henry.command-contract.v1','action':'VERIFY_PUBLIC_ARTIFACT','decision':'ALLOW_EXECUTE','target':'henry/health.json','started_at':f'2026-09-30T05:0{i}:00Z','completed_at':f'2026-09-30T05:0{i}:01Z','before_state_reference':'sha256:before','after_state_reference':'sha256:after','verification_status':'VERIFIED','evidence_references':['henry/health.json'],'error_code_if_any':None}
r1=m.seal(receipt(1,'CMD-1')); r2=m.seal(receipt(2,'CMD-2'),r1['receipt_hash']); r3=m.seal(receipt(3,'CMD-3'),r2['receipt_hash']); valid=[r1,r2,r3]
cases=[]
cases.append(('valid chain accepted',m.verify_chain(valid),True))
t=copy.deepcopy(valid); t[1]['decision']='DENY_SCOPE'; cases.append(('edited receipt rejected',m.verify_chain(t),False))
t=[r1,r3,r2]; cases.append(('reordered receipts rejected',m.verify_chain(t),False))
t=[r1,r3]; cases.append(('removed receipt rejected',m.verify_chain(t),False))
t=copy.deepcopy(valid); t[2]['previous_receipt_hash']='sha256:forged'; cases.append(('forged previous pointer rejected',m.verify_chain(t),False))
t=copy.deepcopy(valid); t[0]['receipt_hash']='sha256:forged'; cases.append(('forged receipt hash rejected',m.verify_chain(t),False))
failed=0
for name,got,expected in cases:
 ok=got is expected; failed+=not ok; print(('PASS' if ok else 'FAIL')+f' | {name} | expected={expected} got={got}')
print(f'SUMMARY | {len(cases)-failed}/{len(cases)} passed'); raise SystemExit(1 if failed else 0)
