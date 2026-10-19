"""Official Python client and MCP Server for CFTC COT Bias Terminal Quant API.

Provides institutional Commitment of Traders (COT) analytics, historical timeseries,
cross-asset screeners, and AI-driven positioning regimes directly in Python and
in AI assistants.
"""

from __future__ import annotations

from .client import AsyncCotClient, CotClient, __version__
from .config import DEFAULT_BASE_URL
from .exceptions import (
    AuthenticationError,
    CotApiError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitExceededError,
    ServerError,
)
from .models import (
    InferenceSchema,
    MarketMetadata,
    MarketsResponse,
    QualitativeAttribution,
    ScreenerResponse,
    ScreenerResultItem,
    TimeseriesResponse,
    TimeseriesRow,
)

__all__ = [
    "DEFAULT_BASE_URL",
    "AsyncCotClient",
    "AuthenticationError",
    "CotApiError",
    "CotClient",
    "InferenceSchema",
    "MarketMetadata",
    "MarketsResponse",
    "NotFoundError",
    "PermissionDeniedError",
    "QualitativeAttribution",
    "RateLimitExceededError",
    "ScreenerResponse",
    "ScreenerResultItem",
    "ServerError",
    "TimeseriesResponse",
    "TimeseriesRow",
    "__version__",
]
