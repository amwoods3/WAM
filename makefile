fresh:
	find -name '*~' -exec rm '{}' \;
	find -name '*.pyc' -exec rm '{}' \;
pull: fresh
	git pull
add:
	git add . -A
commit:
	git commit
push: fresh pull add commit
	git push
run:
	python wam/manage.py runserver
flush:
	python wam/manage.py flush
migrate:
	python wam/manage.py makemigrations
	python wam/manage.py migrate
