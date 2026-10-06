#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'security-foundation.json').read_text(encoding='utf-8'))
def check(n,v):
 if not v: raise AssertionError(n)
 print('PASS',n)
check('identity lock',P['identity']['primary_name']=='Seven-Fold Church')
check('expanded identity',P['identity']['expanded_name']=='Seven-Fold Church — Inspired Indigenous Global Church')
check('default deny',P['invariants']['default_access']=='DENY')
check('auth not authorization',P['invariants']['authentication_is_authorization'] is False)
check('private brain excluded',P['invariants']['private_brain_in_github'] is False)
check('secrets excluded',P['invariants']['secrets_in_github'] is False)
check('payment cannot grant credential',P['invariants']['payment_grants_credential'] is False)
check('browser cannot assert training',P['invariants']['browser_claims_training_completion'] is False)
check('public verification isolated',P['invariants']['public_verification_reads_private_profile'] is False)
check('no subordinate escalation',P['invariants']['subordinate_self_escalation'] is False)
for z in ['PUBLIC','MEMBER','MINISTER_STUDENT','CREDENTIALED_LEADER','ADMIN','HENRY','MAC_HENRY_OWNER']: check('zone '+z,z in P['zones'])
for d in ['identity','membership','messages','training-records','assessments','credentials','good-standing','charters','moderation','consent','payments','audit-evidence']: check('protected '+d,d in P['protected_domains'])
for c in ['identity','authorization','credentials','privacy','security','operations','ai']: check('control family '+c,bool(P['controls'][c]))
check('truth rule',P['truth_rule']=='DOCUMENTED != BUILT != CONNECTED != EXECUTED != VERIFIED != PROVEN')
print('ALL CHURCH SECURITY FOUNDATION TESTS PASS')
