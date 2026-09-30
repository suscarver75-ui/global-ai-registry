#!/usr/bin/env python3
from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parent/'report-router.py'
s=importlib.util.spec_from_file_location('router',P); r=importlib.util.module_from_spec(s); s.loader.exec_module(r)
base={'department':'business_operations','status':'READY','priority':'MEDIUM','evidence_refs':['receipt:HNY-001'],'recommended_next_action':'Review next-best-move preview','approval_required':False,'risk_summary':'No material risk detected.'}
cases=[]
cases.append(('valid report accepted',r.route(dict(base))['accepted'],True))
x=dict(base); x.pop('evidence_refs'); cases.append(('missing evidence rejected',r.route(x)['accepted'],False))
x=dict(base); x['department']='unknown'; cases.append(('unknown department rejected',r.route(x)['accepted'],False))
x=dict(base); x['status']='EXECUTE_NOW'; cases.append(('invalid status rejected',r.route(x)['accepted'],False))
x=dict(base); x['priority']='SUPER'; cases.append(('invalid priority rejected',r.route(x)['accepted'],False))
x=dict(base); x['risk_summary']='credentials'; cases.append(('credential category rejected',r.route(x)['accepted'],False))
x=dict(base); x['recommended_next_action']='use seed_phrases'; cases.append(('seed phrase category rejected',r.route(x)['accepted'],False))
x=dict(base); x['risk_summary']='private_main_brain_content'; cases.append(('private brain content rejected',r.route(x)['accepted'],False))
failed=0
for name,got,expected in cases:
 ok=got==expected; failed+=not ok; print(('PASS' if ok else 'FAIL')+f' | {name} | expected={expected} got={got}')
print(f'SUMMARY | {len(cases)-failed}/{len(cases)} passed'); raise SystemExit(1 if failed else 0)
