.PHONY: install sample test lint run artifacts

install:
	python -m pip install -e ".[dev]"

sample:
	python scripts/generate_sample.py

test:
	pytest -q

lint:
	ruff check .

run:
	streamlit run streamlit_app.py

artifacts:
	python scripts/run_analysis.py
	python scripts/build_report.py
	python scripts/build_presentation.py
