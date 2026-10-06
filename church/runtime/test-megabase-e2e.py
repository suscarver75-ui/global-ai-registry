#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
mb=load('mb',ROOT/'mega-base/core.py');tr=load('tr',D/'training-runtime.py');cr=load('cr',D/'credential-runtime.py');br=load('br',D/'megabase-church-bridge.py')
base=mb.MegaBase();assert base.register_tenant('seven-fold','SEVEN_FOLD_CHURCH')
member={'authenticated':True,'subject_id':'member-1','tenant_id':'seven-fold','capabilities':['training.write'],'zone':'MINISTER_STUDENT','human_actor':True}
intruder={'authenticated':True,'subject_id':'outsider','tenant_id':'other','capabilities':['training.write']}
admin={'authenticated':True,'subject_id':'admin-1','tenant_id':'seven-fold','capabilities':['credential.issue'],'zone':'ADMIN','human_actor':True,'step_up':True,'issuer_authorized':True}
assert base.authorize(member,'seven-fold','training.write');assert not base.authorize(intruder,'seven-fold','training.write');assert base.authorize(admin,'seven-fold','credential.issue')
ts=tr.TrainingStore();cs=cr.CredentialStore();bridge=br.ChurchCredentialBridge(ts,cs)
assert ts.enroll(member,'member-1','ministry');base.receipt('seven-fold','member-1','training.enroll','ALLOW',1)
denied=bridge.issue_after_training(admin,'member-1','ministry',['lesson-1'],['exam-1'],'MINISTER',10000,now=2);assert not denied['issued'];base.receipt('seven-fold','admin-1','credential.issue','DENY_TRAINING_INCOMPLETE',2)
assert ts.complete_lesson(member,'member-1','ministry','lesson-1');assert ts.submit_assessment(member,'member-1','ministry','exam-1',96);assert ts.approve_assessment(admin,'member-1','ministry','exam-1')
issued=bridge.issue_after_training(admin,'member-1','ministry',['lesson-1'],['exam-1'],'MINISTER',10000,now=3);assert issued['issued'];base.receipt('seven-fold','admin-1','credential.issue','ALLOW',3)
public=cs.public_verify(issued['credential_id'],now=4);assert public['valid'] and 'subject_id' not in public and 'issuer_id' not in public
assert base.verify_chain()
print('CHURCH THROUGH MEGA BASE E2E PASS')
