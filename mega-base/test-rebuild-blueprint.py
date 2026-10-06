#!/usr/bin/env python3
import json
from pathlib import Path
s=json.loads((Path(__file__).resolve().parent/'rebuild-blueprint.json').read_text())
i=s['independence'];assert all(i[k] for k in ['future_build_must_not_require_private_instance','no_shared_production_trust_root','no_shared_keys','no_shared_secrets','no_shared_private_data','architecture_reusable'])
assert s['current_use']=='PRIVATE_ONLY'
assert len(s['required_catalog'])>=21 and len(s['per_component_definition'])>=18
assert s['protected_domains']['mac_henry_brain']=='COMPARTMENTALIZED_NEVER_PUBLIC'
assert 'PRODUCTION_CONNECTED' in s['truth']
print('MEGA BASE REBUILD BLUEPRINT PASS')
