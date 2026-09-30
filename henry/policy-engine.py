#!/usr/bin/env python3
"""Henry public-safe command policy engine. Validation only; performs no mutations."""
from __future__ import annotations
import json, re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTRACT = json.loads((ROOT / "command-contract.json").read_text(encoding="utf-8"))
ACTIONS = {a["id"]: a for a in CONTRACT["allowed_actions"]}
SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)(api[_-]?key|password|private[_-]?key|seed[_-]?phrase)\s*[=:]\s*[^\s,}]{8,}"),
]
PRIVATE_TERMS = ("private main brain", "hidden reasoning", "chain of thought", "private prompt", "wallet seed", "seed phrase")

def parse_time(value):
    if not isinstance(value, str): return None
    try: return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError: return None

def decide(command, now=None, preview_evidence=False):
    now = now or datetime.now(timezone.utc)
    action = command.get("action")
    if action not in ACTIONS: return "DENY_UNKNOWN_ACTION"
    if command.get("contract_version") != CONTRACT["schema"]: return "DENY_PRECONDITION"
    exp = parse_time(command.get("expires_at")); issued = parse_time(command.get("issued_at"))
    if not exp or not issued or exp <= now or issued > now: return "DENY_EXPIRED"
    target = str(command.get("target", ""))
    if not target.startswith("henry/") or ".." in target or target.startswith("henry/../"): return "DENY_SCOPE"
    text = json.dumps(command.get("payload", {}), sort_keys=True)
    low = text.lower()
    if any(term in low for term in PRIVATE_TERMS): return "DENY_PRIVATE_DATA"
    if any(p.search(text) for p in SECRET_PATTERNS): return "DENY_SECRET"
    spec = ACTIONS[action]
    mode = command.get("mode")
    if spec.get("mutation"):
        if mode != "EXECUTE": return "ALLOW_PREVIEW" if mode == "PREVIEW" else "DENY_PRECONDITION"
        if not command.get("idempotency_key"): return "DENY_PRECONDITION"
        if spec.get("preview_required") and not preview_evidence: return "DENY_MISSING_PREVIEW"
        return "ALLOW_EXECUTE"
    return "ALLOW_PREVIEW" if mode == "PREVIEW" else "ALLOW_EXECUTE"

if __name__ == "__main__":
    import sys
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(decide(data))
