run:
	poetry run python -m flip

test:
	poetry run ./test.py

cli:
	tio /dev/ttyACM0
