#!/usr/bin/env python3
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('guard',ROOT/'firebreak-guard.py'); g=importlib.util.module_from_spec(s); s.loader.exec_module(g)

def check(name,text,allowed):
 r=g.inspect_text(text)
 assert r['safe_to_publish'] is allowed,(name,r)
 print('PASS',name)

check('sanitized command','action=READ_HEALTH target=henry/health.json risk=R0',True)
check('private brain label','Mac Henry private brain: do not publish',False)
check('password','password=hunter-example',False)
check('bearer token','Authorization: Bearer example-token-value',False)
check('github token','ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456',False)
check('private key','-----BEGIN PRIVATE KEY-----\nexample',False)
check('seed phrase','seed phrase: alpha beta gamma delta',False)
check('ordinary public docs','Henry assistant manager public health evidence',True)
assert g.POLICY['rules']['private_to_public_brain_replication']=='DENY'
assert g.POLICY['roles']['henry']=='GITHUB_ASSISTANT_MANAGER_BOUNDED'
print('ALL FIREBREAK TESTS PASS')
