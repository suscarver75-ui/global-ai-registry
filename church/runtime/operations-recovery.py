#!/usr/bin/env python3
"""Developer-safe Church operational health/recovery gate."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Check:
 name:str; healthy:bool; evidence:str
REQUIRED=('identity','authorization','protected_data','training','credentials','community_safety','charters','payment_boundary','backup_restore')
def assess(checks):
 by={c.name:c for c in checks}; missing=[n for n in REQUIRED if n not in by]
 failed=[n for n in REQUIRED if n in by and (not by[n].healthy or not by[n].evidence)]
 status='HEALTHY' if not missing and not failed else 'DEGRADED'
 return {'status':status,'safe_mode':status!='HEALTHY','missing':missing,'failed':failed,'promotion_allowed':status=='HEALTHY','evidence':{n:by[n].evidence for n in REQUIRED if n in by}}
def recovery_decision(pre_restore_integrity,restore_tested,post_restore_integrity):
 ok=bool(pre_restore_integrity and restore_tested and post_restore_integrity)
 return {'recovery_verified':ok,'resume_mutations':ok,'mode':'NORMAL' if ok else 'SAFE_READ_ONLY'}
