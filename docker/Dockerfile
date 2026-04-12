FROM python:3.11-slim

ARG USER_NAME=tampura
ARG UID=1000
ARG GID=1000

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # uv lock からの再現可能なビルドを確保
    UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    curl \
    sudo \
    # ---- Autotools ------------------------------------------------------
    # SymK が内部でビルドする libcudd の configure ステップで autoreconf が必要
    autoconf \
    automake \
    libtool \
    # ---- TLS/ビルド基盤 -------------------------------------------------
    # ca-certificates: HTTPS で安全にパッケージ取得（pip/uv/git など）
    ca-certificates \
    # pkg-config: ネイティブ拡張ビルド時に C/C++ ライブラリ情報を解決
    pkg-config \
    # ---- 幾何系 Python パッケージ依存 ----------------------------------
    # libspatialindex-dev: rtree など空間インデックス依存のビルド/実行に必要
    libspatialindex-dev \
    # ---- OpenGL / ヘッドレス描画ランタイム -----------------------------
    # libgl1: OpenGL 基本ランタイム（pybullet/open3d 等）
    libgl1 \
    # libglib2.0-0: Open3D/GUI 依存ライブラリの共通基盤
    libglib2.0-0 \
    # libsm6/libxext6/libxrender1: X11 系共有ライブラリ（オフスクリーン描画含む）
    libsm6 \
    libxext6 \
    libxrender1 \
    # libgomp1: OpenMP ランタイム（数値計算系ライブラリの並列化）
    libgomp1 \
    # libegl1: EGL 経由のヘッドレス GPU/GL コンテキスト
    libegl1 \
    # graphviz & libgraphviz-dev: pygraphviz のビルドに必要
    # graphviz-dev \
    graphviz libgraphviz-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN if ! getent group ${GID} >/dev/null; then groupadd -g ${GID} ${USER_NAME}; fi \
    && if ! id -u ${UID} >/dev/null 2>&1; then useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER_NAME}; fi
# --- For ubuntu user ---
RUN echo "$USER_NAME:password" | chpasswd && adduser $USER_NAME sudo

# sudo 実行時にパスワード不要にする（entrypoint.sh での service 起動に必要）
RUN echo "$USER_NAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ENV UV_PYTHON=/opt/venv/bin/python

WORKDIR /workspace/tampura

# ビルド時にはベースツールのみをインストール
# 依存同期（uv sync --frozen）と editable install（uv pip install -e .）は
# 起動時に entrypoint.sh が実行する（compose で /workspace をマウント前提）
RUN uv pip install --upgrade pip setuptools wheel

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh \
    && chown -R ${UID}:${GID} /workspace /opt/venv

USER ${USER_NAME}
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
