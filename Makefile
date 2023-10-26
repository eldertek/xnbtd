SHELL := /bin/bash

all: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-poetry:
	@command -v poetry >/dev/null || (echo 'Please install poetry first, with e.g.: make install-poetry' && exit 1)

install-poetry:  ## install or update poetry
	poetry self update

venv:
	python3 -m venv .venv

install: check-poetry venv  ## install project via poetry
	poetry install

update: check-poetry venv  ## update the sources and installation and generate "conf/requirements.txt"
	poetry update -v
	poetry install

without-poetry-install: venv ## Install/update without poetry (not recommended!)
	.venv/bin/pip install -U pip
	.venv/bin/pip install -e .

lint: ## Run code formatters and linter
	poetry run isort --check-only .
	poetry run flake8 .

fix-code-style: ## Fix code formatting
	poetry run black --verbose --safe --line-length=100 --skip-string-normalization .
	poetry run isort .

tox-listenvs: check-poetry ## List all tox test environments
	poetry run tox --listenvs

tox: check-poetry ## Run tests via tox with all environments
	poetry run tox

test: install  ## Run tests
	DJANGO_SETTINGS_MODULE=xnbtd.settings.test poetry run python -Wa manage.py test -v 2

local-test: install  ## Run the project locally
	./manage.sh runserver

local-diff-settings:  ## Run "manage.py diffsettings"
	./manage.sh diffsettings

messages:  ## Run "manage.py makemessages"
	./manage.sh makemessages -l fr
	./manage.sh compilemessages --ignore=.venv

migrate: install  ## Run "manage.py migrate"
	./manage.sh makemigrations
	./manage.sh migrate

safety:  ## Run https://github.com/pyupio/safety
	poetry run safety check --full-report

publish: ## Release new version to PyPi
	poetry run publish

##############################################################################

.PHONY: help check-poetry install-poetry install update local-test
