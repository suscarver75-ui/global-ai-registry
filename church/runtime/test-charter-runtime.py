#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent/'charter-runtime.py';s=importlib.util.spec_from_file_location('ch',P);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
x=m.CharterStore();member={'authenticated':True,'subject_id':'m1','zone':'MEMBER','human_actor':True};admin={'authenticated':True,'subject_id':'a1','zone':'ADMIN','human_actor':True,'step_up':True,'owner_approved':True};bot=dict(admin);bot['human_actor']=False
cid=x.apply(member,'Test Fellowship',100);assert cid
assert not x.decide(member,cid,'APPROVED',101);assert not x.decide(bot,cid,'APPROVED',101);assert x.decide(admin,cid,'APPROVED',102)
p=x.public_verify(cid);assert set(p)=={'charter_id','name','status'} and p['status']=='APPROVED'
assert x.decide(admin,cid,'SUSPENDED',103);assert x.decide(admin,cid,'APPROVED',104);assert x.decide(admin,cid,'REVOKED',105);assert not x.decide(admin,cid,'APPROVED',106)
print('CHURCH CHARTER RUNTIME PASS')
