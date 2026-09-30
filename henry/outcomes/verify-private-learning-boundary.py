#!/usr/bin/env python3
"""Verify that public Henry cannot inherit Mac Henry private learning authority."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent/'private-learning-boundary.json'
b=json.loads(P.read_text(encoding='utf-8'))
errors=[]
required_private={'private_decision_history','private_business_context','private_learning_weights','private_strategy','private_main_brain_prompts','hidden_reasoning','credentials','access_tokens','wallet_private_keys','seed_phrases','private_identity_records'}
required_public={'opaque_decision_id','decision_fingerprint','public_safe_metric_name','baseline','target','observed','measurement_window','public_evidence_reference','verification_status'}
if b.get('schema')!='henry.private-learning-boundary.v1': errors.append('schema')
if b.get('public_component')!='Henry' or b.get('private_component')!='Mac Henry Brain': errors.append('component_identity')
if not required_private.issubset(set(b.get('public_must_never_receive',[]))): errors.append('private_prohibitions')
if set(b.get('public_may_receive',[]))!=required_public: errors.append('public_allowlist')
a=b.get('public_authority',{})
for key in ('learn_from_outcomes','change_learning_weights','change_strategy','execute_recommendations','request_private_context','promote_own_authority'):
 if a.get(key) is not False: errors.append('authority:'+key)
rules=' '.join(b.get('boundary_rules',[])).lower()
for phrase in ('only explicitly allowlisted','fails closed','never grant execution or learning authority'):
 if phrase not in rules: errors.append('rule:'+phrase)
print('PASS | private Mac Henry learning remains outside public Henry boundary' if not errors else 'FAIL | '+','.join(errors))
raise SystemExit(1 if errors else 0)
