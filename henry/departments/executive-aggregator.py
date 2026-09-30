#!/usr/bin/env python3
"""Aggregate already-routed department reports into one owner-level recommendation.
Read-only: never executes department recommendations or changes authority.
"""
import json, sys
PRIORITY={'LOW':1,'MEDIUM':2,'HIGH':3,'CRITICAL':4}
SEVERITY={'READY':0,'ACTION_REQUIRED':1,'APPROVAL_NEEDED':2,'HOLD':3,'RISK_DETECTED':4}

def aggregate(reports):
 if not isinstance(reports,list) or not reports:
  return {'schema':'mac-henry.executive-aggregate.v1','decision':'HOLD','reason':'NO_VALID_REPORTS','next_best_move':'Obtain valid department reports before proceeding.','departments_considered':[]}
 accepted=[r for r in reports if r.get('accepted') is True and r.get('decision') in SEVERITY and r.get('priority') in PRIORITY]
 if len(accepted)!=len(reports):
  return {'schema':'mac-henry.executive-aggregate.v1','decision':'HOLD','reason':'UNROUTED_OR_INVALID_REPORT','next_best_move':'Resolve invalid department reporting before proceeding.','departments_considered':[r.get('department') for r in accepted]}
 ranked=sorted(accepted,key=lambda r:(SEVERITY[r['decision']],PRIORITY[r['priority']]),reverse=True)
 lead=ranked[0]
 approval=any(r.get('approval_required') is True for r in accepted)
 risks=[{'department':r['department'],'summary':r.get('risk_summary','')} for r in accepted if r['decision'] in {'RISK_DETECTED','HOLD'}]
 if risks: decision='RISK_DETECTED' if any(r['decision']=='RISK_DETECTED' for r in accepted) else 'HOLD'
 elif approval or any(r['decision']=='APPROVAL_NEEDED' for r in accepted): decision='APPROVAL_NEEDED'
 elif any(r['decision']=='ACTION_REQUIRED' for r in accepted): decision='ACTION_REQUIRED'
 else: decision='READY'
 return {'schema':'mac-henry.executive-aggregate.v1','decision':decision,'lead_department':lead['department'],'lead_priority':lead['priority'],'next_best_move':lead['recommended_next_action'],'approval_required':approval or decision=='APPROVAL_NEEDED','risk_signals':risks,'departments_considered':[r['department'] for r in accepted],'evidence_refs':sorted({x for r in accepted for x in r.get('evidence_refs',[])})}

if __name__=='__main__':
 try: reports=json.load(sys.stdin)
 except Exception:
  print(json.dumps({'schema':'mac-henry.executive-aggregate.v1','decision':'HOLD','reason':'INVALID_JSON'})); raise SystemExit(1)
 result=aggregate(reports); print(json.dumps(result,indent=2)); raise SystemExit(0 if result['decision']=='READY' else 2)
