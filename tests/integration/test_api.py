import pandas as pd
from fastapi.testclient import TestClient

from netflix_recommender.api.main import create_app
from netflix_recommender.features.feature_engineering import build_content_text
from netflix_recommender.features.vectorizer import ContentVectorizer
from netflix_recommender.recommender.engine import RecommendationEngine


def client() -> TestClient:
    frame = pd.DataFrame({"title": ["Alpha", "Beta"], "type": ["Movie", "Movie"], "description": ["space travel", "space mission"]})
    content = build_content_text(frame, ["description"])
    matrix = ContentVectorizer().fit_transform(content.tolist())
    return TestClient(create_app(RecommendationEngine(frame, matrix)))


def test_health_and_recommendation_endpoints() -> None:
    api = client()
    assert api.get("/health").json()["status"] == "healthy"
    response = api.get("/recommend", params={"title": "Alpha", "top_n": 1})
    assert response.status_code == 200
    assert response.json()["recommendations"][0]["title"] == "Beta"


def test_unknown_title_returns_404() -> None:
    assert client().get("/recommend", params={"title": "Missing"}).status_code == 404


def test_top_n_is_validated() -> None:
    assert client().get("/recommend", params={"title": "Alpha", "top_n": 0}).status_code == 422
