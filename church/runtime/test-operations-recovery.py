#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent/'operations-recovery.py';s=importlib.util.spec_from_file_location('op',P);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
good=[m.Check(n,True,'ci:'+n) for n in m.REQUIRED];a=m.assess(good);assert a['status']=='HEALTHY' and a['promotion_allowed'] and not a['safe_mode']
bad=good[:-1];a=m.assess(bad);assert a['status']=='DEGRADED' and a['safe_mode'] and not a['promotion_allowed'] and 'backup_restore' in a['missing']
bad2=[m.Check(n,n!='credentials','ci:'+n) for n in m.REQUIRED];assert 'credentials' in m.assess(bad2)['failed']
assert m.recovery_decision(True,True,True)['resume_mutations'];assert m.recovery_decision(True,False,True)['mode']=='SAFE_READ_ONLY'
print('CHURCH OPERATIONS RECOVERY GATE PASS')
