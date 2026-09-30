#!/usr/bin/env python3
"""Mac Henry owner-facing executive status layer. Read-only and fail-closed."""
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
state=json.loads((ROOT/'authority-state.json').read_text(encoding='utf-8'))
proc=subprocess.run([sys.executable,str(ROOT/'manager-readiness.py')],capture_output=True,text=True)
try: readiness=json.loads(proc.stdout)
except Exception: readiness={'henry_status':'HOLD','checks':{},'owner_message':'Readiness evaluator did not return valid evidence.'}
status=readiness.get('henry_status','HOLD')
if proc.returncode!=0 or status=='HOLD': decision='HOLD'
elif state.get('mutation_enabled') is True: decision='APPROVAL_NEEDED'
elif status=='READY_FOR_PREVIEW_OPERATIONS': decision='READY'
else: decision='ACTION_REQUIRED'
report={
 'schema':'mac-henry.owner-status.v1',
 'decision':decision,
 'henry_authority':state.get('current_level'),
 'public_mutation_enabled':state.get('mutation_enabled'),
 'bounded_automation_enabled':state.get('bounded_automation_enabled'),
 'private_brain_authority_exposed':state.get('private_main_brain_authority'),
 'readiness':status,
 'owner_summary':{
  'READY':'Henry public layer is healthy for its currently approved preview-only work.',
  'HOLD':'Stop advancement. One or more required controls are not healthy.',
  'APPROVAL_NEEDED':'A mutation-capable state requires explicit owner approval and evidence review.',
  'ACTION_REQUIRED':'The state needs review before further advancement.'
 }[decision],
 'checks':readiness.get('checks',{})
}
print(json.dumps(report,indent=2)); raise SystemExit(0 if decision=='READY' else 1)
