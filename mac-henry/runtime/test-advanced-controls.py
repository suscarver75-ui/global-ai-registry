#!/usr/bin/env python3
import json
from pathlib import Path
s=json.loads((Path(__file__).resolve().parent/'advanced-controls.json').read_text())
assert s['activation_rule']=='DOCUMENTATION_NEVER_EQUALS_ACTIVE'
assert len(s['systems']['run_mac_henry']['controls'])>=20
assert len(s['systems']['mega_base']['controls'])>=20
assert len(s['deep_controls'])>=35
assert 'future_agent_quarantine' in s['deep_controls'] and 'cost_kill_switch' in s['deep_controls']
print('RUN + MEGA BASE ADVANCED CONTROL SPEC PASS')
