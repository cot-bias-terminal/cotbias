from __future__ import annotations

import httpx

from cotbias.exceptions import handle_error_response
from cotbias.models.inference import InferenceSchema


class InferenceResource:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def get(self, symbol: str) -> InferenceSchema:
        """Fetch current week's AI positioning regime and macro attribution."""
        resp = self._client.get(f"/inference/{symbol.upper()}")
        handle_error_response(resp)
        return InferenceSchema.model_validate(resp.json())


class AsyncInferenceResource:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get(self, symbol: str) -> InferenceSchema:
        resp = await self._client.get(f"/inference/{symbol.upper()}")
        handle_error_response(resp)
        return InferenceSchema.model_validate(resp.json())
