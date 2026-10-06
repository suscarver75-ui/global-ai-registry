#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent/'training-runtime.py';s=importlib.util.spec_from_file_location('tr',P);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
t=m.TrainingStore();student={'authenticated':True,'subject_id':'s1','zone':'MINISTER_STUDENT','human_actor':True};other={'authenticated':True,'subject_id':'s2','zone':'MINISTER_STUDENT','human_actor':True};admin={'authenticated':True,'subject_id':'a1','zone':'ADMIN','human_actor':True}
assert t.enroll(student,'s1','minister-core');assert not t.enroll(other,'s1','minister-core')
assert t.complete_lesson(student,'s1','minister-core','l1');assert not t.complete_lesson(other,'s1','minister-core','l2')
assert t.submit_assessment(student,'s1','minister-core','a1',90);assert not t.approve_assessment(student,'s1','minister-core','a1')
assert t.approve_assessment(admin,'s1','minister-core','a1')
assert t.training_complete('s1','minister-core',['l1'],['a1'])
assert not t.training_complete('s1','minister-core',['l1','l2'],['a1'])
assert t.submit_assessment(student,'s1','minister-core','a2',50);assert not t.approve_assessment(admin,'s1','minister-core','a2',80)
print('CHURCH TRAINING RUNTIME PASS')
