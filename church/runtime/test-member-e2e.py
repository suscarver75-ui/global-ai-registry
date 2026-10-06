#!/usr/bin/env python3
"""End-to-end Church member runtime proof: identity -> session -> authz context -> protected data -> revoke."""
import importlib.util,sys
from pathlib import Path
D=Path(__file__).resolve().parent
def load(name,file):
 s=importlib.util.spec_from_file_location(name,D/file);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
ident=load('church_identity', 'identity-runtime.py'); data=load('church_data','protected-data.py')
ids=ident.IdentityStore(); store=data.ProtectedStore()
assert ids.create_subject('member-a','MEMBER'); assert ids.create_subject('member-b','MEMBER')
sa=ids.issue_session('member-a',100); sb=ids.issue_session('member-b',100)
ca=ident.authz_request(ids,sa,'membership','READ',101); cb=ident.authz_request(ids,sb,'membership','READ',101)
assert store.put_profile(ca,'member-a','A',{'accessibility':'large-text'},101)
assert store.record_consent(ca,'member-a','privacy-v1',True,102)
assert store.get_profile(ca,'member-a')['preferences']['accessibility']=='large-text'
assert store.get_profile(cb,'member-a') is None
assert not store.put_profile(cb,'member-a','B overwrote A',{},103)
assert ids.revoke_session(sa)
dead=ident.authz_request(ids,sa,'membership','READ',104)
assert dead['authenticated'] is False
assert store.get_profile(dead,'member-a') is None
assert ids.change_role('member-b','MINISTER_STUDENT',owner_approved=True)
assert ids.validate_session(sb,105) is None
sb2=ids.issue_session('member-b',106); cb2=ident.authz_request(ids,sb2,'training-records','READ',107)
assert cb2['zone']=='MINISTER_STUDENT'
assert store.integrity_ok()
print('CHURCH MEMBER E2E CHAIN PASS')
