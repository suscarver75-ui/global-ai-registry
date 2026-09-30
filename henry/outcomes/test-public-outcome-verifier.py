#!/usr/bin/env python3
from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parent/'public-outcome-verifier.py'; s=importlib.util.spec_from_file_location('v',P); v=importlib.util.module_from_spec(s); s.loader.exec_module(v)
d={'decision_id':'MH-PUBLIC-DEMO-001','recommendation':'TEST','public_safe':True}
r={'decision_id':d['decision_id'],'decision_fingerprint':v.fingerprint(d),'metric_name':'conversion_rate','expected_direction':'AT_OR_ABOVE','baseline':2.0,'target':3.0,'observed':3.4,'measurement_window':'30d','evidence_refs':['public:metric-001']}
cases=[]
cases.append(('valid measurement verified',v.verify(dict(r),d)['status'],'VERIFIED_MEASUREMENT'))
cases.append(('target result recognized',v.verify(dict(r),d)['target_achieved'],True))
x=dict(r); x['decision_fingerprint']='tampered'; cases.append(('tampered decision binding held',v.verify(x,d)['status'],'HOLD'))
x=dict(r); x['private_context']='secret'; cases.append(('unapproved private field held',v.verify(x,d)['status'],'HOLD'))
x=dict(r); x['evidence_refs']=[]; cases.append(('missing evidence held',v.verify(x,d)['status'],'HOLD'))
x=dict(r); x['expected_direction']='MAGIC'; cases.append(('invalid direction held',v.verify(x,d)['status'],'HOLD'))
out=v.verify(dict(r),d); cases.append(('no private learning authority',out['private_learning_authority'],False)); cases.append(('no execution authority',out['execution_authority'],False))
failed=0
for name,got,expected in cases:
 ok=got==expected; failed+=not ok; print(('PASS' if ok else 'FAIL')+f' | {name} | expected={expected} got={got}')
print(f'SUMMARY | {len(cases)-failed}/{len(cases)} passed'); raise SystemExit(1 if failed else 0)
