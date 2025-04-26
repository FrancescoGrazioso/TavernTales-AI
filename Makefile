# Makefile

.PHONY: quality coverage

quality:
	isort .
	black .
	ruff check --fix

coverage:
	pytest --cov=. --cov-report=html