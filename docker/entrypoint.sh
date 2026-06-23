#!/usr/bin/env bash
set -euo pipefail

cd /workspace/tampura

# 初回起動または pyproject.toml/setup.py 変更時に依存をインストール
# デフォルト: TAMPURA_AUTO_SYNC=1（自動実行）
# 環境変数で制御可能: docker compose up -e TAMPURA_AUTO_SYNC=0 で無効化
if [[ "${TAMPURA_AUTO_SYNC:-1}" == "1" ]]; then
	CURRENT_HASH="$(sha256sum pyproject.toml setup.py 2>/dev/null | sha256sum | awk '{print $1}')"
	STAMP_FILE="${VIRTUAL_ENV:-/opt/venv}/.tampura-deps.sha256"
	PREVIOUS_HASH="$(cat "${STAMP_FILE}" 2>/dev/null || true)"

	if [[ "${CURRENT_HASH}" != "${PREVIOUS_HASH}" ]]; then
		echo "[entrypoint] Syncing dependencies (uv sync --frozen)..."
		uv sync --frozen
		echo "[entrypoint] Installing project (uv pip install -e .)..."
		uv pip install -e . --verbose
		echo "${CURRENT_HASH}" > "${STAMP_FILE}"
		echo "[entrypoint] Dependencies synced successfully."
	else
		echo "[entrypoint] Dependencies are up-to-date."
	fi
else
	echo "[entrypoint] TAMPURA_AUTO_SYNC=0: Skipping dependency sync."
fi

exec "$@"
