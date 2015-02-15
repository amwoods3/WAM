fresh:
	find -name '*~' -exec rm '{}' \;
pull:
	git pull
add:
	git add . -A
commit:
	git commit
push: pull fresh add commit
	git push
bilbo:
	scp -r ./server/ ./src/ amwoods3@bilbo.ccis.edu:~/ciss465/
