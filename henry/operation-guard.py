#!/usr/bin/env python3
"""Bounded public-operation guard. Pure policy/state evaluation; performs no external action."""
from dataclasses import dataclass

@dataclass
class GuardState:
    window_count:int=0
    consecutive_failures:int=0
    circuit_open:bool=False

DEFAULTS={
    'max_operations_per_window':5,
    'max_consecutive_failures':2,
    'allowed_risk':['LOW'],
    'require_rollback_plan':True,
    'require_post_verify':True,
}

def evaluate(operation,state,policy=None):
    p={**DEFAULTS,**(policy or {})}
    if state.circuit_open:return 'DENY_CIRCUIT_OPEN'
    if operation.get('risk') not in p['allowed_risk']:return 'DENY_RISK'
    if state.window_count>=p['max_operations_per_window']:return 'DENY_BUDGET'
    if p['require_rollback_plan'] and not operation.get('rollback_plan'):return 'DENY_NO_ROLLBACK'
    if p['require_post_verify'] and not operation.get('post_verify'):return 'DENY_NO_VERIFY'
    return 'ALLOW_BOUNDED_OPERATION'

def record_result(state,success,policy=None):
    p={**DEFAULTS,**(policy or {})}; state.window_count+=1
    state.consecutive_failures=0 if success else state.consecutive_failures+1
    if state.consecutive_failures>=p['max_consecutive_failures']:state.circuit_open=True
    return state
