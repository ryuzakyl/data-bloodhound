#
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, January 2017
#
# Makefile for DR Toolbox
#

# ---------------- installing requirements ----------------

# init:
# 	pip install -r requirements.txt

# ---------------- running tests ----------------

test:
    # taking './tests/nose.cfg' as the config file
    # taking '.' as the directory containing all the tests
	nosetests --config=./tests/nose.cfg -w .

# ---------------- building documentation ----------------

# Calling a Makefile from another:
# . http://stackoverflow.com/questions/2206128/how-to-call-makefile-from-another-makefile

# Passing parameters to another makefile:
# . http://stackoverflow.com/questions/2214575/passing-arguments-to-make-run

doc_api:
	cd docs && sphinx-apidoc -o packages/ .. ../main.py ../datasets/* ../experiments/* ../preprocessing/icoshift.py ../tests/* ../utils/* ../visualization/*

doc_html:
	cd docs && $(MAKE) html

doc_pdf:
	cd docs && $(MAKE) latex
	cd docs && $(MAKE) latexpdf

# building all types of documentations
doc_all: doc_api doc_html doc_pdf
