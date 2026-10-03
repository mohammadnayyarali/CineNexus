"""FastAPI route definitions."""

from fastapi import APIRouter, HTTPException, Query, status

from netflix_recommender.api.schemas import HealthResponse, RecommendationResponse, TitlesResponse
from netflix_recommender.utils.exceptions import TitleNotFoundError


def build_router(engine: object | None, max_top_n: int = 50) -> APIRouter:
    router = APIRouter()

    def require_engine() -> object:
        if engine is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Recommendation artifacts are not loaded.")
        return engine

    @router.get("/", tags=["service"])
    def root() -> dict[str, str]:
        return {"service": "CineNexus", "message": "Content-based Netflix recommendations"}

    @router.get("/health", response_model=HealthResponse, tags=["service"])
    def health() -> HealthResponse:
        active_engine = require_engine()
        return HealthResponse(status="healthy", catalog_size=len(active_engine.metadata))

    @router.get("/titles", response_model=TitlesResponse, tags=["catalog"])
    def titles() -> TitlesResponse:
        return TitlesResponse(titles=require_engine().titles())

    @router.get("/recommend", response_model=RecommendationResponse, tags=["recommendations"])
    def recommend(title: str = Query(min_length=1, max_length=200), top_n: int = Query(default=10, ge=1, le=max_top_n)) -> RecommendationResponse:
        try:
            recommendations = require_engine().recommend(title, top_n)
        except TitleNotFoundError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
        return RecommendationResponse(query_title=title.strip(), recommendations=recommendations)

    return router
