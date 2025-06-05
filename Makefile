dev:
	uvicorn app.main:app --reload --log-level warning --host 0.0.0.0 --port 8000
production:
	uvicorn app.main:app --log-level warning --host 0.0.0.0 --port 8000 --workers 2