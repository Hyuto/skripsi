clean:
	find . | grep -E '(__pycache__|\.pyc|\.lprof|\.pytest_cache|\.ipynb_checkpoints|\.coverage)' | xargs rm -rf

format:
	pipenv run isort && pipenv run format

lint:
	pipenv run lint

local-notebook:
	pipenv run notebook

test:
	pipenv run test