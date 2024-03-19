venv:
	python3 -m venv .venv
	@echo "Please run 'source .novastore/bin/venv'"

migrate:
	python smartGrader/manage.py 

run:
	python smartGrader/manage.py runserver