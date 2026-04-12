# Docker (uv + pyproject.toml)

このディレクトリの構成は、`conda` を使わずに `uv` で `pyproject.toml` の依存を解決して、ローカル開発用コンテナを起動するためのものです。

## 1. 目的

- 依存管理はプロジェクト本体の `pyproject.toml` をそのまま使用
- `uv pip install -e .` で editable install
- SSH / VNC は使わず、ローカルで `docker compose exec` する前提
- 重い依存（例: torch）は **Docker build 時にインストール済み** を再利用

## 2. 初回セットアップ

### 2.1 `.env` を作成（オプション）

ホスト側の `UID`/`GID` を指定する場合、`.env` を作成してください：

```bash
cd docker
cp .env.example .env
```

編集して `UID`/`GID` をホスト側に合わせてください（マウント先の権限ズレ防止）。

### 2.2 初回ビルド

```bash
cd docker
docker compose build
```

- イメージにはベースツールのみ含まれます
- `uv.lock` はコンテナ内にコピーされます

### 2.3 依存をインストール（手動実行）

コンテナを起動し、entrypoint.sh が自動的に依存をインストールします：

```bash
docker compose up
```

- 初回起動時に `uv sync --frozen` と `uv pip install -e .` が自動実行
- 2回目以降は pyproject.toml/setup.py に変更がなければスキップ
- ログに `[entrypoint] Dependencies synced successfully.` と表示されたら完了

コンテナにシェルで入る場合:

```bash
docker compose exec tampura bash
```

## 3. 依存の管理と更新

### 3.1 `pyproject.toml` 編集後の手順

`pyproject.toml` に新しい依存を追加した場合：

1. **`uv.lock` を更新** （ホスト側 / または コンテナ内）:
   
   **ホスト側に uv がある場合:**
   ```bash
   cd /path/to/tampura
   uv lock --upgrade
   ```
   
   **ホスト側に uv がない場合:**
   ```bash
   cd docker
   docker compose run --rm tampura uv lock --upgrade
   ```
   生成された `uv.lock` はホスト側の `tampura/` に自動反映されます（`/workspace` マウント）

2. **git に commit**:
   ```bash
   git add uv.lock
   git commit -m "Update dependencies with [package name]"
   ```

3. **イメージ再ビルド**:
   ```bash
   cd docker
   docker compose up --build
   ```
   - 新しい `uv.lock` が Dockerfile にコピーされ、ビルド時に使用されます

### 3.2 起動時の自動依存同期

デフォルトでは `TAMPURA_AUTO_SYNC=1` なため、以下が自動実行されます：

- **初回起動時**: `uv sync --frozen` と `uv pip install -e .` を実行
- **以降の起動時**: pyproject.toml/setup.py に変更がなければスキップ
- **ログ確認**: `[entrypoint] Dependencies synced successfully.` を確認

自動同期を無効化したい場合：

```bash
docker compose up -e TAMPURA_AUTO_SYNC=0
```

## 4. 動作確認

```bash
docker compose exec tampura python -c "import tampura; print('ok')"
```

```bash
# @ workspace/tampura/
cd ..

# @ workspace/
uv run python tampura_environments/run_planner.py --config=./tampura_environments/env_configs/find_dice.yml --vis=1 --global-seed=0 --vis-graph=1
```

