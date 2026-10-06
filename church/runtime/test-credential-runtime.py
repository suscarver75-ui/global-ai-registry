#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent/'credential-runtime.py';s=importlib.util.spec_from_file_location('cr',P);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
c=m.CredentialStore();admin={'authenticated':True,'subject_id':'admin1','zone':'ADMIN','human_actor':True,'step_up':True,'issuer_authorized':True}
leader={'authenticated':True,'subject_id':'leader','zone':'CREDENTIALED_LEADER','human_actor':True,'step_up':True,'issuer_authorized':True}
assert c.issue(leader,'s1','MINISTER',True,200,100) is None
assert c.issue(admin,'s1','MINISTER',False,200,100) is None
cid=c.issue(admin,'s1','MINISTER',True,200,100);assert cid
pub=c.public_verify(cid,150);assert pub['valid'] and 'subject_id' not in pub and 'issuer_id' not in pub
assert c.set_good_standing(admin,'s1','GOOD',110)
assert c.set_status(admin,cid,'SUSPENDED',120);assert not c.public_verify(cid,130)['valid']
assert c.set_status(admin,cid,'ACTIVE',140);assert c.public_verify(cid,150)['valid']
assert c.public_verify(cid,201)['status']=='EXPIRED'
assert c.set_status(admin,cid,'REVOKED',160);assert not c.public_verify(cid,170)['valid']
paid=dict(admin);paid['payment_confirmed']=True;paid['issuer_authorized']=False
assert c.issue(paid,'s2','MINISTER',True,300,100) is None
print('CHURCH CREDENTIAL + GOOD STANDING PASS')
