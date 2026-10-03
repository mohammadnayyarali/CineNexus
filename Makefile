PORT ?= 8001
STREAMLIT_PORT ?= 8501

install:
	python -m pip install -e ".[dev]"

preprocess:
	python scripts/preprocess.py

build:
	python scripts/build_recommender.py

test:
	python -m pytest -q

lint:
	ruff check src scripts tests

api:
	uvicorn netflix_recommender.api.main:app --reload --host 127.0.0.1 --port $(PORT)

streamlit:
	streamlit run app/streamlit_app.py --server.port $(STREAMLIT_PORT) --server.headless true
