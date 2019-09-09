DEVPI_URL ?= https://devpi.qa.stormsec.com.br/deploy/dev/+simple
CI_ENVIRONMENT_NAME ?= dev

.PHONY: clean clean-test clean-pyc clean-build docs help tests uninstall_all
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

define UNINSTALL_ALL_PYSCRIPT
import os
req = 'requirements.txt'
for package in [x.split('==')[0] for x in open(req).read().split('\n')]:
	if package.strip():
		os.system('pip uninstall --yes %s' % package)

endef
export UNINSTALL_ALL_PYSCRIPT

uninstall_all:
	@python -c "$$UNINSTALL_ALL_PYSCRIPT"

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

local:
	DYNAMODB_URL="http://localhost:8000" chalice local --port 8002

tests:
	python3 -m pytest -s -v --cov=tests --cov=playerstars_routes -W ignore::DeprecationWarning --cov-report term-missing:skip-covered
	@echo "Linting..."
	@flake8 playerstars_routes/ --max-complexity=5
	@flake8 tests/ --ignore=S101,S311,F811
	@echo "\033[32mTudo certo!"

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/playerstars_routes.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ playerstars_routes
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

install_dev: clean install ## instala as dependências de desenvolvimento
	pip install -r requirements_dev.txt

install: clean uninstall_all ## instala as dependências do projeto
	pip install devpi-client
	devpi use $(DEVPI_URL) --always-set-cfg=yes
	pip install -r requirements.txt

deploy: clean install ## Executa o chalice deploy.
	chalice deploy --stage $(CI_ENVIRONMENT_NAME) | tee deploy.log

run:
	@chalice local --port 8080 --host 0.0.0.0 --stage stg
