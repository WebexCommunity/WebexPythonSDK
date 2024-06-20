.PHONY: clean setup format lint build tests tests-manual tests-slow tests-all docs

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .cache/
	rm -f  .coverage
	rm -rf .pytest_cache/
	rm -rf docs/_build/*

setup:
	-poetry env remove
	poetry install

format:
	poetry run ruff format .

lint:
	poetry run check .

build:
	poetry build

tests:
	poetry run pytest -s -m "not slow and not manual"

tests-manual:
	poetry run pytest -s -m "manual"

tests-slow:
	poetry run pytest -s -m "slow and not manual"

tests-all:
	poetry run pytest

docs:
	$(MAKE) -C docs html
