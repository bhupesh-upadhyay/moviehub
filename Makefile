# Use the project venv explicitly (avoids /usr/bin/pip on Python 3.8).
PYTHON ?= .venv/bin/python
UV ?= uv

.PHONY: install install-uv check

install:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -r requirements.txt

install-uv:
	$(UV) pip install -r requirements.txt

check:
	$(PYTHON) manage.py check
