## Delete all compiled Python files
.PHONY: clean-pyc
clean-pyc:  ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test:  ## Remove test and coverage artifacts.
	rm -f .coverage coverage.xml
	rm -fr htmlcov/ .junit/
	rm -fr .pytest_cache

.PHONY: lint black
## Lint using flake8
lint:
	python -m flake8 src

## Format your code using black
black:
	python -m black --version
	python -m black src