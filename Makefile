all : clean format lint
.PHONY : all

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

format: isort-format black-format

lint:
	poetry run pylava

run:
	poetry run python main.py

isort-format:
	poetry run isort -rc --atomic .

black-format:
	poetry run black fizzbotz
