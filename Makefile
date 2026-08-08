ifeq ($(OS),Windows_NT)
	VENV_PYTHON = .venv/Scripts/python.exe
else
	VENV_PYTHON = .venv/bin/python
endif

.PHONY: test lexer setup

setup:
	python -m venv .venv
	$(VENV_PYTHON) -m pip install -r requirements.txt

test:
	$(VENV_PYTHON) -m pytest tests/ -v

lexer:
	$(VENV_PYTHON) -m expr_evaler.lexer "$(EXPR)"
