clean:
	rm -rf .pytest_cache 
	
local-notebook:
	pipenv run notebook
