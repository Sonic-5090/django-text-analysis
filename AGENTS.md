# AGENTS.md

## Python Project Setup

- Run with: `python main.py` or `python -m src.runner`
- Install deps: `pip install -r requirements.txt` or `pip install -e .`

## Testing

- Run tests: `pytest` or `python -m pytest`
- Run specific test: `pytest tests/test_file.py::test_function`

## Code Quality

- Lint: `flake8` or `ruff check .`
- Format: `black .` or `ruff format .`
- Typecheck: `mypy .` (if using type hints)

## Project Structure (typical)

```
src/          # Source code
tests/        # Test files
main.py       # Entry point
requirements.txt
pyproject.toml
```

## Virtual Environment

- Create: `python -m venv venv`
- Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)