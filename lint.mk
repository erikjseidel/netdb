export WORKING_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
export LINT_IMAGE := erikjseidel/pylint-docker
export APP_DIR := /netdb
export PYLINTRC := /var/cache/.pylintrc

.PHONY: lint
lint:
	docker run --rm -v $(WORKING_DIR)/$(APP_DIR):$(APP_DIR)/ -v $(WORKING_DIR)/.pylintrc:$(PYLINTRC) -i $(LINT_IMAGE) pylint --rcfile=$(PYLINTRC) $(APP_DIR)
