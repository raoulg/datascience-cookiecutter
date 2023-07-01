
.PHONY: install test lint format

install:
	pdm install

test:
	pdm run pytest -v

lint:
	pdm run ruff datascience_cookiecutter
	pdm run mypy --pretty datascience_cookiecutter

format:
	pdm run isort -v datascience_cookiecutter
	pdm run black datascience_cookiecutter
