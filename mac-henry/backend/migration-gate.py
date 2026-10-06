#!/usr/bin/env python3
"""In-place migration gate. Developer-safe; no production connection."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Migration:
 id:str; reversible:bool; backup_verified:bool; compatibility_tested:bool; data_loss_risk:bool=False; owner_approved:bool=False
def decide(m):
 if not (m.id and m.backup_verified and m.compatibility_tested): return "HOLD"
 if m.data_loss_risk and not m.owner_approved:return "OWNER_APPROVAL_REQUIRED"
 if not m.reversible and not m.owner_approved:return "OWNER_APPROVAL_REQUIRED"
 return "ALLOW"
