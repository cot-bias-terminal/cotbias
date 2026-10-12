from typing import Optional, Union
import httpx
import pandas as pd


class ScreenerResource:
    def __init__(self, client: httpx.Client):
        self._client = client

    def scan(
        self,
        ai_bias_score: Optional[str] = None,
        crowdedness_risk: Optional[str] = None,
        momentum: Optional[str] = None,
        cot_positioning: Optional[str] = None,
        as_dataframe: bool = True,
    ) -> Union[pd.DataFrame, list[dict]]:
        """Filter across all tracked markets based on inference classifications."""
        params = {}
        if ai_bias_score:
            params["ai_bias_score"] = ai_bias_score
        if crowdedness_risk:
            params["crowdedness_risk"] = crowdedness_risk
        if momentum:
            params["momentum"] = momentum
        if cot_positioning:
            params["cot_positioning"] = cot_positioning

        resp = self._client.get("/screener", params=params)
        resp.raise_for_status()

        data = resp.json().get("results", [])
        return pd.DataFrame(data) if as_dataframe else data


class AsyncScreenerResource:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def scan(
        self,
        ai_bias_score: Optional[str] = None,
        crowdedness_risk: Optional[str] = None,
        momentum: Optional[str] = None,
        cot_positioning: Optional[str] = None,
        as_dataframe: bool = True,
    ) -> Union[pd.DataFrame, list[dict]]:
        params = {}
        if ai_bias_score:
            params["ai_bias_score"] = ai_bias_score
        if crowdedness_risk:
            params["crowdedness_risk"] = crowdedness_risk
        if momentum:
            params["momentum"] = momentum
        if cot_positioning:
            params["cot_positioning"] = cot_positioning

        resp = await self._client.get("/screener", params=params)
        resp.raise_for_status()

        data = resp.json().get("results", [])
        return pd.DataFrame(data) if as_dataframe else data