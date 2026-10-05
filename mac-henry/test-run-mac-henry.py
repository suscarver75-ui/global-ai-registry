#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("runner",ROOT/"run-mac-henry.py")
runner=importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)

def state(items): return {"schema":"mac-henry.run-state.v1","departments":items}
def item(dept,priority,status="READY",risk="R0",approval=False,evidence=None,action="Act"):
 return {"department":dept,"priority_class":priority,"status":status,"risk":risk,"approval_required":approval,"evidence_refs":evidence or ["evidence:test"],"recommended_next_action":action}

def check(name,condition):
 if not condition: raise AssertionError(name)
 print("PASS",name)

# Security outranks ordinary strategy.
r=runner.run(state([item("Growth","STRATEGIC_IMPROVEMENT"),item("Security","SAFETY_SECURITY",action="Contain risk")]))
check("security priority",r["department"]=="Security" and r["next_best_move"]=="Contain risk")
# High risk always requires Owner approval.
r=runner.run(state([item("Finance","VERIFIED_REVENUE",risk="R3",action="Review transaction")]))
check("high risk approval gate",r["decision"]=="APPROVAL_NEEDED" and r["approval_required"] is True)
# Missing evidence fails closed.
r=runner.run(state([{"department":"Build","priority_class":"BLOCKERS","status":"READY","risk":"R0","approval_required":False,"evidence_refs":[],"recommended_next_action":"Build"}]))
check("evidence required",r["decision"]=="HOLD" and any("EVIDENCE_REQUIRED" in e for e in r["errors"]))
# Unknown status fails closed.
r=runner.run(state([item("Build","BLOCKERS",status="MAGIC")]))
check("unknown status denied",r["decision"]=="HOLD")
# Resolved state reports verified/no unresolved work.
r=runner.run(state([item("Done","STRATEGIC_IMPROVEMENT",status="VERIFIED")]))
check("verified idle state",r["decision"]=="READY" and r["status"]=="VERIFIED")
# Core ten preserved.
s=runner.load_spec(); check("core ten preserved",len(s["core_10_light_years_ahead"])==10)
# Public/private firebreak asserted.
check("private brain excluded",s["public_private_firebreak"]["private_brain_in_repository"] is False)
print("ALL RUN MAC HENRY TESTS PASS")
