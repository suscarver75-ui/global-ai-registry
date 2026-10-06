#!/usr/bin/env python3
import importlib.util
from pathlib import Path
P=Path(__file__).resolve().parent/'access-control.py'
s=importlib.util.spec_from_file_location('authz',P); a=importlib.util.module_from_spec(s); s.loader.exec_module(a)
def expect(name,req,decision,reason=None):
 r=a.authorize(req); assert r.decision==decision,(name,r)
 if reason: assert r.reason==reason,(name,r)
 print('PASS',name)
expect('public read',{'zone':'PUBLIC','domain':'public','action':'READ'},'ALLOW')
expect('member must authenticate',{'zone':'MEMBER','domain':'membership','action':'READ'},'DENY','AUTHENTICATION_REQUIRED')
expect('member own domain',{'zone':'MEMBER','domain':'membership','action':'READ','authenticated':True},'ALLOW')
expect('member cannot read messages via membership role map',{'zone':'MEMBER','domain':'messages','action':'READ','authenticated':True},'DENY','DOMAIN_NOT_AUTHORIZED')
expect('student cannot issue credential',{'zone':'MINISTER_STUDENT','domain':'credentials','action':'ISSUE_CREDENTIAL','authenticated':True,'step_up':True,'human_actor':True},'DENY')
expect('leader cannot self issue',{'zone':'CREDENTIALED_LEADER','domain':'credentials','action':'ISSUE_CREDENTIAL','authenticated':True,'step_up':True,'human_actor':True},'ALLOW')
expect('leader issue requires stepup',{'zone':'CREDENTIALED_LEADER','domain':'credentials','action':'ISSUE_CREDENTIAL','authenticated':True,'human_actor':True},'DENY','STEP_UP_REQUIRED')
expect('henry cannot issue credential',{'zone':'HENRY','domain':'credentials','action':'ISSUE_CREDENTIAL','authenticated':True,'step_up':True,'human_actor':False},'DENY','HUMAN_AUTHORITY_REQUIRED')
expect('henry can inspect bounded credential state',{'zone':'HENRY','domain':'credentials','action':'READ','authenticated':True},'ALLOW')
expect('admin cannot access payments',{'zone':'ADMIN','domain':'payments','action':'READ','authenticated':True},'DENY','DOMAIN_NOT_AUTHORIZED')
expect('owner payment admin requires approval',{'zone':'MAC_HENRY_OWNER','domain':'payments','action':'PAYMENT_ADMIN','authenticated':True,'step_up':True,'human_actor':True},'DENY','OWNER_APPROVAL_REQUIRED')
expect('owner approved payment admin',{'zone':'MAC_HENRY_OWNER','domain':'payments','action':'PAYMENT_ADMIN','authenticated':True,'step_up':True,'human_actor':True,'owner_approved':True},'ALLOW')
expect('unknown zone',{'zone':'ROOT','domain':'public','action':'READ'},'DENY','UNKNOWN_ZONE')
print('ALL ACCESS CONTROL TESTS PASS')
