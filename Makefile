SHELL=/bin/bash

# Build recipes
.PHONY : build
build : tests docs buildpackage
	$(MAKE) clean

.PHONY : buildpackage
buildpackage : setup.py
	python setup.py sdist

.PHONY : docs
docs : docs/Makefile
	cd docs/ && $(MAKE) html


# Local project directory and environment management recipes
.PHONY : init
init : Pipfile
	pipenv install --dev --skip-lock

.PHONY : update
update :
	pipenv update --dev
	pipenv lock -r > requirements-secure.txt
	pipenv lock -r --dev > requirements-secure-dev.txt
	pipenv run pip freeze > requirements.txt
	rm versioneer.py
	pipenv run versioneer install


# Local testing recipes
.PHONY : tests
tests: lint toxtest ;

.PHONY : ci
ci :
	pytest -m "not ratelimit"

.PHONY : toxtest
toxtest : tox.ini
	tox

.PHONY : pytest
pytest :
	pytest -m "not ratelimit"

.PHONY : pytest-rate-limit
pytest-rate-limit : local/environment.sh
	pytest -m "ratelimit"

.PHONY : lint
lint :
	flake8 ciscosparkapi


# Git recipes
.PHONY : push
push :
	git push origin
	git push origin --tags


# Cleaning recipes
.PHONY : clean
clean : cleanbuild cleandocs cleanpytest cleantox clean-dist ;

.PHONY : clean-all
clean-all : clean clean-venv ;

.PHONY : cleanbuild
cleanbuild :
	rm -rf ./ciscosparkapi.egg-info/
	rm -rf ./__pycache__/

.PHONY : cleandocs
cleandocs :
	rm -rf ./docs/_build/*

.PHONY : cleantox
cleantox : cleanpytest
	rm -rf ./.tox/

.PHONY : cleanpytest
cleanpytest :
	rm -rf ./.cache/

.PHONY : clean-dist
clean-dist :
	rm -rf ./dist/*

.PHONY : clean-venv
clean-venv :
	pipenv --rm
