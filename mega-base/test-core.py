#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent/'core.py';s=importlib.util.spec_from_file_location('mb',P);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
b=m.MegaBase();assert b.register_tenant('church','SEVEN_FOLD_CHURCH');assert not b.register_tenant('church','OTHER')
church={'authenticated':True,'tenant_id':'church','capabilities':['profile.read','training.write']}
other={'authenticated':True,'tenant_id':'other','capabilities':['profile.read']}
assert b.authorize(church,'church','profile.read');assert not b.authorize(church,'church','admin');assert not b.authorize(other,'church','profile.read')
b.receipt('church','member1','profile.read','ALLOW',1);b.receipt('church','admin1','training.review','ALLOW',2);assert b.verify_chain()
b.events[0]['result']='DENY';assert not b.verify_chain()
print('MEGA BASE CORE PASS')
