#!/usr/bin/env python3
"""Public-safe confidence gate for Henry.
Uses categorical evidence governance only; private Mac Henry weights and strategy remain outside this component.
"""
import json,sys
REQ={'verification_state','recency_band','sample_size_band','source_independence_band','contradiction_state','evidence_class','decay_state'}

def gate(items):
 if not isinstance(items,list) or not items:return {'schema':'henry.confidence-gate.v1','state':'HOLD','reason':'NO_EVIDENCE','execution_authority':False}
 if any(not REQ.issubset(i) for i in items):return {'schema':'henry.confidence-gate.v1','state':'HOLD','reason':'INCOMPLETE_EVIDENCE','execution_authority':False}
 if any(i['contradiction_state'] in {'MATERIAL_CONFLICT','UNRESOLVED'} for i in items):return {'schema':'henry.confidence-gate.v1','state':'CONFLICT_REVIEW','reason':'CONTRADICTORY_EVIDENCE','execution_authority':False}
 active=[i for i in items if i['decay_state']!='EXPIRED' and i['recency_band']!='STALE']
 verified=[i for i in active if i['verification_state']=='VERIFIED']
 independent=[i for i in verified if i['source_independence_band']=='MULTI_SOURCE_INDEPENDENT']
 strong=[i for i in independent if i['sample_size_band'] in {'MODERATE','STRONG'} and i['evidence_class'] in {'VERIFIED_RESULT','OBSERVED_RESULT'}]
 if not active:return {'schema':'henry.confidence-gate.v1','state':'INSUFFICIENT_EVIDENCE','reason':'ALL_EVIDENCE_STALE_OR_EXPIRED','execution_authority':False}
 if len(strong)>=2:state='STRONG_PUBLIC_PROOF'
 elif verified:state='LIMITED_PUBLIC_PROOF'
 else:state='INSUFFICIENT_EVIDENCE'
 return {'schema':'henry.confidence-gate.v1','state':state,'counts':{'submitted':len(items),'active':len(active),'verified':len(verified),'independent_strong':len(strong)},'private_weighting_exposed':False,'execution_authority':False}

if __name__=='__main__':
 try:out=gate(json.load(sys.stdin))
 except Exception:out={'schema':'henry.confidence-gate.v1','state':'HOLD','reason':'INVALID_INPUT','execution_authority':False}
 print(json.dumps(out,indent=2));raise SystemExit(0 if out['state'] in {'STRONG_PUBLIC_PROOF','LIMITED_PUBLIC_PROOF'} else 1)
