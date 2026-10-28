#!/usr/bin/env bash
# Dayglass v2.1.0 — 1-Command macOS Installer
# Usage: curl -fsSL https://igorganapolsky.github.io/dayglass-mac/install.sh | bash
set -euo pipefail

VERSION="2.1.0"
DMG_URL="https://github.com/IgorGanapolsky/homebrew-dayglass/releases/download/v${VERSION}/Dayglass.dmg"
EXPECTED_SHA256="769a66d2b6580f2ec36f348ec8524c1d7876ad55aecb9c25fe0b9b89c0abc877"
APP_DEST="${DAYGLASS_INSTALL_APP_DIR:-/Applications/Dayglass.app}"
TMP_DMG="$(mktemp /tmp/Dayglass-installer-XXXXXX.dmg)"
MOUNT_DIR="$(mktemp -d /tmp/Dayglass-mount-XXXXXX)"

cleanup() {
  hdiutil detach "${MOUNT_DIR}" -quiet 2>/dev/null || true
  rm -rf "${TMP_DMG}" "${MOUNT_DIR}" 2>/dev/null || true
}
trap cleanup EXIT

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "Error: Dayglass requires macOS (Darwin)." >&2
  exit 1
fi

echo "==> [1/4] Downloading Dayglass v${VERSION} for macOS..."
curl -fL --progress-bar "${DMG_URL}" -o "${TMP_DMG}"

echo "==> [2/4] Verifying SHA-256 checksum..."
ACTUAL_SHA256="$(shasum -a 256 "${TMP_DMG}" | awk '{print $1}')"
if [[ "${ACTUAL_SHA256}" != "${EXPECTED_SHA256}" ]]; then
  echo "Error: SHA-256 mismatch! Expected ${EXPECTED_SHA256}, got ${ACTUAL_SHA256}" >&2
  exit 1
fi

echo "==> [3/4] Installing Dayglass.app to ${APP_DEST}..."
rmdir "${MOUNT_DIR}" 2>/dev/null || true
hdiutil attach "${TMP_DMG}" -nobrowse -readonly -mountpoint "${MOUNT_DIR}" -quiet
rm -rf "${APP_DEST}"
cp -R "${MOUNT_DIR}/Dayglass.app" "${APP_DEST}"
hdiutil detach "${MOUNT_DIR}" -quiet || true

echo "==> [4/4] Clearing macOS Gatekeeper quarantine & registering LaunchServices..."
xattr -dr com.apple.quarantine "${APP_DEST}" 2>/dev/null || true
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "${APP_DEST}" 2>/dev/null || true

# Anonymous install telemetry ping to PostHog
curl -fsS -m 3 -X POST "https://us.i.posthog.com/capture/" \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"phc_ub5A4JPFsB2dm54Vaq2dWGeDh9zouzLL4Vb6TcicJxvf\",\"event\":\"app_installed_via_script\",\"distinct_id\":\"dg-cli-$(uuidgen | tr '[:upper:]' '[:lower:]' | cut -c1-12)\",\"properties\":{\"version\":\"${VERSION}\",\"arch\":\"$(uname -m)\",\"utm_source\":\"install_sh\"}}" >/dev/null 2>&1 || true

echo ""
echo "✅ Dayglass v${VERSION} installed at ${APP_DEST}"
if [[ "${DAYGLASS_NO_OPEN:-0}" != "1" ]]; then
  echo "==> Launching Dayglass.app..."
  open "${APP_DEST}" || true
fi
