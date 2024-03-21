.PHONY: refresh build install build_dist json release lint test docs

refresh: clean build install test lint docs

build:
	python -m build

build_dist:
	make clean
	python -m build
	pip install dist/*.whl
	make test

install:
	pip install -e .

release:
	python -m twine upload dist/*

docs:
	sphinx-build -b html docs/source/ docs/build/

lint:
	flake8 src/ tests/
	mypy src/

test:
	python -m pytest

clean:
	rm models.db
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	pip uninstall -y dpai