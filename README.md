# TAMPURA

Partially Observable Task and motion planning with uncertainty and risk awareness. See our [paper](https://arxiv.org/abs/2403.10454) or [website](https://aidan-curtis.github.io/tampura.github.io/) for more details.

![alt text](figs/tasks.png)

## Install

### ホスト側に uv/python がある場合

```
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U uv
uv lock --upgrade
uv pip install --frozen -e .
```

### Docker を使う場合

ホスト側には Docker のみあれば十分です。`uv` や `python` は不要です。

詳細は [docker/README.md](docker/README.md) を参照してください。

# Example Notebook

See `notebooks/grasping_env.ipynb` for a simple usage example.

# Robot environments

The robot environments from the paper are in a separate [tampura_environments](https://github.com/aidan-curtis/tampura_environments) repo
