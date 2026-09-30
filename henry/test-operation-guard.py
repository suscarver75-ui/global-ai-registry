#!/usr/bin/env python3
from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parent/'operation-guard.py'; s=importlib.util.spec_from_file_location('guard',P); g=importlib.util.module_from_spec(s); s.loader.exec_module(g)
def op(**kw):
 x={'risk':'LOW','rollback_plan':'restore prior verified state','post_verify':True}; x.update(kw); return x
cases=[]
cases.append(('safe bounded operation allowed',g.evaluate(op(),g.GuardState()),'ALLOW_BOUNDED_OPERATION'))
cases.append(('high risk denied',g.evaluate(op(risk='HIGH'),g.GuardState()),'DENY_RISK'))
cases.append(('missing rollback denied',g.evaluate(op(rollback_plan=None),g.GuardState()),'DENY_NO_ROLLBACK'))
cases.append(('missing verification denied',g.evaluate(op(post_verify=False),g.GuardState()),'DENY_NO_VERIFY'))
cases.append(('budget exhaustion denied',g.evaluate(op(),g.GuardState(window_count=5)),'DENY_BUDGET'))
st=g.GuardState(); g.record_result(st,False); g.record_result(st,False); cases.append(('two failures open circuit',g.evaluate(op(),st),'DENY_CIRCUIT_OPEN'))
st2=g.GuardState(); g.record_result(st2,False); g.record_result(st2,True); cases.append(('success resets failure streak',g.evaluate(op(),st2),'ALLOW_BOUNDED_OPERATION'))
failed=0
for name,got,expected in cases:
 ok=got==expected; failed+=not ok; print(('PASS' if ok else 'FAIL')+f' | {name} | expected={expected} got={got}')
print(f'SUMMARY | {len(cases)-failed}/{len(cases)} passed'); raise SystemExit(1 if failed else 0)
