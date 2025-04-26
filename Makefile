# Makefile

.PHONY: quality

quality:
	isort .
	black .
	ruff check --fix