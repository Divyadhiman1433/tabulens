.PHONY: install sample test lint run

install:
	python -m pip install -e ".[dev]"

sample:
	python scripts/generate_sample.py

test:
	pytest -q

lint:
	ruff check .

run:
	streamlit run app.py
