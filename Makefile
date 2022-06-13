clean:
	rm -rf .pytest_cache */.ipynb_checkpoints

format:
	pipenv run isort && pipenv run format

lint:
	pipenv run lint

local-notebook:
	pipenv run notebook

test:
	pipenv run pytest scripts/test/*.py