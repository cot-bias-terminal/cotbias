"""Inference resource endpoint for AI positioning regimes and qualitative attribution."""

from __future__ import annotations

import httpx

from cotbias.exceptions import handle_error_response
from cotbias.models.inference import InferenceSchema


class InferenceResource:
    """Synchronous resource for querying current week AI positioning regimes and attribution."""

    def __init__(self, client: httpx.Client) -> None:
        """Initialize the inference resource with an active HTTP client.

        Args:
            client: Active synchronous HTTP client session.
        """
        self._client = client

    def get(self, symbol: str) -> InferenceSchema:
        """Fetch current week's AI positioning regime and macro attribution for an asset.

        Args:
            symbol: Asset ticker symbol (e.g., 'GC', 'ES', 'CL', '6E', 'ZB').

        Returns:
            An :class:`~cotbias.models.inference.InferenceSchema` model containing
            institutional bias score, regime status, primary driver, momentum,
            crowdedness risk, and qualitative macro attribution rationale.

        Raises:
            AuthenticationError: If API key is missing or invalid (HTTP 401).
            PermissionDeniedError: If account tier lacks access (HTTP 403).
            NotFoundError: If the market symbol is not found (HTTP 404).
            RateLimitExceededError: If daily request quota is exceeded (HTTP 429).
            ServerError: If upstream COT Bias servers return an error (HTTP 5xx).
            CotApiError: Base exception for any unexpected API errors.

        Example:
            ```python
            from cotbias import CotClient

            client = CotClient()
            regime = client.inference.get("ES")
            print(f"Bias: {regime.ai_bias_score} | Regime: {regime.regime_status}")
            print(f"Rationale: {regime.qualitative_attribution.macro_rationale}")
            ```
        """
        resp = self._client.get(f"/inference/{symbol.upper()}")
        handle_error_response(resp)
        return InferenceSchema.model_validate(resp.json())


class AsyncInferenceResource:
    """Asynchronous resource for querying current week AI positioning regimes and attribution."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        """Initialize the async inference resource with an active async HTTP client.

        Args:
            client: Active asynchronous HTTP client session.
        """
        self._client = client

    async def get(self, symbol: str) -> InferenceSchema:
        """Fetch current week's AI positioning regime and macro attribution asynchronously.

        Args:
            symbol: Asset ticker symbol (e.g., 'GC', 'ES', 'CL', '6E', 'ZB').

        Returns:
            An :class:`~cotbias.models.inference.InferenceSchema` model containing
            institutional bias score, regime status, primary driver, momentum,
            crowdedness risk, and qualitative macro attribution rationale.

        Raises:
            AuthenticationError: If API key is missing or invalid (HTTP 401).
            PermissionDeniedError: If account tier lacks access (HTTP 403).
            NotFoundError: If the market symbol is not found (HTTP 404).
            RateLimitExceededError: If daily request quota is exceeded (HTTP 429).
            ServerError: If upstream COT Bias servers return an error (HTTP 5xx).
            CotApiError: Base exception for any unexpected API errors.

        Example:
            ```python
            import asyncio
            from cotbias import AsyncCotClient

            async def main():
                async with AsyncCotClient() as client:
                    regime = await client.inference.get("CL")
                    print(regime.ai_bias_score, regime.momentum)

            asyncio.run(main())
            ```
        """
        resp = await self._client.get(f"/inference/{symbol.upper()}")
        handle_error_response(resp)
        return InferenceSchema.model_validate(resp.json())
