#!/usr/bin/env python3
import importlib.util,sys
from pathlib import Path
P=Path(__file__).resolve().parent/'payment-boundary.py';s=importlib.util.spec_from_file_location('pb',P);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
x=m.PaymentLedger();rid=x.record_provider_event('DONATION',2500,'evt-1',subject_id='m1',now=100);assert rid
assert x.record_provider_event('DONATION',2500,'evt-1',subject_id='m1',now=101)==rid
a=x.authority_projection(rid);assert all(a[k] is False for k in ['grants_role','grants_credential','grants_good_standing','grants_charter'])
assert x.record_provider_event('DONATION',-1,'evt-2') is None
assert x.record_provider_event('DONATION',100,'evt-3','PAID') is None
print('CHURCH PAYMENT AUTHORITY BOUNDARY PASS')
