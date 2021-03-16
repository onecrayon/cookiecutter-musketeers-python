# Basic 3 Musketeers pattern
DOCKER_RUN=docker run --rm -v "${PWD}":'/code' -w '/code' -it cookiecutter:python-musketeers

##
##=== Template for a 3-Musketeers Python project ===
##

help: build  ## Show this help
	@$(DOCKER_RUN) make _help

# This has to be a single line to avoid getting interpreted as help text
_help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -E -e 's/: [a-z0-9_][ a-z0-9_-]+?[a-z0-9](\s+)##/:\1/' | sed -e 's/##//'

# Default command: create a new Cookiecutter project from this project
# BASE is the local parent directory within which to run CookieCutter
ifndef BASE
override BASE = ./
endif
# Evaluate absolute path for BASEPATH, in case they passed a relative one
BASEPATH = $(shell cd $(BASE) && pwd)

new: build   ## Create a new project from this template; set BASE to specify parent directory
	@docker run --rm -v "${PWD}":'/code' -v "$(BASEPATH)":'/base' -w '/code' \
		-it cookiecutter:python-musketeers cookiecutter --output-dir /base /code

build: ## Rebuild the image for running CookieCutter
	@docker build -t cookiecutter:python-musketeers .

shell: ## Access bash in the CookieCutter shell
	@$(DOCKER_RUN) bash
