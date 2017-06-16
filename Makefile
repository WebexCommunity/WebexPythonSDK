SHELL=/bin/bash

# Build recipes
.PHONY : build
build : tests docs buildpackage ;

.PHONY : buildpackage
buildpackage : setup.py
	python setup.py sdist

.PHONY : docs
docs : docs/Makefile
	cd docs/
	make html


# Local project directory and environment management recipes
.PHONY : init
init : requirements.txt
	pip install -r requirements.txt


# Local testing recipes
.PHONY : tests
tests: toxtest lint ;

.PHONY : toxtest
toxtest : local/environment.sh tox.ini
	source local/environment.sh
	tox

.PHONY : pytest
pytest : local/environment.sh
	source local/environment.sh
	pytest

.PHONY : lint
lint :
	flake8 ciscosparkapi


# Cleaning recipes
.PHONY : clean
clean : cleanbuild cleandocs cleanpytest cleantox ;

.PHONY : cleanbuild
cleanbuild :
	rm -rf ./ciscosparkapi.egg-info/

.PHONY : cleandocs
cleandocs :
	rm -rf ./docs/_build/*

.PHONY : cleantox
cleantox : cleanpytest
	rm -rf ./.tox/

.PHONY : cleanpytest
cleanpytest :
	rm -rf ./.cache/

.PHONY : clean-all
clean-all : clean clean-dist ;

.PHONY : clean-dist
cleandist :
	rm -rf ./dist/*

.PHONY : clean-venv
clean-venv :
	pip freeze | grep -v "^-e" | xargs pip uninstall -y
