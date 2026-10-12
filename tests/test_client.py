from __future__ import annotations

import pytest
from cotbias import CotClient, AsyncCotClient
from cotbias.config import DEFAULT_BASE_URL


def test_client_missing_key(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("COT_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key missing"):
        CotClient()


def test_client_env_key(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("COT_API_KEY", "cot_live_envkey")
    with CotClient() as cot:
        assert cot._http.headers["X-API-Key"] == "cot_live_envkey"
        assert str(cot._http.base_url).rstrip("/") == DEFAULT_BASE_URL


def test_client_explicit_key():
    with CotClient(api_key="cot_live_explicit", base_url="https://api.custom.com/v1") as cot:
        assert cot._http.headers["X-API-Key"] == "cot_live_explicit"
        assert str(cot._http.base_url).rstrip("/") == "https://api.custom.com/v1"


@pytest.mark.asyncio
async def test_async_client_context():
    async with AsyncCotClient(api_key="cot_live_async") as cot:
        assert cot._http.headers["X-API-Key"] == "cot_live_async"
