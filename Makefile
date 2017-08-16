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
init : requirements.txt
	pip install -r requirements.txt

.PHONY : update
update : clean-venv init versioneer.py
	rm versioneer.py
	versioneer install


# Local testing recipes
.PHONY : tests
tests: toxtest lint ;

.PHONY : ci
ci :
	pytest

.PHONY : toxtest
toxtest : local/environment.sh tox.ini
	source local/environment.sh && tox

.PHONY : pytest
pytest : local/environment.sh
	source local/environment.sh && pytest

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
clean : cleanbuild cleandocs cleanpytest cleantox ;

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

.PHONY : clean-all
clean-all : clean clean-dist ;

.PHONY : clean-dist
clean-dist :
	rm -rf ./dist/*

.PHONY : clean-venv
clean-venv :
	pip freeze | grep -v "^-e" | xargs pip uninstall -y
