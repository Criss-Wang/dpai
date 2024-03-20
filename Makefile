.PHONY: refresh build install build_dist json release lint test docs

refresh_old: clean build install lint

refresh: test lint docs

build:
	python -m build

install:
	pip install -e .

docs:
	sphinx-build -b html docs/source/ docs/build/

lint:
	flake8 src/ tests/
	mypy src/

test:
	pytest

clean:
	rm model.db
	rm -rf model
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf src/dpai/__pycache__
	rm -rf build
	rm -rf dist
	rm -rf DeployableAI.egg-info
	rm -rf src/dpai.egg-info
	pip uninstall -y dpai