#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
D=Path(__file__).resolve().parent
def load(name,file):
 s=importlib.util.spec_from_file_location(name,D/file);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
t=load('tr','training-runtime.py');c=load('cr','credential-runtime.py');b=load('br','megabase-church-bridge.py')
ts=t.TrainingStore();cs=c.CredentialStore();bridge=b.ChurchCredentialBridge(ts,cs)
student={'authenticated':True,'subject_id':'s1','zone':'MINISTER_STUDENT','human_actor':True}
admin={'authenticated':True,'subject_id':'a1','zone':'ADMIN','human_actor':True,'step_up':True,'issuer_authorized':True}
assert ts.enroll(student,'s1','ministry')
r=bridge.issue_after_training(admin,'s1','ministry',['l1'],['a1'],'MINISTER',9999,now=1);assert not r['issued'] and r['reason']=='TRAINING_INCOMPLETE'
assert ts.complete_lesson(student,'s1','ministry','l1');assert ts.submit_assessment(student,'s1','ministry','a1',95)
assert not ts.approve_assessment(student,'s1','ministry','a1')
assert ts.approve_assessment(admin,'s1','ministry','a1')
r=bridge.issue_after_training(admin,'s1','ministry',['l1'],['a1'],'MINISTER',9999,now=1);assert r['issued'] and r['training_evidence']['complete']
v=cs.public_verify(r['credential_id'],now=2);assert v['valid'] and 'subject_id' not in v
assert cs.set_status(admin,r['credential_id'],'REVOKED',now=3);assert not cs.public_verify(r['credential_id'],now=4)['valid']
print('CHURCH MEGA BASE TRAINING-CREDENTIAL BRIDGE PASS')
