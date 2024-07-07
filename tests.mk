
.PHONY: unit-tests
unit-tests:
	docker build -f Dockerfile.pytest -t test-netdb-api .
	docker run --rm test-netdb-api && docker image rm test-netdb-api
