
.PHONY: install test lint format

install:
	rye sync

test:
	pytest -v

lint:
	ruff check src --fix
	pyright src

format:
	isort src
	rye fmt
