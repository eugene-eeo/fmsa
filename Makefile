test:
	py.test -sq tests.py

test_cov:
	py.test -sq tests.py --cov=fmsa

supertest:
	FMSA_ROUNDS=50 py.test -sq tests.py
