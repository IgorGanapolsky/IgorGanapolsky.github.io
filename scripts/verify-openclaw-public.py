#!/usr/bin/env python3
"""Verify public OpenClaw pages serve current revenue telemetry markup."""

from __future__ import annotations

import json
import sys
import urllib.request


URLS = [
    "https://igorganapolsky.github.io/openclaw-mac-ai-workstation-setup/",
    "https://igorganapolsky.github.io/openclaw-mac-ai-workstation-setup/troubleshooting.html",
    "https://igorganapolsky.github.io/openclaw-mac-ai-workstation-setup/computer-use-plugin-unavailable.html",
]

ASSET_URL = "https://igorganapolsky.github.io/assets/revenue-analytics.js"


def fetch(url: str) -> tuple[str, dict[str, str | None]]:
    req = urllib.request.Request(
        url + ("&" if "?" in url else "?") + "public-smoke=1",
        headers={
            "User-Agent": "openclaw-public-smoke/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", "replace"), {
            "status": str(resp.status),
            "last_modified": resp.headers.get("Last-Modified"),
            "etag": resp.headers.get("ETag"),
            "age": resp.headers.get("Age"),
            "x_cache": resp.headers.get("X-Cache"),
        }


def main() -> int:
    results: list[dict[str, object]] = []
    failed = False

    for url in URLS:
        body, headers = fetch(url)
        checks = {
            "has_data_surface": "data-surface=" in body,
            "has_tagged_plausible": "script.tagged-events.js" in body,
            "has_root_revenue_analytics": "/assets/revenue-analytics.js" in body,
            "still_uses_stale_relative_asset": "./assets/revenue-analytics.js" in body,
        }
        ok = (
            checks["has_data_surface"]
            and checks["has_tagged_plausible"]
            and checks["has_root_revenue_analytics"]
        )
        failed = failed or not ok
        results.append(
            {
                "url": url,
                "ok": ok,
                "headers": headers,
                "checks": checks,
            }
        )

    asset_body, asset_headers = fetch(ASSET_URL)
    asset_checks = {
        "has_checkout_abandon_reason": "checkout_abandon_reason" in asset_body,
        "has_offer_objection_click": "offer_objection_click" in asset_body,
        "has_checkout_click": "checkout_click" in asset_body,
    }
    asset_ok = all(asset_checks.values())
    failed = failed or not asset_ok
    results.append(
        {
            "url": ASSET_URL,
            "ok": asset_ok,
            "headers": asset_headers,
            "checks": asset_checks,
        }
    )

    print(json.dumps({"ok": not failed, "results": results}, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
