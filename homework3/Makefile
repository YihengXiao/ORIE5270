cover:
	make lint
	make cover_tests

lint:
	flake8 --max-line-length=100 find_path tests

cover_tests:
	py.test -s --cov-config .coveragerc --cov find_path --cov-report term-missing \
	--no-cov-on-fail \
	--cov-fail-under=90 \
	tests
