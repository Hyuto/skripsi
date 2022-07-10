clean:
	find . | grep -E '(__pycache__|\.pyc|\.lprof|\.pytest_cache|\.ipynb_checkpoints)' | \
	xargs rm -rf

format:
	pipenv run isort .
	pipenv run black . 

format-check:
	pipenv run isort . --check-only
	pipenv run black . --check

local-notebook:
	pipenv run jupyter notebook --no-browser

test:
	pipenv run pytest --cov=scripts/ -v

typecheck:
	pipenv run mypy --no-incremental
