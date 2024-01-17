USER_GROUP := $(shell id -u):$(shell id -g)

UPSTREAM_OWNER := $(shell monitoring/scripts/git/upstream_owner.sh)
COMMIT := $(shell monitoring/scripts/git/commit.sh)

BLACK_EXCLUDES := "/interfaces|/venv"

ifeq ($(OS),Windows_NT)
  detected_OS := Windows
else
  detected_OS := $(shell uname -s)
endif


.PHONY: run_test
run_test: 
	cd monitoring && make run-decea-containers

.PHONY: down
down:
	cd monitoring && make stop-uss-mocks && make down-locally