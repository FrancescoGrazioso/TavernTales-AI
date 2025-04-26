# Makefile

.PHONY: quality

quality:
	black .
	ruff check --fix
	isort .