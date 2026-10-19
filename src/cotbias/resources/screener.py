"""Screener resource endpoint for cross-asset market filtering based on COT inference."""

from __future__ import annotations

from typing import Literal, cast, overload

import httpx
import pandas as pd

from cotbias.exceptions import handle_error_response
from cotbias.models.screener import ScreenerResponse


class ScreenerResource:
    """Synchronous resource for multi-market positioning scans."""

    def __init__(self, client: httpx.Client) -> None:
        """Initialize the screener resource with an active HTTP client.

        Args:
            client: Active synchronous HTTP client session.
        """
        self._client = client

    @overload
    def scan(
        self,
        ai_bias_score: str | None = ...,
        crowdedness_risk: str | None = ...,
        momentum: str | None = ...,
        cot_positioning: str | None = ...,
        as_dataframe: Literal[True] = ...,
    ) -> pd.DataFrame: ...

    @overload
    def scan(
        self,
        ai_bias_score: str | None = ...,
        crowdedness_risk: str | None = ...,
        momentum: str | None = ...,
        cot_positioning: str | None = ...,
        as_dataframe: Literal[False] = ...,
    ) -> ScreenerResponse: ...

    @overload
    def scan(
        self,
        ai_bias_score: str | None = ...,
        crowdedness_risk: str | None = ...,
        momentum: str | None = ...,
        cot_positioning: str | None = ...,
        as_dataframe: bool = ...,
    ) -> pd.DataFrame | ScreenerResponse: ...

    def scan(
        self,
        ai_bias_score: str | None = None,
        crowdedness_risk: str | None = None,
        momentum: str | None = None,
        cot_positioning: str | None = None,
        as_dataframe: bool = True,
    ) -> pd.DataFrame | ScreenerResponse:
        """Filter across all tracked futures markets based on positioning classifications.

        Args:
            ai_bias_score: Filter by directional bias (e.g. `'Bullish'`, `'Strongly Bullish'`,
                `'Bearish'`, `'Neutral'`).
            crowdedness_risk: Filter by positioning risk (e.g. `'High Liquidation Risk'`,
                `'High Squeeze Risk'`, `'Balanced'`).
            momentum: Filter by open interest dynamics (e.g. `'New Longs (OI Expanding)'`,
                `'Short Covering (OI Contracting)'`).
            cot_positioning: Filter by smart vs dumb positioning (`'Convergence'` or `'Divergence'`).
            as_dataframe: When `True` (default), returns a Pandas DataFrame of matched
                contracts. When `False`, returns a :class:`~cotbias.models.screener.ScreenerResponse`.

        Returns:
            A Pandas DataFrame if `as_dataframe=True`, or a `ScreenerResponse` model if `as_dataframe=False`.

        Raises:
            AuthenticationError: If API key is missing or invalid (HTTP 401).
            PermissionDeniedError: If account tier lacks access (HTTP 403).
            RateLimitExceededError: If daily request quota is exceeded (HTTP 429).
            ServerError: If upstream COT Bias servers return an error (HTTP 5xx).
            CotApiError: Base exception for any unexpected API errors.

        Example:
            ```python
            from cotbias import CotClient

            client = CotClient()
            df = client.screener.scan(
                ai_bias_score="Bullish",
                crowdedness_risk="Balanced",
                as_dataframe=True,
            )
            print(df[["symbol", "regime_status", "primary_driver"]])
            ```
        """
        params: dict[str, str] = {}
        if ai_bias_score:
            params["ai_bias_score"] = ai_bias_score
        if crowdedness_risk:
            params["crowdedness_risk"] = crowdedness_risk
        if momentum:
            params["momentum"] = momentum
        if cot_positioning:
            params["cot_positioning"] = cot_positioning

        resp = self._client.get("/screener", params=params)
        handle_error_response(resp)

        parsed = ScreenerResponse.model_validate(resp.json())

        if not as_dataframe:
            return parsed

        raw_results = [r.model_dump() for r in parsed.results]
        return cast("pd.DataFrame", pd.DataFrame(raw_results))


class AsyncScreenerResource:
    """Asynchronous resource for multi-market positioning scans."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        """Initialize the async screener resource with an active async HTTP client.

        Args:
            client: Active asynchronous HTTP client session.
        """
        self._client = client

    @overload
    async def scan(
        self,
        ai_bias_score: str | None = ...,
        crowdedness_risk: str | None = ...,
        momentum: str | None = ...,
        cot_positioning: str | None = ...,
        as_dataframe: Literal[True] = ...,
    ) -> pd.DataFrame: ...

    @overload
    async def scan(
        self,
        ai_bias_score: str | None = ...,
        crowdedness_risk: str | None = ...,
        momentum: str | None = ...,
        cot_positioning: str | None = ...,
        as_dataframe: Literal[False] = ...,
    ) -> ScreenerResponse: ...

    @overload
    async def scan(
        self,
        ai_bias_score: str | None = ...,
        crowdedness_risk: str | None = ...,
        momentum: str | None = ...,
        cot_positioning: str | None = ...,
        as_dataframe: bool = ...,
    ) -> pd.DataFrame | ScreenerResponse: ...

    async def scan(
        self,
        ai_bias_score: str | None = None,
        crowdedness_risk: str | None = None,
        momentum: str | None = None,
        cot_positioning: str | None = None,
        as_dataframe: bool = True,
    ) -> pd.DataFrame | ScreenerResponse:
        """Filter across all tracked futures markets asynchronously.

        Args:
            ai_bias_score: Filter by directional bias ('Bullish', 'Bearish', 'Neutral').
            crowdedness_risk: Filter by positioning risk ('High Liquidation Risk', 'Balanced').
            momentum: Filter by open interest dynamics ('New Longs', 'Short Covering').
            cot_positioning: Filter by smart vs dumb positioning ('Convergence', 'Divergence').
            as_dataframe: When `True` (default), returns a Pandas DataFrame.
                When `False`, returns a `ScreenerResponse`.

        Returns:
            A Pandas DataFrame if `as_dataframe=True`, or a `ScreenerResponse` model if `as_dataframe=False`.

        Raises:
            AuthenticationError: If API key is missing or invalid (HTTP 401).
            PermissionDeniedError: If account tier lacks access (HTTP 403).
            RateLimitExceededError: If daily request quota is exceeded (HTTP 429).
            ServerError: If upstream COT Bias servers return an error (HTTP 5xx).
            CotApiError: Base exception for any unexpected API errors.

        Example:
            ```python
            import asyncio
            from cotbias import AsyncCotClient

            async def main():
                async with AsyncCotClient() as client:
                    results = await client.screener.scan(ai_bias_score="Bullish")
                    print(results)

            asyncio.run(main())
            ```
        """
        params: dict[str, str] = {}
        if ai_bias_score:
            params["ai_bias_score"] = ai_bias_score
        if crowdedness_risk:
            params["crowdedness_risk"] = crowdedness_risk
        if momentum:
            params["momentum"] = momentum
        if cot_positioning:
            params["cot_positioning"] = cot_positioning

        resp = await self._client.get("/screener", params=params)
        handle_error_response(resp)

        parsed = ScreenerResponse.model_validate(resp.json())

        if not as_dataframe:
            return parsed

        raw_results = [r.model_dump() for r in parsed.results]
        return cast("pd.DataFrame", pd.DataFrame(raw_results))
