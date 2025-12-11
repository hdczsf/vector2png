# Contributing

## Setup
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[full,dev]"
```

## Tests
```bash
PYTHONPATH=. pytest -q
```

## Coding guidelines
- Keep dependencies optional; use `optional_import` with clear hints.
- Preserve dataclass-based options and clear defaults.
- Favor small, readable functions; add brief comments only when logic is non-obvious.
- Maintain transparency/background precedence rules consistently across pipelines.

## Documentation
- Update `README.md`/`README.cn.md` and relevant `docs/*.md` when changing behavior or options.

## Releases
- Bump version in `pyproject.toml` when publishing.
- Ensure optional extras remain correct (`[ai]`, `[dxf]`, `[full]`).
- Run tests before tagging. 
