#!/usr/bin/env python3
from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parent/'decision-engine.py'; s=importlib.util.spec_from_file_location('d',P); d=importlib.util.module_from_spec(s); s.loader.exec_module(d)
def o(name,action='KEEP',works=80,earn=70,save=60,cost=25,risk='LOW',evidence=80,reverse=80):return {'name':name,'action':action,'works_score':works,'earn_score':earn,'save_score':save,'cost_score':cost,'risk':risk,'evidence_score':evidence,'reversibility_score':reverse}
cases=[]
cases.append(('strong useful option kept',d.evaluate(o('A'))['decision'],'KEEP'))
cases.append(('weak evidence tested first',d.evaluate(o('B',evidence=20))['decision'],'TEST'))
cases.append(('critical risk held',d.evaluate(o('C',risk='CRITICAL'))['decision'],'HOLD'))
cases.append(('sell requires approval',d.evaluate(o('D',action='SELL'))['approval_required'],True))
cases.append(('donate requires approval',d.evaluate(o('E',action='DONATE'))['approval_required'],True))
cases.append(('invalid score held',d.evaluate(o('F',works=120))['decision'],'HOLD'))
res=d.decide([o('lower',works=55,earn=40),o('higher',works=95,earn=95,save=80,cost=10)])
cases.append(('best option selected',res['next_best_move']['name'],'higher'))
cases.append(('engine has no execution authority',res['execution_authority'],False))
cases.append(('empty options fail closed',d.decide([])['status'],'HOLD'))
failed=0
for name,got,expected in cases:
 ok=got==expected; failed+=not ok; print(('PASS' if ok else 'FAIL')+f' | {name} | expected={expected} got={got}')
print(f'SUMMARY | {len(cases)-failed}/{len(cases)} passed'); raise SystemExit(1 if failed else 0)
