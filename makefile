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
