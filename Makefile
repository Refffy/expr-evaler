VENV_PYTHON = .venv/Scripts/python.exe

.PHONY: test lexer setup

setup:
	python -m venv .venv
	$(VENV_PYTHON) -m pip install -r requirements.txt

test:
	$(VENV_PYTHON) -m pytest tests/ -v

lexer:
	$(VENV_PYTHON) -m expr_evaler.lexer "$(EXPR)"
