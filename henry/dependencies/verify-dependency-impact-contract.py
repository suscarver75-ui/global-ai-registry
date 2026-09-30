#!/usr/bin/env python3
import json
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/'dependency-impact-public-contract.json').read_text(encoding='utf-8'))
e=[]
if p.get('schema')!='henry.dependency-impact-public-contract.v1':e.append('schema')
domains={'FINANCE','WORKLOAD','SECURITY','CUSTOMER','PRODUCT','LEGAL_COMPLIANCE','OPERATIONS','REPUTATION','DATA_PRIVACY','FUTURE_OPTIONALITY'}
if set(p.get('required_impact_domains',[]))!=domains:e.append('domains')
fields={'dependency_id','domain','relationship','criticality','failure_mode','downstream_effects','mitigation_ref','evidence_refs','owner_review_trigger'}
if set(p.get('required_fields',[]))!=fields:e.append('fields')
if set(p.get('criticality_bands',[]))!={'LOW','MEDIUM','HIGH','CRITICAL'}:e.append('criticality')
rels={'REQUIRES','BLOCKS','ENABLES','DEGRADES','AMPLIFIES_RISK','REDUCES_RISK','CONFLICTS_WITH'}
if set(p.get('relationship_types',[]))!=rels:e.append('relationships')
a=p.get('public_authority',{})
for k in ('execute_dependency_change','override_critical_dependency','change_private_strategy','request_private_context'):
 if a.get(k) is not False:e.append('authority:'+k)
pro=set(p.get('prohibited_public_fields',[]))
for k in ('private_strategy','private_business_context','private_dependency_memory','private_learning_weights','hidden_reasoning','credentials','tokens','private_keys','seed_phrases'):
 if k not in pro:e.append('prohibited:'+k)
r=' '.join(p.get('governance_rules',[])).lower()
for phrase in ('all required impact domains','require owner review','fail closed','cross-department effects','future optionality','never grants execution authority','dependency proof only'):
 if phrase not in r:e.append('rule:'+phrase)
print('PASS | dependency governance preserves downstream analysis, owner control and private Brain separation' if not e else 'FAIL | '+','.join(e))
raise SystemExit(1 if e else 0)
