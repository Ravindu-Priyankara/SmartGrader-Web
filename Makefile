venv:
	python3 -m venv .venv
	@echo "Please run 'source .novastore/bin/venv'"

migrate:
	@echo "Migration ......"
	python smartGrader/manage.py 

pylint:
	@echo "please use pylint or flake8. im using flake8"
	flake8 smartGrader/webApp/

run:
	@echo "Run the project ...."
	python smartGrader/manage.py runserver