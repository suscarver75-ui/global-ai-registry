#!/usr/bin/env python3
"""Recovery + authority-promotion gate. Pure evaluation only; grants no authority and performs no mutation."""
LEVELS=('L0_OBSERVE','L1_PREVIEW','L2_CONTROLLED_MUTATION','L3_BOUNDED_AUTOMATION')
REQUIREMENTS={
 'L1_PREVIEW':{'public_boundary','fail_closed_policy'},
 'L2_CONTROLLED_MUTATION':{'public_boundary','fail_closed_policy','preview_evidence','idempotency','replay_protection','state_precondition','command_receipt_binding','receipt_chain_integrity','post_change_verification','rollback_verified','independent_readback'},
 'L3_BOUNDED_AUTOMATION':{'public_boundary','fail_closed_policy','preview_evidence','idempotency','replay_protection','state_precondition','command_receipt_binding','receipt_chain_integrity','post_change_verification','rollback_verified','independent_readback','rate_limit','operation_budget','circuit_breaker','audit_retention_verified'}
}
def promote(current,target,evidence,human_approved=False):
 if current not in LEVELS or target not in LEVELS:return 'DENY_UNKNOWN_LEVEL'
 ci,ti=LEVELS.index(current),LEVELS.index(target)
 if ti<=ci:return 'DENY_INVALID_PROMOTION'
 if ti!=ci+1:return 'DENY_SKIP_LEVEL'
 missing=REQUIREMENTS.get(target,set())-set(evidence)
 if missing:return 'DENY_MISSING_EVIDENCE:' + ','.join(sorted(missing))
 if target in {'L2_CONTROLLED_MUTATION','L3_BOUNDED_AUTOMATION'} and not human_approved:return 'DENY_HUMAN_APPROVAL'
 return 'PROMOTION_ELIGIBLE'
def rollback(before_state,current_state,rollback_result,independent_readback):
 if current_state==before_state:return 'ROLLBACK_NOT_NEEDED'
 if rollback_result!=before_state:return 'ROLLBACK_FAILED'
 if independent_readback!=before_state:return 'ROLLBACK_READBACK_FAILED'
 return 'ROLLBACK_VERIFIED'
