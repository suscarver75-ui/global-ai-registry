#!/usr/bin/env python3
"""Henry public-safe outcome verifier.
Demonstrates immutable decision/outcome linkage without exposing Mac Henry private decision memory.
No learning weights, private context, credentials, or execution authority are stored here.
"""
import hashlib, json, sys
ALLOWED={'decision_id','decision_fingerprint','metric_name','expected_direction','baseline','target','observed','measurement_window','evidence_refs'}
DIRECTIONS={'UP','DOWN','AT_OR_ABOVE','AT_OR_BELOW'}

def canonical(v): return json.dumps(v,sort_keys=True,separators=(',',':'))
def fingerprint(decision): return hashlib.sha256(canonical(decision).encode()).hexdigest()
def verify(record, decision):
 errors=[]
 extra=set(record)-ALLOWED
 if extra: errors.append('UNAPPROVED_FIELDS:'+','.join(sorted(extra)))
 if record.get('decision_id')!=decision.get('decision_id'): errors.append('DECISION_ID_MISMATCH')
 if record.get('decision_fingerprint')!=fingerprint(decision): errors.append('DECISION_FINGERPRINT_MISMATCH')
 if record.get('expected_direction') not in DIRECTIONS: errors.append('INVALID_DIRECTION')
 for k in ('baseline','target','observed'):
  if not isinstance(record.get(k),(int,float)): errors.append('INVALID_'+k.upper())
 if not isinstance(record.get('evidence_refs'),list) or not record.get('evidence_refs'): errors.append('MISSING_EVIDENCE')
 if errors:return {'schema':'henry.public-outcome-verification.v1','status':'HOLD','errors':errors,'execution_authority':False}
 b,t,o=record['baseline'],record['target'],record['observed']; d=record['expected_direction']
 achieved=(o>=t if d in {'UP','AT_OR_ABOVE'} else o<=t)
 delta=o-b
 return {'schema':'henry.public-outcome-verification.v1','status':'VERIFIED_MEASUREMENT','decision_id':record['decision_id'],'metric_name':record['metric_name'],'target_achieved':achieved,'delta_from_baseline':delta,'evidence_refs':record['evidence_refs'],'private_learning_authority':False,'execution_authority':False}

if __name__=='__main__':
 try:
  payload=json.load(sys.stdin); out=verify(payload['record'],payload['decision'])
 except Exception:
  out={'schema':'henry.public-outcome-verification.v1','status':'HOLD','errors':['INVALID_INPUT'],'execution_authority':False}
 print(json.dumps(out,indent=2)); raise SystemExit(0 if out['status']=='VERIFIED_MEASUREMENT' else 1)
