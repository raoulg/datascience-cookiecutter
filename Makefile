
.PHONY: install test lint format

install:
	pdm install

test:
	pdm run pytest

lint:
	pdm run flake8 cookietest
	pdm run mypy cookietest

format:
	pdm run isort -v cookietest
	pdm run black cookietest
