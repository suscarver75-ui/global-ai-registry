#!/usr/bin/env python3
import json
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/'scenario-governance-public-contract.json').read_text(encoding='utf-8'))
e=[]
if p.get('schema')!='henry.scenario-governance-public-contract.v1':e.append('schema')
if set(p.get('required_scenarios',[]))!={'BEST_CASE','EXPECTED_CASE','WORST_CASE'}:e.append('scenarios')
req={'scenario_id','assumptions','dependencies','impact_band','likelihood_band','reversibility_band','evidence_refs','decision_change_triggers'}
if set(p.get('required_dimensions',[]))!=req:e.append('dimensions')
checks={'likelihood_bands':{'LOW','MEDIUM','HIGH','UNKNOWN'},'impact_bands':{'LOW','MEDIUM','HIGH','CRITICAL'},'reversibility_bands':{'EASY','MODERATE','DIFFICULT','IRREVERSIBLE'}}
for k,v in checks.items():
 if set(p.get(k,[]))!=v:e.append(k)
a=p.get('public_authority',{})
for k in ('execute_scenario','change_private_forecast_weights','select_private_strategy','request_private_context'):
 if a.get(k) is not False:e.append('authority:'+k)
pro=set(p.get('prohibited_public_fields',[]))
for k in ('private_forecast_weights','private_strategy','private_business_context','private_scenario_memory','hidden_reasoning','credentials','tokens','private_keys','seed_phrases'):
 if k not in pro:e.append('prohibited:'+k)
r=' '.join(p.get('governance_rules',[])).lower()
for phrase in ('must not be represented as certainty','best, expected, and worst','dependencies and assumptions','decision-change triggers','critical worst-case impact','irreversible material decisions','never grants execution authority','scenario proof only'):
 if phrase not in r:e.append('rule:'+phrase)
print('PASS | scenario governance preserves uncertainty, owner control and private Brain separation' if not e else 'FAIL | '+','.join(e))
raise SystemExit(1 if e else 0)
