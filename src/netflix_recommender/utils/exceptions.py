"""Domain exceptions used across the application."""


class DatasetValidationError(ValueError):
    """Raised when a dataset cannot support recommendations."""


class TitleNotFoundError(LookupError):
    """Raised when a requested title is absent from the catalog."""


class RecommendationError(RuntimeError):
    """Raised when recommendation artifacts are incomplete or invalid."""
