# Defines help target logic
# Add help text after each target name starting with '\#\#'
# Inspired by <https://gist.github.com/prwhite/8168133>
DOCKER_RUN = docker-compose run --rm -e STANDALONE=true --no-deps -u root -w /code app
DOCKER_RUN_DB = docker-compose run --rm -u root -w /code app
{% if cookiecutter.use_pytest == 'True' -%}
DOCKER_COMPOSE_TESTS = docker-compose -p {{ cookiecutter.directory_name }}_tests -f docker-compose.yml -f docker/docker-compose.test.yml
{% endif %}
##=== Welcome to {{ cookiecutter.project_name }}! ===

help:     ## Show this help.
	@$(DOCKER_RUN) make _help

# This has to be a single line to avoid the ## in the line getting interpreted as help text
_help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -E -e 's/: [a-z0-9_][ a-z0-9_-]+?[a-z0-9](\s+)##/:\1/' | sed -e 's/##//'

##
##=== Local development ===

up:       ## Run local stack
	@docker-compose up

{% if cookiecutter.use_pytest == 'True' -%}
test:     ## Execute test suite; or specify target: `make test ARGS='app/tests/example'`
	@(DOCKER_COMPOSE_TESTS) run --rm -w /code app \
		pytest --cov=app --cov-config=.coveragerc --cov-report=term:skip-covered --cov-report=html $(ARGS)
{% endif -%}
{%- if cookiecutter.use_postgres == 'True' %}
# This ensures that even if they pass in an empty value, we default to "head"
ifndef REV
override REV = head
endif

migrate: clean-app  ## Run database migrations; or specify a revision: `make migrate REV='head'`
	@$(DOCKER_RUN_DB) alembic upgrade $(REV)

{% endif -%}

# This ensures that even if they pass in an empty value, we default to parsing the "app" folder
ifndef FILEPATH
override FILEPATH = app
endif

format:   ## Format via isort and black; or specify a file: `make format FILEPATH='app/main.py'`
	@$(DOCKER_RUN) make _format FILEPATH=$(FILEPATH)

_format:
	@black $(FILEPATH)
	@isort $(FILEPATH)

##
##=== Access internals ===

{% if cookiecutter.use_postgres == 'True' -%}
db:       ## Run standalone postgres server; accessible at localhost:5431
	@docker-compose run --service-ports --rm db

{% endif -%}

shell:    ## Open a bash shell to app (warning: root user!)
	@$(DOCKER_RUN) bash

{% if cookiecutter.use_postgres == 'True' -%}
shell-db: ## Open a bash shell to app with the database running
	@$(DOCKER_RUN_DB) bash

{% endif -%}

##
##=== Docker maintenance ===

build:    ## Rebuild the main app container
	@docker-compose build --no-cache app

clean-app:
	@docker-compose down --remove-orphans

{% if cookiecutter.use_pytest == 'True' -%}
clean-tests:
	@$(DOCKER_COMPOSE_TESTS) down --remove-orphans

{% endif -%}

clean: clean-app{% if cookiecutter.use_pytest == 'True' %} clean-tests{% endif %}    ## Clean up Docker containers, images, etc.
	@echo 'All clean!'

##

stack:     ## Rebuild the entire stack
	@docker-compose pull
	@docker-compose build

reset:     ## Completely remove all images, containers, and volumes (DANGER!)
	@docker-compose down --rmi all --remove-orphans --volumes
	@echo
	@echo 'You should now run `make stack`{% if cookiecutter.use_postgres == 'True' %}, `make db`, then populate your database{% endif %}!'
