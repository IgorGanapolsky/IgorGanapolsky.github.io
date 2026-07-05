#!/usr/bin/env python3
"""Verify the OpenClaw troubleshooting page promise matches outbound copy.

This intentionally checks the local source, not the deployed site. It prevents
agents from drafting social posts that promise a different count, price, or
diagnostic vocabulary than the page can actually support.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "openclaw-mac-ai-workstation-setup" / "troubleshooting.html"

REQUIRED = [
    "The six real causes",
    "$499 Agent Safety Diagnostic",
    "codex plugin marketplace add",
    "codesign -dv",
    "threshold_inherited_from_primary",
    "AppleScript error -1743",
    "$CODEX_HOME",
    "openclaw --session-key",
]

FORBIDDEN_PATTERNS = [
    ("$19", r"\$19(?!\d)"),
    ("$49", r"\$49(?!\d)"),
    ("$99", r"\$99(?!\d)"),
    ("$497", r"\$497(?!\d)"),
    ("8 patterns", r"\b8 patterns\b"),
    ("eight patterns", r"\beight patterns\b"),
    ("SCStreamErrorDomain -3811", r"SCStreamErrorDomain -3811"),
    ("minos", r"\bminos\b"),
    ("24h marketplace", r"\b24h marketplace\b"),
    ("24-hour marketplace", r"\b24-hour marketplace\b"),
]


def main() -> int:
    html = PAGE.read_text(encoding="utf-8")
    missing = [needle for needle in REQUIRED if needle not in html]
    forbidden_present = [
        label for label, pattern in FORBIDDEN_PATTERNS
        if re.search(pattern, html, flags=re.IGNORECASE)
    ]
    result = {
        "page": str(PAGE),
        "requiredPresent": len(missing) == 0,
        "forbiddenAbsent": len(forbidden_present) == 0,
        "missing": missing,
        "forbiddenPresent": forbidden_present,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not missing and not forbidden_present else 1


if __name__ == "__main__":
    sys.exit(main())
