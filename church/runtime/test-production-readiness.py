#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent/'production-readiness.py';s=importlib.util.spec_from_file_location('pr',P);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
e={k:'configured' for k in m.REQUIRED};e.update({k:'secret-value' for k in m.SECRET_NAMES});r=m.assess(e);assert r['ready'] and r['secret_values_exposed'] is False and 'secret-value' not in str(r)
e.pop('CHURCH_DATABASE_PROVIDER');assert not m.assess(e)['ready']
e['CHURCH_DATABASE_PROVIDER']='placeholder';assert not m.assess(e)['ready']
print('CHURCH PRODUCTION READINESS GATE PASS')
