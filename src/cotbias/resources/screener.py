from __future__ import annotations

from typing import TYPE_CHECKING, Literal, cast, overload

import httpx

from cotbias.exceptions import handle_error_response
from cotbias.models.screener import ScreenerResponse

if TYPE_CHECKING:
    import pandas as pd


class ScreenerResource:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

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
        as_dataframe: Literal[True] = ...,
    ) -> pd.DataFrame: ...

    def scan(
        self,
        ai_bias_score: str | None = None,
        crowdedness_risk: str | None = None,
        momentum: str | None = None,
        cot_positioning: str | None = None,
        as_dataframe: bool = False,
    ) -> pd.DataFrame | ScreenerResponse:
        """Filter across all tracked markets based on inference classifications."""
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

        try:
            import pandas as pd  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "pandas is required when as_dataframe=True. Install it via 'pip install cotbias[pandas]'."
            ) from exc

        raw_results = [r.model_dump() for r in parsed.results]
        return cast("pd.DataFrame", pd.DataFrame(raw_results))


class AsyncScreenerResource:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

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
        as_dataframe: Literal[True] = ...,
    ) -> pd.DataFrame: ...

    async def scan(
        self,
        ai_bias_score: str | None = None,
        crowdedness_risk: str | None = None,
        momentum: str | None = None,
        cot_positioning: str | None = None,
        as_dataframe: bool = False,
    ) -> pd.DataFrame | ScreenerResponse:
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

        try:
            import pandas as pd  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "pandas is required when as_dataframe=True. Install it via 'pip install cotbias[pandas]'."
            ) from exc

        raw_results = [r.model_dump() for r in parsed.results]
        return cast("pd.DataFrame", pd.DataFrame(raw_results))
