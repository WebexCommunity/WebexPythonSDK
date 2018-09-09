# Scripts to Rule Them All

## Script Summary

| Script | Intent |
|:--|:--|
| [`script/installdeps`](#scriptinstalldeps) | Install project dependencies |
| [`script/clean`](#scriptclean) | Clean-up project artifacts |
| [`script/setup`](#scriptsetup) | Setup or reset the project to an initial state |
| [`script/update`](#scriptupdate) | Update the project after a fresh pull |
| [`script/test`](#scripttest) | Run the project's test suite |
| [`script/build`](#scriptbuild) | Build the project's product(s) |
| [`script/ci`](#scriptci) | Continuous integration script |
| [`script/ci-bootstrap`](#scriptcibootstrap) | CI bootstrap script |
| [`script/server`](#scriptserver) | Control project servers and services |
| [`script/console`](#scriptconsole) | Access the project's console |

### script/installdeps

[`script/installdeps`][installdeps] Install the dependencies for this project.

### script/clean

[`script/clean`][clean] Clean the project directory

This script implements a `--deep` command line option that "deep cleans" the system removing all artifacts created by the project (virtual environments and all).

### script/setup

[`script/setup`][setup] Set up the project or reset it to an initial state.

This is typically run after an initial clone, or, to _reset_ the project back to its _initial state_. [`script/clean`][clean] and [`script/installdeps`][installdeps] are run inside this script.

### script/update

[`script/update`][update] Update the project's dependencies.

### script/test

[`script/test`][test] Run the test suite for this project.

This script implements `lint`, `tests`, and `ratelimiting` command line options to enable you to select and run only the code linting or the package tests (by default, both are run when you execute `script/test` without any command line arguments).


### script/build

[`script/build`][build] Build this project's product(s).

### script/ci

[`script/ci`][ci] Continuous integration script.

### script/ci-bootstrap

[`script/ci-bootstrap`][ci-bootstrap] Prepare the CI environment.

### script/console

[`script/console`][console] Open a console for the project.

## Inspiration

The GitHub Engineering Team: [Scripts to Rule Them All](https://githubengineering.com/scripts-to-rule-them-all/)

[github/scripts-to-rule-them-all](https://github.com/github/scripts-to-rule-them-all)

[installdeps]: installdeps
[clean]: clean
[setup]: setup
[update]: update
[test]: test
[build]: build
[ci]: ci
[ci-bootstrap]: ci-bootstrap
[console]: console
