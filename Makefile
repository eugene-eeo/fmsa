test:
	py.test -sq tests.py

test_cov:
	py.test -sq tests.py --cov=fmsa
