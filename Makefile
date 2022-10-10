# Tests
#

.PHONY: tests tests-backend

tests: tests-backend

tests-backend:
	pytest backend/tests/

# Tests + Coverage
#

.PHONY: coverage coverage-backend

coverage: coverage-backend

coverage-backend:
	pytest --cov=backend --cov-report term --cov-report \
		xml:coverage/backend-coverage.xml backend/tests/
