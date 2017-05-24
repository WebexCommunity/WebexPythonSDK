SHELL=/bin/bash

# Build recipes
.PHONY : build
build : tests docs buildpackage ;

.PHONY : buildpackage
buildpackage : setup.py
	python setup.py sdist

docs : docs/Makefile
	cd docs/
	make html


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
clean : cleanbuild cleandocs cleanpytest cleantox cleandist ;

.PHONY : cleandist
cleandist :
	rm -rf ./dist/*

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
