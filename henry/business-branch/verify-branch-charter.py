#!/usr/bin/env python3
import json
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/'branch-charter.json').read_text(encoding='utf-8'))
e=[]
if p.get('schema')!='henry.business-branch-charter.v1':e.append('schema')
if p.get('enterprise_parent')!='Mac Henry':e.append('parent')
if p.get('branch_manager')!='Henry':e.append('manager')
if p.get('classification')!='BUSINESS_BRANCH':e.append('classification')
h=p.get('hierarchy',{})
if h.get('enterprise_manager')!='Mac Henry' or h.get('business_branch')!='GitHub Business' or h.get('branch_manager')!='Henry':e.append('hierarchy')
metrics=set(p.get('economic_metrics',[]))
for k in ('revenue','recurring_revenue','gross_margin','net_contribution','operating_cost','asset_value_created','income_basket_performance','growth_rate'):
 if k not in metrics:e.append('metric:'+k)
pro=set(p.get('prohibited_branch_fields',[]))
for k in ('mac_henry_private_strategy','cross_business_private_rankings','private_financial_context','private_learning_weights','hidden_reasoning','credentials','tokens','private_keys','seed_phrases'):
 if k not in pro:e.append('prohibited:'+k)
r=' '.join(p.get('boundary_rules',[])).lower()
for phrase in ('one branch','subordinate to mac henry','report to henry','not stored in or exposed','sibling branches','real economic and operating outcomes'):
 if phrase not in r:e.append('rule:'+phrase)
print('PASS | GitHub is a Henry-managed business branch under private Mac Henry enterprise' if not e else 'FAIL | '+','.join(e))
raise SystemExit(1 if e else 0)
