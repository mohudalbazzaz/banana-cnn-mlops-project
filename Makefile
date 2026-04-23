fastapi:
	python3 -m uvicorn main:app --reload

streamlit:
	python3 -m streamlit run src/frontend/streamlit_app.py 

mlflow:
	mlflow ui --port 5001 --host 0.0.0.0

compose:
	docker compose up --build

pytest:
	python3 -m pytest

lint:
	python3 -m black . 

monitor:
	python -m src.backend.model_monitoring