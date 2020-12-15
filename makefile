all: install test

install:
	sage -pip install --upgrade --no-index -v .
install-internet:
	sage -pip install --upgrade -v .

develop:
	# python setup.py develop
	sage -pip install --upgrade -e .

test:
	sage -t --force-lib --show-skipped . --log=logs/test.log
testlong:
	sage -t --force-lib --long --show-skipped . --log=logs/testlong.log
ptest:
	sage -tp --force-lib --show-skipped . --log=logs/ptest.log
ptestlong:
	sage -tp --force-lib --long --memlimit=4000 --show-skipped . --log=logs/ptestlong.log

coverage:
	sage -coverage slabbe/*

doc:install
	cd docs && sage -sh -c "make html"
doc-pdf:install
	cd docs && sage -sh -c "make latexpdf"

dist:
	sage -python setup.py sdist
check: dist
	VERSION=`cat VERSION`; sage -sh -c "twine check dist/slabbe-$$VERSION.tar.gz"
upload: dist
	VERSION=`cat VERSION`; sage -sh -c "twine upload dist/slabbe-$$VERSION.tar.gz"

clean: clean-doc
clean-doc:
	cd docs && sage -sh -c "make clean"

.PHONY: all install develop test coverage clean clean-doc doc doc-pdf dist upload
