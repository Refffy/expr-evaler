ifeq ($(OS),Windows_NT)
	PYTHON ?= py -3
	VENV_PYTHON := .venv/Scripts/python.exe
else
	PYTHON ?= python3
	VENV_PYTHON := .venv/bin/python
endif

.PHONY: setup test lexer

setup:
	python -m venv .venv
	$(VENV_PYTHON) -m pip install -r requirements.txt
	$(VENV_PYTHON) -m pip install -e .

test:
	$(VENV_PYTHON) -m pytest tests/ -v

lexer:
	$(VENV_PYTHON) lexer/lexer.py "$(EXPR)"

