#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent/'identity-runtime.py'; s=importlib.util.spec_from_file_location('identity_runtime',P); m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)
x=m.IdentityStore(); assert x.create_subject('member-001'); assert not x.create_subject('member-001')
sid=x.issue_session('member-001',100); assert sid; assert x.validate_session(sid,101)
r=m.authz_request(x,sid,'membership','READ',101); assert r['authenticated'] and r['zone']=='MEMBER'
assert not r['step_up']; assert x.step_up(sid,True,102); assert m.authz_request(x,sid,'membership','READ',103)['step_up']
assert x.revoke_session(sid); assert x.validate_session(sid,104) is None
sid=x.issue_session('member-001',200); assert sid; assert x.change_role('member-001','MINISTER_STUDENT',owner_approved=True); assert x.validate_session(sid,201) is None
sid=x.issue_session('member-001',300); assert m.authz_request(x,sid,'training-records','READ',301)['zone']=='MINISTER_STUDENT'
assert x.disable_subject('member-001'); assert x.validate_session(sid,302) is None
assert not x.change_role('member-001','ADMIN',owner_approved=False)
assert all('token' not in str(e).lower() and 'nonce' not in str(e).lower() for e in x.audit)
print('ALL IDENTITY RUNTIME TESTS PASS')
