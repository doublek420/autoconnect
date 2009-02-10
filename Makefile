release:
	python2.4 setup.py bdist_egg upload
	python2.5 setup.py bdist_egg upload
	/opt/web/bin/python2.6 setup.py bdist_egg upload

