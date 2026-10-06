#!/usr/bin/env python3
import json,importlib.util,sys
from pathlib import Path
D=Path(__file__).resolve().parent
s=json.loads((D/'platform-spec.json').read_text())
assert s['upgrade_mode']=='IN_PLACE_NEVER_RESTART' and len(s['principles'])==10
assert s['invariants']['private_brain_in_repo'] is False and s['invariants']['production_secrets_in_repo'] is False
assert s['invariants']['deny_by_default'] and s['invariants']['provider_independent']
p=D/'migration-gate.py';sp=importlib.util.spec_from_file_location('mg',p);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
assert m.decide(m.Migration('m1',True,True,True))=='ALLOW'
assert m.decide(m.Migration('m2',True,False,True))=='HOLD'
assert m.decide(m.Migration('m3',False,True,True))=='OWNER_APPROVAL_REQUIRED'
assert m.decide(m.Migration('m4',True,True,True,True))=='OWNER_APPROVAL_REQUIRED'
print('SOVEREIGN BACKEND FOUNDATION PASS')
