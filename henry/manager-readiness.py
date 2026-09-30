#!/usr/bin/env python3
"""Owner-facing readiness evaluator for the restricted Henry public layer. Read-only; grants no authority."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
state=json.loads((ROOT/'authority-state.json').read_text())
trust=json.loads((ROOT/'trust-levels.json').read_text())
audit=json.loads((ROOT/'audit-policy.json').read_text())
checks={
 'authority_preview_only': state.get('current_level')=='L1_PREVIEW' and state.get('mutation_enabled') is False,
 'fail_closed': state.get('fail_closed') is True,
 'no_private_brain_authority': state.get('private_main_brain_authority') is False,
 'no_self_promotion': state.get('self_promotion_allowed') is False,
 'audit_public_safe': audit.get('boundary')=='PUBLIC_SAFE' and audit.get('authority')=='NO_PRIVATE_AUTHORITY',
 'trust_model_present': trust.get('schema')=='henry.trust-levels.v1',
}
status='READY_FOR_PREVIEW_OPERATIONS' if all(checks.values()) else 'HOLD'
report={'schema':'mac-henry.manager-readiness.v1','henry_status':status,'authority_level':state.get('current_level'),'mutation_enabled':state.get('mutation_enabled'),'bounded_automation_enabled':state.get('bounded_automation_enabled'),'checks':checks,'owner_message':'Henry is constrained to preview-only public operations.' if status.startswith('READY') else 'Henry readiness checks require attention.'}
print(json.dumps(report,indent=2)); raise SystemExit(0 if status.startswith('READY') else 1)
