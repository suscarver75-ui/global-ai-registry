#!/usr/bin/env python3
"""Henry public-safe provenance verifier. Standard-library only."""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parent
TESTS = ROOT / "provenance-tests"
REGISTRY = "LoAI-2024-0414-001"

checks = []
def check(name, ok, detail=""):
    checks.append((name, bool(ok), detail))

def load(p):
    return p.read_text(encoding="utf-8")

# Henry console
html = load(ROOT / "index.html")
prov = json.loads(load(ROOT / "provenance.json"))
check("console artifact id", prov.get("artifact_id") in html, prov.get("artifact_id", ""))
check("console registry", prov.get("registry") == REGISTRY and REGISTRY in html, REGISTRY)
check("console public boundary", prov.get("boundary") == "PUBLIC_SAFE", str(prov.get("boundary")))
check("console no private authority", prov.get("authority") == "NO_PRIVATE_AUTHORITY", str(prov.get("authority")))
check("console canonical path", prov.get("artifact_path") == "henry/index.html", str(prov.get("artifact_path")))

# Document test
doc = load(TESTS / "HNY-DOCUMENT-TEST-001.md")
for token in ["HNY-DOCUMENT-TEST-001", REGISTRY, "CURRENT_PUBLIC", "PUBLIC_SAFE", "HNY-01"]:
    check(f"document token {token}", token in doc)

# SVG image test
svg = load(TESTS / "HNY-IMAGE-TEST-001.svg")
for token in ["HNY-IMAGE-TEST-001", REGISTRY, "PUBLIC_SAFE", "henry.public-provenance.v1", "HNY-01"]:
    check(f"image token {token}", token in svg)

# Product manifest
product = json.loads(load(TESTS / "HNY-PRODUCT-TEST-001.manifest.json"))
check("product artifact", product.get("artifact_id") == "HNY-PRODUCT-TEST-001")
check("product registry", product.get("registry") == REGISTRY)
check("product boundary", product.get("boundary") == "PUBLIC_SAFE")
check("product no private authority", product.get("package_policy", {}).get("private_authority") is False)

# Video manifest: do not overclaim rendered video verification
video = json.loads(load(TESTS / "HNY-VIDEO-TEST-001.manifest.json"))
check("video artifact", video.get("artifact_id") == "HNY-VIDEO-TEST-001")
check("video registry", video.get("registry") == REGISTRY)
check("video boundary", video.get("boundary") == "PUBLIC_SAFE")
check("video honesty state", video.get("verification_status") == "MANIFEST_VERIFIED_ONLY", str(video.get("verification_status")))

# Basic public-secret hygiene: flag common credential assignment patterns.
public_files = [ROOT / "index.html", ROOT / "provenance.json", *TESTS.iterdir()]
secret_patterns = [
    re.compile(r"(?i)(api[_-]?key|secret|password|private[_-]?key)\s*[=:]\s*['\"][^'\"]{8,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
]
for p in public_files:
    text = load(p)
    hit = any(pattern.search(text) for pattern in secret_patterns)
    check(f"secret hygiene {p.name}", not hit)

failed = [c for c in checks if not c[1]]
for name, ok, detail in checks:
    print(("PASS" if ok else "FAIL") + " | " + name + (" | " + detail if detail else ""))
print(f"SUMMARY | {len(checks)-len(failed)}/{len(checks)} passed")
sys.exit(1 if failed else 0)
