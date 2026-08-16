ifeq ($(OS),Windows_NT)
    PYTHON ?= python
    VENV_PYTHON := .venv/Scripts/python.exe
else
    PYTHON ?= python3
    VENV_PYTHON := .venv/bin/python
endif

.PHONY: setup test eval tokenize parse

setup:
	$(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install -r requirements.txt

test:
	$(VENV_PYTHON) -m pytest tests/ -v

eval:
	$(VENV_PYTHON) main.py "$(EXPR)"

tokenize:
	$(VENV_PYTHON) main.py "$(EXPR)" -t

parse:
	$(VENV_PYTHON) main.py "$(EXPR)" -p