#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
mb=load('mb',ROOT/'mega-base/core.py');pd=load('pd',D/'protected-data.py')
base=mb.MegaBase();assert base.register_tenant('seven-fold','SEVEN_FOLD_CHURCH')
a={'authenticated':True,'subject_id':'m1','tenant_id':'seven-fold','capabilities':['profile.write','profile.read','consent.write'],'zone':'MEMBER','human_actor':True}
b={'authenticated':True,'subject_id':'m2','tenant_id':'seven-fold','capabilities':['profile.read'],'zone':'MEMBER','human_actor':True}
outside={'authenticated':True,'subject_id':'x','tenant_id':'other','capabilities':['profile.read'],'zone':'MEMBER'}
store=pd.ProtectedStore()
assert base.authorize(a,'seven-fold','profile.write');assert store.put_profile(a,'m1','Member One',{'accessibility':'large-text'},now=1);base.receipt('seven-fold','m1','profile.write','ALLOW',1)
assert store.get_profile(a,'m1')['display_name']=='Member One'
assert store.get_profile(b,'m1') is None;base.receipt('seven-fold','m2','profile.cross_member.read','DENY',2)
assert not base.authorize(outside,'seven-fold','profile.read')
assert store.record_consent(a,'m1','privacy-v1',True,now=3);base.receipt('seven-fold','m1','consent.write','ALLOW',3)
export=store.export_subject(a,'m1');assert export['consents'][0]['granted']==1
assert store.integrity_ok() and base.verify_chain()
print('CHURCH MEGA BASE PROTECTED DATA PASS')
