#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent/'henry-health-signal.py';s=importlib.util.spec_from_file_location('hh',P);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
good={'component':'training','status':'HEALTHY','verification_level':'V3','last_check':'2026-10-05','open_blockers':[],'evidence_ref':'ci:123'}
v=m.henry_view([good]);assert v['private_brain_shared'] is False and v['signals'][0]['component']=='training'
for bad in [dict(good,email='x@example.test'),dict(good,subject_id='s1'),dict(good,secret='x'),dict(good,private_brain='x')]:
 try:m.henry_view([bad]);raise AssertionError('protected field accepted')
 except ValueError:pass
extra=dict(good,internal_note='drop-me');assert 'internal_note' not in m.henry_view([extra])['signals'][0]
print('HENRY SANITIZED CHURCH HEALTH SIGNAL PASS')
