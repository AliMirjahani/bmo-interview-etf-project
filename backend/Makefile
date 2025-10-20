
PORT ?= 5000
PYTHON ?= python
PYTEST ?= $(PYTHON) -m pytest

install-deps:
	pip install -r requirements.txt

run:
	clear && PORT=$(PORT) $(PYTHON) main.py

run-tests:
	$(PYTEST) test/ -v

test-coverage:
	$(PYTEST) test/ -v --cov=. --cov-report=html --cov-report=term

