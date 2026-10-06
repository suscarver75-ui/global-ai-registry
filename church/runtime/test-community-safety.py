#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent/'community-safety.py';s=importlib.util.spec_from_file_location('cs',P);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
c=m.CommunitySafety();member={'authenticated':True,'subject_id':'m1','zone':'MEMBER','human_actor':True};admin={'authenticated':True,'subject_id':'a1','zone':'ADMIN','human_actor':True};aiadmin={'authenticated':True,'subject_id':'bot','zone':'ADMIN','human_actor':False}
rid=c.report(member,'post:42','HARASSMENT',100);assert rid
assert not c.resolve(member,rid,'CONTENT_REMOVED',101);assert not c.resolve(aiadmin,rid,'CONTENT_REMOVED',101)
assert c.resolve(admin,rid,'CONTENT_REMOVED',102);aid=c.appeal(member,rid,103);assert aid
pub=c.public_status(rid);assert set(pub)=={'report_id','status'} and 'reporter_id' not in pub
assert c.report({},'x','THREAT') is None
print('CHURCH COMMUNITY SAFEGUARDING PASS')
