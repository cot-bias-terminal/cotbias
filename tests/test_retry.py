from __future__ import annotations

import httpx
import pytest
import respx

from cotbias.client import AsyncCotClient, CotClient
from cotbias.exceptions import (
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitExceededError,
    ServerError,
)


@respx.mock
def test_sync_retry_on_503_success():
    route = respx.get("https://api.cot-bias-terminal.com/v1/markets").mock(
        side_effect=[
            httpx.Response(503, json={"error": {"message": "Service unavailable"}}),
            httpx.Response(200, json={"markets": []}),
        ]
    )
    with CotClient(api_key="cot_live_test", max_retries=2) as cot:
        markets = cot.markets.list()
        assert len(markets) == 0
        assert route.call_count == 2


@respx.mock
def test_sync_no_retry_on_401():
    route = respx.get("https://api.cot-bias-terminal.com/v1/markets").mock(
        return_value=httpx.Response(401, json={"error": {"code": "INVALID_API_KEY", "message": "Unauthorized"}})
    )
    with CotClient(api_key="cot_live_test", max_retries=3) as cot:
        with pytest.raises(AuthenticationError):
            cot.markets.list()
        # Must not retry 401!
        assert route.call_count == 1


@respx.mock
def test_sync_no_retry_on_403():
    route = respx.get("https://api.cot-bias-terminal.com/v1/markets").mock(
        return_value=httpx.Response(403, json={"error": {"code": "FORBIDDEN", "message": "Upgrade required"}})
    )
    with CotClient(api_key="cot_live_test", max_retries=3) as cot:
        with pytest.raises(PermissionDeniedError):
            cot.markets.list()
        assert route.call_count == 1


@respx.mock
def test_sync_no_retry_on_404():
    route = respx.get("https://api.cot-bias-terminal.com/v1/inference/UNKNOWN").mock(
        return_value=httpx.Response(404, json={"error": {"code": "NOT_FOUND", "message": "Unknown symbol"}})
    )
    with CotClient(api_key="cot_live_test", max_retries=3) as cot:
        with pytest.raises(NotFoundError):
            cot.inference.get("UNKNOWN")
        assert route.call_count == 1


@respx.mock
def test_sync_no_retry_on_quota_exhausted():
    route = respx.get("https://api.cot-bias-terminal.com/v1/markets").mock(
        return_value=httpx.Response(
            429,
            json={"error": {"code": "QUOTA_EXCEEDED", "message": "Daily quota reached"}},
            headers={"Retry-After": "3600"},
        )
    )
    with CotClient(api_key="cot_live_test", max_retries=3) as cot:
        with pytest.raises(RateLimitExceededError) as exc_info:
            cot.markets.list()
        assert exc_info.value.code == "QUOTA_EXCEEDED"
        # Must not retry when daily quota is exhausted
        assert route.call_count == 1


@respx.mock
def test_sync_max_retries_zero():
    route = respx.get("https://api.cot-bias-terminal.com/v1/markets").mock(
        return_value=httpx.Response(500, json={"error": {"message": "Internal error"}})
    )
    with CotClient(api_key="cot_live_test", max_retries=0) as cot:
        with pytest.raises(ServerError):
            cot.markets.list()
        assert route.call_count == 1


@respx.mock
async def test_async_retry_on_502_success():
    route = respx.get("https://api.cot-bias-terminal.com/v1/markets").mock(
        side_effect=[
            httpx.Response(502, json={"error": {"message": "Bad Gateway"}}),
            httpx.Response(200, json={"markets": []}),
        ]
    )
    async with AsyncCotClient(api_key="cot_live_test", max_retries=2) as cot:
        markets = await cot.markets.list()
        assert len(markets) == 0
        assert route.call_count == 2
