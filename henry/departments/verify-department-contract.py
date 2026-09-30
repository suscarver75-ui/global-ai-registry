#!/usr/bin/env python3
"""Verify Mac Henry department managers remain least-privilege and fail closed."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent/'department-contract.json'
d=json.loads(P.read_text(encoding='utf-8'))
errors=[]
allowed_status={'READY','HOLD','APPROVAL_NEEDED','ACTION_REQUIRED','RISK_DETECTED'}
if d.get('schema')!='mac-henry.department-contract.v1': errors.append('schema')
if d.get('default_authority')!='ADVISE_ONLY': errors.append('default_authority')
if set(d.get('required_output_states',[]))!=allowed_status: errors.append('output_states')
rules=' '.join(d.get('rules',[])).lower()
for phrase in ('do not inherit private main brain authority','may not expand their own permissions','fails closed'):
 if phrase not in rules: errors.append('rule:'+phrase)
deps=d.get('initial_departments',{})
required={'business_operations','content_products','finance_review','security_governance','henry_public_operations'}
if not required.issubset(deps): errors.append('departments')
for name,cfg in deps.items():
 if cfg.get('authority') not in {'ADVISE_ONLY','PREVIEW_ONLY'}: errors.append('authority:'+name)
finance=deps.get('finance_review',{})
if not {'wallet_private_keys','seed_phrases','credentials'}.issubset(set(finance.get('prohibited',[]))): errors.append('finance_secret_boundary')
henry=deps.get('henry_public_operations',{})
if henry.get('authority')!='PREVIEW_ONLY': errors.append('henry_preview_boundary')
if 'private_main_brain_content' not in henry.get('prohibited',[]): errors.append('henry_private_brain_boundary')
print('PASS | department managers remain restricted and least-privilege' if not errors else 'FAIL | '+','.join(errors))
raise SystemExit(1 if errors else 0)
