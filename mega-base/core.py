#!/usr/bin/env python3
"""MEGA BASE core isolation/evidence primitives. Developer-safe reference runtime."""
import hashlib,hmac,json,secrets,time
class MegaBase:
 def __init__(self):
  self.tenants={};self.events=[];self.prev='0'*64
 def register_tenant(self,tenant_id,department):
  if not tenant_id or not department or tenant_id in self.tenants:return False
  self.tenants[tenant_id]={'department':department,'enabled':True};return True
 def authorize(self,ctx,tenant_id,capability):
  t=self.tenants.get(tenant_id)
  return bool(t and t['enabled'] and ctx and ctx.get('authenticated') and ctx.get('tenant_id')==tenant_id and capability in set(ctx.get('capabilities',[])))
 def receipt(self,tenant_id,actor,action,result,now=None):
  if tenant_id not in self.tenants:raise ValueError('unknown tenant')
  body={'tenant_id':tenant_id,'actor':actor,'action':action,'result':result,'at':int(time.time() if now is None else now),'prev':self.prev}
  digest=hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest();body['hash']=digest;self.prev=digest;self.events.append(body);return dict(body)
 def verify_chain(self):
  prev='0'*64
  for e in self.events:
   x={k:v for k,v in e.items() if k!='hash'}
   if x['prev']!=prev or hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=e['hash']:return False
   prev=e['hash']
  return True
