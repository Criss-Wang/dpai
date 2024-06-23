ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.SILENT:
.PHONY: refresh install setup lint test docs

refresh:

build: install setup test

setup:
	echo "=== Port forward the required services ==="
	export $(grep -v '^#' .env | xargs -0)

test:
	echo "=== Run tests ==="
	if ! command -v pytest &> /dev/null; then \
        echo "Installing pytest..."; \
        pip install pytest; \
    fi
	# export TEST_ENV=dev && \
	# python -m pytest

docs:

lint:
	python -m flake8 cre tests

kill_k:
	ps aux | grep -i kubectl | grep -v grep | awk {'print $$2'} | xargs kill

