#!/usr/bin/env python3
"""RUN MAC HENRY — developer-safe orchestration core.

This module deliberately does not contain private Brain data or credentials and
performs no external mutation. It compiles bounded system state into an
Owner-facing next-best-move decision with evidence and approval gating.
"""
from __future__ import annotations
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SPEC_PATH = ROOT / "runtime-spec.json"
ALLOWED_STATUS = {"ACTIVE","READY","BUILDING","PLANNED","BLOCKED","DEGRADED","CONTAINED","VERIFIED","ARCHIVED"}
RISK = {"R0":0,"R1":1,"R2":2,"R3":3}
PRIORITY = {
    "SAFETY_SECURITY": 700,
    "OWNER_LEGAL_OBLIGATIONS": 600,
    "ASSET_PROTECTION": 500,
    "VERIFIED_REVENUE": 400,
    "BLOCKERS": 300,
    "DEADLINES": 200,
    "STRATEGIC_IMPROVEMENT": 100,
}


def load_spec() -> dict[str, Any]:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def fingerprint(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def validate_state(state: dict[str, Any]) -> list[str]:
    errors=[]
    if not isinstance(state, dict): return ["STATE_NOT_OBJECT"]
    if state.get("schema") != "mac-henry.run-state.v1": errors.append("BAD_SCHEMA")
    if not isinstance(state.get("departments"), list): errors.append("DEPARTMENTS_REQUIRED")
    for i, item in enumerate(state.get("departments", [])):
        if item.get("status") not in ALLOWED_STATUS: errors.append(f"BAD_STATUS:{i}")
        if item.get("risk", "R0") not in RISK: errors.append(f"BAD_RISK:{i}")
        if item.get("priority_class") not in PRIORITY: errors.append(f"BAD_PRIORITY:{i}")
        if not item.get("evidence_refs"): errors.append(f"EVIDENCE_REQUIRED:{i}")
    return errors


def score(item: dict[str, Any]) -> int:
    value = PRIORITY[item["priority_class"]]
    value += RISK[item.get("risk", "R0")] * 25
    if item["status"] in {"BLOCKED","DEGRADED","CONTAINED"}: value += 40
    if item.get("money_impact") == "POSITIVE_VERIFIED": value += 20
    if item.get("deadline_urgent"): value += 15
    return value


def run(state: dict[str, Any]) -> dict[str, Any]:
    spec=load_spec(); errors=validate_state(state)
    correlation_id="MH-RUN-" + fingerprint(state).split(":",1)[1][:16].upper()
    if errors:
        return {"schema":"mac-henry.run-result.v1","correlation_id":correlation_id,"decision":"HOLD","status":"BLOCKED","errors":errors,"external_mutation_performed":False}
    candidates=[d for d in state["departments"] if d["status"] not in {"ARCHIVED","VERIFIED"}]
    if not candidates:
        return {"schema":"mac-henry.run-result.v1","correlation_id":correlation_id,"decision":"READY","status":"VERIFIED","next_best_move":"No unresolved bounded work. Continue health monitoring.","approval_required":False,"external_mutation_performed":False,"evidence_refs":["mac-henry/runtime-spec.json"]}
    ranked=sorted(candidates,key=lambda x:(score(x),x.get("department","")),reverse=True)
    chosen=ranked[0]
    approval=bool(chosen.get("approval_required")) or chosen.get("risk") in {"R2","R3"}
    decision="APPROVAL_NEEDED" if approval else "READY"
    result={
        "schema":"mac-henry.run-result.v1",
        "correlation_id":correlation_id,
        "decision":decision,
        "status":chosen["status"],
        "department":chosen.get("department"),
        "next_best_move":chosen.get("recommended_next_action"),
        "priority_class":chosen["priority_class"],
        "risk":chosen.get("risk","R0"),
        "approval_required":approval,
        "external_mutation_performed":False,
        "evidence_refs":chosen["evidence_refs"],
        "truth_rule":spec["truth_rule"],
        "state_fingerprint":fingerprint(state),
        "generated_at":datetime.now(timezone.utc).isoformat(),
    }
    return result


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: run-mac-henry.py STATE.json", file=sys.stderr); return 2
    try:
        state=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result=run(state)
    except Exception as exc:
        result={"schema":"mac-henry.run-result.v1","decision":"HOLD","status":"BLOCKED","error":"FAIL_CLOSED:"+type(exc).__name__,"external_mutation_performed":False}
    print(json.dumps(result,indent=2))
    return 0 if result.get("decision") != "HOLD" else 1

if __name__ == "__main__": raise SystemExit(main())
