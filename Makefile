export WORKING_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
export BLACK_IMAGE := pyfound/black
export LINT_IMAGE := erikjseidel/pylint-docker
export APP_DIR := /netdb
export PYLINTRC := /var/cache/.pylintrc

.PHONY: format
format:
	docker run --rm -v $(WORKING_DIR)/$(APP_DIR):$(APP_DIR)/ $(BLACK_IMAGE) black --fast --skip-string-normalization $(APP_DIR)/

.PHONY: black
black:
	docker run --rm -v $(WORKING_DIR)/$(APP_DIR):$(APP_DIR)/ $(BLACK_IMAGE) black --fast --skip-string-normalization --check $(APP_DIR)/

.PHONY: lint
lint:
	docker run --rm -v $(WORKING_DIR)/$(APP_DIR):$(APP_DIR)/ -v $(WORKING_DIR)/.pylintrc:$(PYLINTRC) -i $(LINT_IMAGE) pylint --rcfile=$(PYLINTRC) $(APP_DIR)

.PHONY: unit-tests
unit-tests:
	docker build -f Dockerfile.pytest -t test-netdb-api .; docker run --rm test-netdb-api; e=$$?; docker image rm test-netdb-api ; exit $$e

.PHONY: type-check
type-check:
	docker build -f Dockerfile.pytest -t test-netdb-api .; docker run --rm test-netdb-api mypy --explicit-package-bases .; e=$$?; docker image rm test-netdb-api ; exit $$e

.PHONY: build
build:
	docker build -t erikjseidel/netdb-api .
