.PHONY: setup test lint format ci report

setup:
	python -m pip install -U pip
	pip install -e .[test,dev]

test:
	pytest -q

lint:
	ruff check src tests
	mypy src

format:
	black src tests
	ruff check --fix src tests

ci: lint test

report:
	python -m raman_ai.report.gen_latex


.PHONY: train_bayes figs standards
train_bayes:
	python -m raman_ai.cli train_bayes

figs:
	python -m raman_ai.cli inject_figs

standards:
	python -m raman_ai.cli list_standards


.PHONY: preprocess features train calibrate evaluate report paper
preprocess:
	python -m raman_ai.cli preprocess
features:
	python -m raman_ai.cli features
train:
	python -m raman_ai.cli train --alpha 1.3 --beta 25.0
calibrate:
	python -m raman_ai.cli calibrate --method isotonic --quantiles 15
evaluate:
	python -m raman_ai.cli evaluate
report:
	python -m raman_ai.cli report
paper: train calibrate report


# paper target runs train->calibrate->report with default options
paper:
	python -m raman_ai.cli train --alpha 1.3 --beta 25.0
	python -m raman_ai.cli calibrate --method isotonic --quantiles 15
	python -m raman_ai.cli report
