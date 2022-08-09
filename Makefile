lint:
	pip install -r backend/requirements/dev-requirements.txt
	flake8 backend
	pylint backend
	black --check --config black.toml backend

format:
	pip install -r backend/requirements/dev-requirements.txt
	black --verbose --config black.toml backend
	isort backend

run:
	python3 backend/main.py