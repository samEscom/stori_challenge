SHELL=/bin/bash
PATH := .venv/bin:$(PATH)
export TEST?=./tests
export LAMBDA?=stori-challenge
export REPO=lambda-${LAMBDA}
export ENV?=dev

install:
	@( \
		if [ ! -d .venv ]; then python3 -m venv --copies .venv; fi; \
		source .venv/bin/activate; \
		python3 -m pip install -qU pip; \
		python3 -m pip install -r requirements-dev.txt; \
		python3 -m pip install -r requirements.txt; \
	)

setup:
	@if [ ! -f .env ] ; then cp .env.mock .env ; fi;
	@make install;

autoflake:
	@autoflake . --check --recursive --remove-all-unused-imports --remove-unused-variables --exclude .venv;

black:
	@black . --check --exclude '.venv|build|target|dist|.cache|node_modules';

isort:
	@isort . --check-only;

lint: black isort autoflake

lint-fix:
	@black . --exclude '.venv|build|target|dist';
	@isort .;
	@autoflake . --in-place --recursive --exclude .venv --remove-all-unused-imports --remove-unused-variables;

tests:
	@python -B -m pytest -l --color=yes \
		--cov=src \
		--cov-config=./tests/.coveragerc \
		--cov-report term \
		--cov-report html:coverage \
		--junit-xml=junit.xml \
		--rootdir=. $${TEST};


invoke-local:
	@aws lambda invoke --function-name $${LAMBDA} --payload file://event.local.json --qualifier $${ENV} response.json;
	@if [ -f response.json ]; then python -B -m json.tool response.json; fi;



.PHONY: tests docs
