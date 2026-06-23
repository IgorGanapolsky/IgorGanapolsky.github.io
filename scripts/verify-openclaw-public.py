#!/usr/bin/env python3
"""Verify public OpenClaw pages serve current revenue telemetry markup."""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request


URLS = [
    "https://igorganapolsky.com/openclaw-mac-ai-workstation-setup/",
    "https://igorganapolsky.com/openclaw-mac-ai-workstation-setup/troubleshooting.html",
    "https://igorganapolsky.com/openclaw-mac-ai-workstation-setup/computer-use-plugin-unavailable.html",
    "https://igorganapolsky.com/openclaw-mac-ai-workstation-setup/agent-safety-diagnostic.html",
    "https://igorganapolsky.com/openclaw-mac-ai-workstation-setup/quick-read.html",
    "https://igorganapolsky.com/openclaw-mac-ai-workstation-setup/codex-computer-use-intel-mac.html",
    "https://igorganapolsky.com/openclaw-mac-ai-workstation-setup/claude-code-computer-use.html",
    "https://igorganapolsky.com/openclaw-mac-ai-workstation-setup/speed-to-lead.html",
    "https://igorganapolsky.com/openclaw-agent-safety-diagnostic.html",
    "https://igorganapolsky.com/openclaw-agent-safety-sample.html",
]

ASSET_URL = "https://igorganapolsky.com/assets/revenue-analytics.js"


def fetch(url: str) -> tuple[str, dict[str, str | None]]:
    cachebuster = str(int(time.time() * 1000))
    req = urllib.request.Request(
        url + ("&" if "?" in url else "?") + f"public-smoke={cachebuster}",
        headers={
            "User-Agent": "openclaw-public-smoke/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", "replace"), {
                "status": str(resp.status),
                "last_modified": resp.headers.get("Last-Modified"),
                "etag": resp.headers.get("ETag"),
                "age": resp.headers.get("Age"),
                "x_cache": resp.headers.get("X-Cache"),
                "error": None,
            }
    except urllib.error.HTTPError as exc:
        return exc.read().decode("utf-8", "replace"), {
            "status": str(exc.code),
            "last_modified": exc.headers.get("Last-Modified"),
            "etag": exc.headers.get("ETag"),
            "age": exc.headers.get("Age"),
            "x_cache": exc.headers.get("X-Cache"),
            "error": exc.reason,
        }


def parse_args(argv: list[str]) -> tuple[int, float]:
    attempts = 1
    delay = 15.0
    for i, arg in enumerate(argv):
        if arg == "--attempts" and i + 1 < len(argv):
            attempts = int(argv[i + 1])
        if arg == "--delay" and i + 1 < len(argv):
            delay = float(argv[i + 1])
    return max(1, attempts), max(0.0, delay)


def run_once() -> tuple[bool, list[dict[str, object]]]:
    results: list[dict[str, object]] = []
    failed = False

    for url in URLS:
        body, headers = fetch(url)
        requires_telemetry = (
            url.endswith("/quick-read.html")
            or url.endswith("/speed-to-lead.html")
            or url.endswith("/troubleshooting.html")
            or url.endswith("/computer-use-plugin-unavailable.html")
            or url.endswith("/codex-computer-use-intel-mac.html")
            or url.endswith("/claude-code-computer-use.html")
            or url.endswith("/openclaw-agent-safety-diagnostic.html")
            or url.endswith("/openclaw-agent-safety-sample.html")
        )
        checks = {
            "has_data_surface": "data-surface=" in body,
            "has_tagged_plausible": "script.tagged-events.js" in body,
            "has_root_revenue_analytics": "/assets/revenue-analytics.js" in body,
            "still_uses_stale_relative_asset": "./assets/revenue-analytics.js" in body,
            "has_stripe_checkout": "https://buy.stripe.com/" in body,
            "has_speed_to_lead_fallback": "./speed-to-lead.html" in body,
            "is_stale_agent_diagnostic_404": (
                url.endswith("/agent-safety-diagnostic.html") and headers["status"] == "404"
            ),
            "has_redirect_or_revenue_markup": (
                "http-equiv=\"refresh\"" in body
                or ("data-surface=" in body and "/assets/revenue-analytics.js" in body)
                or "https://buy.stripe.com/" in body
                or "./speed-to-lead.html" in body
            ),
            "telemetry_required": requires_telemetry,
            "telemetry_ok": (
                "script.tagged-events.js" in body
                and "/assets/revenue-analytics.js" in body
                and "data-track=" in body
            ),
        }
        ok = (checks["has_redirect_or_revenue_markup"] or checks["is_stale_agent_diagnostic_404"]) and (
            not requires_telemetry
            or checks["telemetry_ok"]
            or checks["is_stale_agent_diagnostic_404"]
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

    return not failed, results


def main(argv: list[str]) -> int:
    attempts, delay = parse_args(argv)
    last_results: list[dict[str, object]] = []
    for attempt in range(1, attempts + 1):
        ok, results = run_once()
        last_results = results
        print(json.dumps({"attempt": attempt, "ok": ok, "results": results}, indent=2))
        if ok:
            return 0
        if attempt < attempts:
            time.sleep(delay)
    print(
        json.dumps(
            {
                "ok": False,
                "attempts": attempts,
                "failure": "public_openclaw_telemetry_stale_after_retries",
                "last_results": last_results,
            },
            indent=2,
        )
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
