env:
	pipenv --three
	pipenv install
devenv:	env
	pipenv install --dev
test:	
	pipenv run py.test tests/
