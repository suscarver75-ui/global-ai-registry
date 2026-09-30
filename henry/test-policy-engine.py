#!/usr/bin/env python3
from datetime import datetime, timezone
from pathlib import Path
import importlib.util

ENGINE_PATH = Path(__file__).resolve().parent / "policy-engine.py"
spec = importlib.util.spec_from_file_location("henry_policy_engine", ENGINE_PATH)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
decide = engine.decide

NOW=datetime(2026,9,30,5,0,0,tzinfo=timezone.utc)
def base(**kw):
 c={"command_id":"TEST-001","contract_version":"henry.command-contract.v1","issued_at":"2026-09-30T04:59:00Z","expires_at":"2026-09-30T05:10:00Z","action":"READ_HEALTH","mode":"PREVIEW","target":"henry/health.json","payload":{},"expected_state":None,"idempotency_key":None,"requested_evidence":["decision"]}; c.update(kw); return c
cases=[
 ("allow safe read",base(),False,"ALLOW_PREVIEW"),
 ("deny unknown action",base(action="RUN_ANYTHING"),False,"DENY_UNKNOWN_ACTION"),
 ("deny expired",base(expires_at="2026-09-30T04:00:00Z"),False,"DENY_EXPIRED"),
 ("deny future issued",base(issued_at="2026-09-30T06:00:00Z"),False,"DENY_EXPIRED"),
 ("deny traversal",base(target="henry/../private/brain.json"),False,"DENY_SCOPE"),
 ("deny non-Henry scope",base(target="mac-henry/private.json"),False,"DENY_SCOPE"),
 ("deny private brain data",base(payload={"note":"private Main Brain architecture"}),False,"DENY_PRIVATE_DATA"),
 ("deny hidden reasoning",base(payload={"note":"hidden reasoning"}),False,"DENY_PRIVATE_DATA"),
 ("deny token",base(payload={"token":"ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"}),False,"DENY_SECRET"),
 ("mutation preview only",base(action="PUBLISH_APPROVED_PUBLIC_ARTIFACT",mode="PREVIEW",target="henry/public.json"),False,"ALLOW_PREVIEW"),
 ("deny execute without idempotency",base(action="PUBLISH_APPROVED_PUBLIC_ARTIFACT",mode="EXECUTE",target="henry/public.json"),True,"DENY_PRECONDITION"),
 ("deny execute without preview evidence",base(action="PUBLISH_APPROVED_PUBLIC_ARTIFACT",mode="EXECUTE",target="henry/public.json",idempotency_key="idem-001"),False,"DENY_MISSING_PREVIEW"),
 ("allow gated execute",base(action="PUBLISH_APPROVED_PUBLIC_ARTIFACT",mode="EXECUTE",target="henry/public.json",idempotency_key="idem-001"),True,"ALLOW_EXECUTE"),
]
failed=0
for name,cmd,preview,expected in cases:
 got=decide(cmd,NOW,preview); ok=got==expected; failed+=not ok; print(("PASS" if ok else "FAIL")+f" | {name} | expected={expected} got={got}")
print(f"SUMMARY | {len(cases)-failed}/{len(cases)} passed")
raise SystemExit(1 if failed else 0)
