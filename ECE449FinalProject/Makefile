# Author      : Rasheed Othman
# Created     : December 1, 2023
# Description : Provides Makefile rules for project navigation.

# Specify the project name here
name := "FuzzyController_v1.0.0"

# Use Bash as the default shell
SHELL := bash

# Setting these flags forces an exit when an error occurs
.SHELLFLAGS := -eu -o pipefail -c

# Adding this flag disables any built-in Make rules
MAKEFLAGS += --no-builtin-rules

# This variable is set to run the help message when 'make' is used with no target
.DEFAULT_GOAL := help

# Create an alias for the parent working directory path
pwd := $(realpath $(dir $(abspath $(firstword $(MAKEFILE_LIST)))))

# Run Python packages from the virtual environment if it exists, otherwise use the system's path
# The shell command is run each time the variable is used
.ONESHELL:
py = $(shell if [ -d $(pwd)/env ]; then echo "source $(pwd)/env/bin/activate && $(pwd)/env/bin/python"; else echo "python3"; fi)
pip = $(shell if [ -d $(pwd)/env ]; then echo "source $(pwd)/env/bin/activate && $(pwd)/env/bin/pip"; else echo "pip"; fi)

# This variable tells Make that this rule isn't associated with a file.
.PHONY: help
help: ## Display a list of runnable targets
	@echo ------------------------------------------------------------------
	@echo $(name) Application Makefile Usage:
	@echo ------------------------------------------------------------------
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z\$$/]+.*:.*?##\s/ {printf "\033[36m%-12s\033[0m > %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ------------------------------------------------------------------

run: ## Run the application
	$(py) $(script)

venv: ## Initialize a new Python virtual environment
	$(py) -m pip install -U pip
	pip install -U virtualenv
	virtualenv env
	$(MAKE) install

install: requirements/modules.txt ## Install the project Python package requirements
	$(py) -m pip install -U pip
	$(pip) install -U -r requirements/modules.txt
