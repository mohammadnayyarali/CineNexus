"""FastAPI application factory."""

from pathlib import Path

from fastapi import FastAPI

from netflix_recommender.api.routes import build_router
from netflix_recommender.config import Settings
from netflix_recommender.logging_config import configure_logging
from netflix_recommender.recommender.artifacts import load_engine


def create_app(engine: object | None = None, settings: Settings | None = None) -> FastAPI:
    """Create an app with an optional injected engine for tests and local embedding."""
    runtime_settings = settings or Settings.from_environment()
    configure_logging(runtime_settings.log_level)
    loaded_engine = engine
    artifact = Path(runtime_settings.artifact_path)
    if loaded_engine is None and artifact.exists():
        loaded_engine = load_engine(artifact)
    app = FastAPI(title="CineNexus Recommendation API", version="0.1.0")
    app.include_router(build_router(loaded_engine, runtime_settings.max_top_n))
    return app


app = create_app()
