venv:
	python3 -m venv .venv
	@echo "Please run 'source .novastore/bin/venv'"

version:
	@echo "\ncheck python version"
	python --version 
	@echo "\ncheck pip version"
	pip --version  
	@echo "\nCheck Django Version"
	django-admin --version
	@echo "\n"

install:
	@echo "\nInstall Django framework"
	python -m pip install Django || pip install Django

create:
	@echo "\nCreate Project"
	django-admin startproject webApp

migrate:
	@echo "Migration ......"
	python smartGrader/manage.py makemigrations
	python smartGrader/manage.py migrate

app:
	@echo "\n Create app"
	cd medi_help/ && python manage.py startapp webApp && cd ..

pylint:
	@echo "please use pylint or flake8. im using flake8"
	flake8 --config=.flake8

run:
	@echo "Run the project ...."
	python smartGrader/manage.py runserver

db:
	@echo"\ncreate db\n"
	mkdir db
	initdb -D ~/db

start:
	@echo "\nStart Postgresql....\n"
	pg_ctl -D ~/db start || brew services start postgresql

stop:
	@echo "\nEnd Postgresql....\n"
	pg_ctl -D ~/db stop || brew services stop postgresql

status:
	@echo "\nStatus Postgresql....\n"
	pg_ctl -D ~/db status

connect:
	@echo "\nConnect Postgresql....\n"
	psql -U ravindu -d smartgrader

log:
	@echo "\nLog Postgresql....\n"
	pg_ctl -D ~/db -l db.log start