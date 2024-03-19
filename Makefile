venv:
	python3 -m venv .venv
	@echo "Please run 'source .novastore/bin/venv'"

run:
	python smartGrader/manage.py runserver