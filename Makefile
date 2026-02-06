PYTHON ?= python3
PROJECT_NAME := project-chimera

.PHONY: setup test test-docker

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .
	$(PYTHON) -m pip install pytest

test:
	$(PYTHON) -m pytest

test-docker:
	docker build -t $(PROJECT_NAME)-test .
	docker run --rm $(PROJECT_NAME)-test

