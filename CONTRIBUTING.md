# Contributing

Thanks for helping improve this teaching repo!

## Quick start

1. Fork & clone.
2. Install `uv` (`curl -LsSf https://astral.sh/uv/install.sh | sh` on Linux/macOS, or PowerShell on Windows), then:
   ```bash
   uv sync                  # creates .venv + installs deps
   ```
3. Run `uv run python examples/01-lennard-jones-fluid/run.py` — should finish in <5 s.
4. Make your change on a feature branch, open a PR.

## What we welcome

- Clearer explanations / figures (especially in `docs/` and `slides/`).
- New examples that follow the 7-step workflow and include a README.
- Bug fixes, typo fixes, better error messages.
- Tests for examples (energy conservation, determinism with seed).

## Style

- Examples: pure Python + NumPy where possible; optional deps behind `try/except ImportError`.
- Keep each example self-contained with its own `README.md`.
- Use reduced LJ units in toy examples (document the mapping to real units).
- Cite sources for non-trivial equations.

## Code of Conduct

Be kind, be constructive. This is a learning resource.
