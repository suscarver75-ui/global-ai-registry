#!/usr/bin/env python3
"""Fail CI if Henry's checked-in authority exceeds the currently approved preview-only ceiling."""
import json
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/'authority-state.json').read_text(encoding='utf-8'))
errors=[]
if p.get('schema')!='henry.authority-state.v1': errors.append('schema')
if p.get('current_level')!='L1_PREVIEW': errors.append('current_level')
if p.get('maximum_enabled_level')!='L1_PREVIEW': errors.append('maximum_enabled_level')
for key in ('mutation_enabled','bounded_automation_enabled','private_main_brain_authority','arbitrary_execution','self_promotion_allowed'):
 if p.get(key) is not False: errors.append(key)
if p.get('human_approval_required_for_mutation') is not True: errors.append('human_approval_required_for_mutation')
if p.get('fail_closed') is not True: errors.append('fail_closed')
print('PASS | authority remains preview-only and fail-closed' if not errors else 'FAIL | unauthorized authority state: '+','.join(errors))
raise SystemExit(1 if errors else 0)
