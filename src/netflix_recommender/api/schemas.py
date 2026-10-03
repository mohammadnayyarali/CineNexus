"""API request and response models."""


from pydantic import BaseModel, Field


class RecommendationItem(BaseModel):
    title: str
    similarity_score: float = Field(ge=0, le=1)
    type: str | None = None
    listed_in: str | None = None
    release_year: int | str | None = None
    rating: str | None = None
    description: str | None = None


class RecommendationResponse(BaseModel):
    query_title: str
    recommendations: list[RecommendationItem]


class HealthResponse(BaseModel):
    status: str
    catalog_size: int


class TitlesResponse(BaseModel):
    titles: list[str]


class ErrorResponse(BaseModel):
    detail: str
