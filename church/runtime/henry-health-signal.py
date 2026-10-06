#!/usr/bin/env python3
"""Sanitized Church operational signal for bounded Henry management."""
ALLOWED={'component','status','verification_level','last_check','open_blockers','evidence_ref'}
FORBIDDEN={'member','member_id','subject_id','email','phone','message','payment','profile','secret','token','credential_holder','private_brain'}
VALID_STATUS={'HEALTHY','DEGRADED','CONTAINED','OFFLINE'}
def sanitize_signal(raw):
 if not isinstance(raw,dict): raise ValueError('signal must be object')
 for k in raw:
  if k.lower() in FORBIDDEN: raise ValueError('protected field')
 out={k:raw[k] for k in ALLOWED if k in raw}
 if not {'component','status','verification_level'}<=out.keys(): raise ValueError('missing required field')
 if out['status'] not in VALID_STATUS: raise ValueError('bad status')
 blockers=out.get('open_blockers',[])
 if not isinstance(blockers,list) or any(not isinstance(x,str) for x in blockers): raise ValueError('bad blockers')
 return out
def henry_view(signals):
 return {'schema':'seven-fold-church.henry-health.v1','scope':'SANITIZED_OPERATIONAL_ONLY','private_brain_shared':False,'signals':[sanitize_signal(x) for x in signals]}
