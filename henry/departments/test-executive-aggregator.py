#!/usr/bin/env python3
from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parent/'executive-aggregator.py'; s=importlib.util.spec_from_file_location('agg',P); a=importlib.util.module_from_spec(s); s.loader.exec_module(a)
def r(dept,status='READY',priority='MEDIUM',approval=False,action='Continue approved work',risk='None'):
 return {'accepted':True,'decision':status,'department':dept,'priority':priority,'recommended_next_action':action,'approval_required':approval,'risk_summary':risk,'evidence_refs':['receipt:'+dept]}
cases=[
 ('all ready',a.aggregate([r('business_operations'),r('content_products')])['decision'],'READY'),
 ('risk dominates',a.aggregate([r('business_operations'),r('security_governance','RISK_DETECTED','CRITICAL',False,'Review control gap','Control gap')])['decision'],'RISK_DETECTED'),
 ('hold dominates approval',a.aggregate([r('finance_review','APPROVAL_NEEDED','HIGH',True),r('security_governance','HOLD','HIGH')])['decision'],'HOLD'),
 ('approval surfaced',a.aggregate([r('finance_review','APPROVAL_NEEDED','HIGH',True)])['decision'],'APPROVAL_NEEDED'),
 ('action required surfaced',a.aggregate([r('content_products','ACTION_REQUIRED','MEDIUM')])['decision'],'ACTION_REQUIRED'),
 ('empty fails closed',a.aggregate([])['decision'],'HOLD'),
 ('unrouted input fails closed',a.aggregate([{'accepted':False}])['decision'],'HOLD')]
failed=0
for name,got,expected in cases:
 ok=got==expected; failed+=not ok; print(('PASS' if ok else 'FAIL')+f' | {name} | expected={expected} got={got}')
print(f'SUMMARY | {len(cases)-failed}/{len(cases)} passed'); raise SystemExit(1 if failed else 0)
