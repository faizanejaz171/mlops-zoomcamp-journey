.PHONY: help setup format test build

# Help command khud-ba-khud saari commands bata degi
help:
	@echo "Available commands:"
	@echo "make setup  - Install pre-commit hooks and dependencies"
	@echo "make format - Run code quality tools (black, isort, pylint)"
	@echo "make test   - Run unit tests with pytest"

# Pre-commit aur baqi zaroori cheezein set karne ke liye
setup:
	pre-commit install
	pre-commit autoupdate

# Code ki safai aur quality check ke liye (wahi lambi command)
format:
	pre-commit run --all-files

# Testing ke liye (jab hum aage ja kar tests likhenge)
test:
	pytest tests/
