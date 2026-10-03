# API

Start the service with:

```powershell
$env:PYTHONPATH = "src"
uvicorn netflix_recommender.api.main:app --reload
```

Endpoints:

- `GET /` service description
- `GET /health` artifact readiness and catalog size
- `GET /titles` available title strings
- `GET /recommend?title=Stranger%20Things&top_n=5` ranked results

Unknown titles return HTTP 404. Empty or out-of-range query parameters return HTTP 422. Missing artifacts return HTTP 503. FastAPI publishes interactive OpenAPI documentation at `/docs`.
