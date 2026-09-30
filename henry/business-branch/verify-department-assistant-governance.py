#!/usr/bin/env python3
import json
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/'department-assistant-governance.json').read_text(encoding='utf-8'))
e=[]
if p.get('schema')!='henry.department-assistant-governance.v1':e.append('schema')
if p.get('business_branch')!='GitHub Business':e.append('branch')
if p.get('enterprise_manager')!='Mac Henry' or p.get('branch_manager')!='Henry':e.append('management')
chain=p.get('reporting_chain',[])
if chain!=['DEPARTMENT_ASSISTANT','HENRY_BRANCH_MANAGER','MAC_HENRY_ENTERPRISE_MANAGER','HUMAN_OWNER']:e.append('reporting_chain')
cap=set(p.get('department_assistant_required_capabilities',[]))
for k in ('department_status','task_queue','risk_register','asset_register','income_basket_metrics','cost_metrics','experiment_metrics','security_status','needs_and_blockers','report_to_henry'):
 if k not in cap:e.append('capability:'+k)
views=p.get('dashboard_views',{})
for k in ('department_view','henry_branch_view','mac_henry_enterprise_view'):
 if k not in views:e.append('view:'+k)
enterprise=set(views.get('mac_henry_enterprise_view',[]))
for k in ('full_github_branch_visibility','department_drilldown','branch_economics','branch_security','henry_performance','department_assistant_performance'):
 if k not in enterprise:e.append('enterprise_view:'+k)
r=' '.join(p.get('inspection_rules',[])).lower()
for phrase in ('directly at any time','scheduled, unscheduled, announced or unannounced','never becomes a visibility gate','report operationally to henry','may conceal, filter away, delete or downgrade','does not itself grant','remain outside the github branch'):
 if phrase not in r:e.append('rule:'+phrase)
print('PASS | department assistants report to Henry while Mac Henry retains direct branch inspection authority' if not e else 'FAIL | '+','.join(e))
raise SystemExit(1 if e else 0)
