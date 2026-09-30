#!/usr/bin/env python3
import json
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/'learning-governance-public-contract.json').read_text(encoding='utf-8'))
e=[]
if p.get('schema')!='henry.learning-governance-public-contract.v1': e.append('schema')
g=p.get('governance_invariants',{})
false_required={'single_outcome_can_rewrite_strategy','unverified_evidence_can_change_weights','public_henry_can_apply_private_learning','public_henry_can_view_private_learning_state'}
true_required={'conflicting_outcomes_require_review','major_policy_change_requires_owner_approval','major_weight_change_requires_owner_approval','decision_versions_are_immutable','superseded_versions_remain_auditable','rollback_reference_required_for_major_change'}
for k in false_required:
 if g.get(k) is not False:e.append('invariant:'+k)
for k in true_required:
 if g.get(k) is not True:e.append('invariant:'+k)
required_states={'INSUFFICIENT_EVIDENCE','STABLE','CONFLICT_REVIEW','OWNER_APPROVAL_REQUIRED','SUPERSEDED'}
if set(p.get('public_safe_states',[]))!=required_states:e.append('states')
prohibited=set(p.get('prohibited_public_fields',[]))
for k in {'private_learning_weights','private_strategy','private_decision_history','private_business_context','hidden_reasoning','credentials','tokens','private_keys','seed_phrases'}:
 if k not in prohibited:e.append('prohibited:'+k)
rules=' '.join(p.get('rules',[])).lower()
for phrase in ('not authority grants','verified before','conflicting evidence','explicit owner approval','rollback reference','governance proof only'):
 if phrase not in rules:e.append('rule:'+phrase)
print('PASS | governed-learning public contract preserves owner control and private Brain separation' if not e else 'FAIL | '+','.join(e))
raise SystemExit(1 if e else 0)
