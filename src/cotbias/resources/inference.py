import httpx
from cotbias.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitExceededError,
    CotApiError,
)
from cotbias.models.inference import InferenceSchema


class InferenceResource:
    def __init__(self, client: httpx.Client):
        self._client = client

    def get(self, symbol: str) -> InferenceSchema:
        """Fetch current week's AI positioning regime and macro attribution."""
        resp = self._client.get(f"/inference/{symbol.upper()}")
        
        if resp.status_code == 200:
            return InferenceSchema.model_validate(resp.json())
        elif resp.status_code == 401:
            raise AuthenticationError("Invalid or expired API key", status_code=401)
        elif resp.status_code == 404:
            raise NotFoundError(f"Market '{symbol}' not found", status_code=404)
        elif resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 60))
            raise RateLimitExceededError("Rate limit exceeded", retry_after=retry_after)
        else:
            raise CotApiError(f"API Error: {resp.text}", status_code=resp.status_code)


class AsyncInferenceResource:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def get(self, symbol: str) -> InferenceSchema:
        resp = await self._client.get(f"/inference/{symbol.upper()}")
        if resp.status_code == 200:
            return InferenceSchema.model_validate(resp.json())
        elif resp.status_code == 401:
            raise AuthenticationError("Invalid API key", status_code=401)
        elif resp.status_code == 404:
            raise NotFoundError(f"Market '{symbol}' not found", status_code=404)
        elif resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 60))
            raise RateLimitExceededError("Rate limit exceeded", retry_after=retry_after)
        raise CotApiError(f"API Error: {resp.text}", status_code=resp.status_code)