#!/usr/bin/env python3
"""Validate department reports before they can be summarized upward to Mac Henry.
Read-only validation: no action execution and no authority changes.
"""
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
contract=json.loads((ROOT/'department-contract.json').read_text(encoding='utf-8'))
DEPTS=contract['initial_departments']
STATES=set(contract['required_output_states'])
FIELDS=set(contract['required_report_fields'])
SENSITIVE={'wallet_private_keys','seed_phrases','credentials','private_main_brain_content','hidden_reasoning','access_tokens'}

def validate(report):
 errors=[]
 missing=FIELDS-set(report)
 if missing: errors.append('missing_fields:'+','.join(sorted(missing)))
 dept=report.get('department')
 if dept not in DEPTS: errors.append('unknown_department')
 if report.get('status') not in STATES: errors.append('invalid_status')
 if report.get('priority') not in {'LOW','MEDIUM','HIGH','CRITICAL'}: errors.append('invalid_priority')
 refs=report.get('evidence_refs')
 if not isinstance(refs,list): errors.append('evidence_refs_not_list')
 if report.get('approval_required') not in {True,False}: errors.append('invalid_approval_flag')
 blob=json.dumps(report,sort_keys=True).lower()
 for term in SENSITIVE:
  if term.lower() in blob: errors.append('sensitive_material:'+term)
 return errors

def route(report):
 errors=validate(report)
 if errors:
  return {'schema':'mac-henry.department-route.v1','accepted':False,'decision':'HOLD','errors':errors}
 return {'schema':'mac-henry.department-route.v1','accepted':True,'decision':report['status'],'department':report['department'],'priority':report['priority'],'recommended_next_action':report['recommended_next_action'],'approval_required':report['approval_required'],'risk_summary':report['risk_summary'],'evidence_refs':report['evidence_refs']}

if __name__=='__main__':
 try: report=json.load(sys.stdin)
 except Exception:
  print(json.dumps({'schema':'mac-henry.department-route.v1','accepted':False,'decision':'HOLD','errors':['invalid_json']})); raise SystemExit(1)
 result=route(report); print(json.dumps(result,indent=2)); raise SystemExit(0 if result['accepted'] else 1)
