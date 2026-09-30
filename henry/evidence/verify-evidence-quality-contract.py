#!/usr/bin/env python3
import json
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/'evidence-quality-public-contract.json').read_text(encoding='utf-8'))
e=[]
if p.get('schema')!='henry.evidence-quality-public-contract.v1':e.append('schema')
expected={'verification_state','recency_band','sample_size_band','source_independence_band','contradiction_state','evidence_class','decay_state'}
if set(p.get('public_dimensions',[]))!=expected:e.append('dimensions')
checks={'verification_states':{'VERIFIED','PARTIALLY_VERIFIED','UNVERIFIED'},'recency_bands':{'CURRENT','AGING','STALE'},'sample_size_bands':{'INSUFFICIENT','LIMITED','MODERATE','STRONG'},'source_independence_bands':{'SINGLE_SOURCE','CORRELATED','MULTI_SOURCE_INDEPENDENT'},'contradiction_states':{'NONE','MATERIAL_CONFLICT','UNRESOLVED'},'decay_states':{'ACTIVE','DECAYING','EXPIRED'}}
for k,v in checks.items():
 if set(p.get(k,[]))!=v:e.append(k)
a=p.get('public_authority',{})
for k in ('change_private_confidence_weights','resolve_conflicts_privately','execute_from_confidence','request_private_strategy'):
 if a.get(k) is not False:e.append('authority:'+k)
pro=set(p.get('prohibited_public_fields',[]))
for k in ('private_confidence_weights','private_source_reputation_model','private_strategy','private_business_context','hidden_reasoning','credentials','tokens','private_keys','seed_phrases'):
 if k not in pro:e.append('prohibited:'+k)
r=' '.join(p.get('governance_rules',[])).lower()
for phrase in ('unverified evidence','stale or expired','correlated sources','material contradictions','insufficient sample size','not execution authority','may not see private brain'):
 if phrase not in r:e.append('rule:'+phrase)
print('PASS | evidence-quality governance preserves confidence discipline and private Brain separation' if not e else 'FAIL | '+','.join(e))
raise SystemExit(1 if e else 0)
