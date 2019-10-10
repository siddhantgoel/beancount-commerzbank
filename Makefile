lint-flake8:
	poetry run flake8 beancount_commerzbank/ tests/

lint-black:
	poetry run black --check beancount_commerzbank/ tests/

lint: lint-black lint-flake8

test-pytest:
	poetry run py.test tests/

.PHONY: lint test
