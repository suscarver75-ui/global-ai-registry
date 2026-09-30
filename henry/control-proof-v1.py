#!/usr/bin/env python3
"""Mac Henry -> Henry End-to-End Control Proof v1.
Simulation only: proves control flow without performing repository/network mutations.
"""
from pathlib import Path
import importlib.util, json
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent

def loadmod(name,path):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
policy=loadmod('policy',ROOT/'policy-engine.py')
guard=loadmod('guard',ROOT/'operation-guard.py')
chain=loadmod('chain',ROOT/'receipts'/'chain.py')
NOW=datetime(2026,9,30,5,30,0,tzinfo=timezone.utc)
command={
 'command_id':'HNY-E2E-001','contract_version':'henry.command-contract.v1','issued_at':'2026-09-30T05:29:00Z','expires_at':'2026-09-30T05:40:00Z',
 'action':'PUBLISH_APPROVED_PUBLIC_ARTIFACT','mode':'EXECUTE','target':'henry/e2e-proof-target.json',
 'payload':{'classification':'CURRENT_PUBLIC','purpose':'End-to-end control proof simulation'},
 'expected_state':'sha256:before','idempotency_key':'HNY-E2E-IDEM-001','requested_evidence':['decision','verification_status','evidence_references']}
steps=[]
def mark(name,ok,detail): steps.append({'step':name,'ok':bool(ok),'detail':detail}); return bool(ok)
preview=policy.decide({**command,'mode':'PREVIEW'},NOW,False,{},'sha256:before')
mark('policy_preview',preview=='ALLOW_PREVIEW',preview)
execute=policy.decide(command,NOW,True,{},'sha256:before')
mark('policy_execute',execute=='ALLOW_EXECUTE',execute)
op={'risk':'LOW','rollback_plan':'restore sha256:before','post_verify':True}
gate=guard.evaluate(op,guard.GuardState())
mark('bounded_operation_guard',gate=='ALLOW_BOUNDED_OPERATION',gate)
# No external mutation occurs. We simulate a deterministic after-state and verify expected evidence flow.
after='sha256:simulated-after-state'; verified=all(s['ok'] for s in steps)
mark('post_change_verification',verified,'VERIFIED' if verified else 'FAILED')
receipt={'receipt_id':'HNY-E2E-R-001','command_id':command['command_id'],'contract_version':command['contract_version'],'action':command['action'],'decision':execute,'target':command['target'],'started_at':'2026-09-30T05:30:00Z','completed_at':'2026-09-30T05:30:01Z','before_state_reference':'sha256:before','after_state_reference':after,'verification_status':'VERIFIED' if verified else 'FAILED','evidence_references':['henry/control-proof-v1.py'],'error_code_if_any':None}
sealed=chain.seal(receipt,command=command)
mark('receipt_command_binding',chain.verify(sealed,command=command),'bound receipt verified')
mark('receipt_chain_integrity',chain.verify_chain([sealed]),'single-receipt genesis chain verified')
result={'schema':'henry.control-proof-result.v1','simulation_only':True,'external_mutation_performed':False,'command_id':command['command_id'],'steps':steps,'overall':'PASS' if all(s['ok'] for s in steps) else 'FAIL','receipt_hash':sealed['receipt_hash'],'command_fingerprint':sealed['command_fingerprint']}
print(json.dumps(result,indent=2)); raise SystemExit(0 if result['overall']=='PASS' else 1)
