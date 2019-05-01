flake8:
	flake8 beancount_commerzbank/ tests/

py.test:
	py.test tests/

test: flake8 py.test

.PHONY: test
