# Contributing

Thanks for considering a contribution to 13Recon.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
ruff check .
```

## Pull requests

Keep changes focused, add tests for behavior you change, and document user-facing options.
