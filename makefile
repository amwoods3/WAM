fresh:
	find -name '*~' -exec rm '{}' \;
	find -name '*.pyc' -exec rm '{}' \;
pull:
	git pull
add:
	git add . -A
commit:
	git commit
push: fresh pull add commit
	git push
bilbo:
	scp -r ./server/ ./src/ amwoods3@bilbo.ccis.edu:~/ciss465/
