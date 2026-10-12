from typing import Literal, Union
import httpx
import pandas as pd
from cotbias.exceptions import AuthenticationError, NotFoundError, CotApiError


ContractType = Literal["fut", "futopt", "opt"]


class TimeseriesResource:
    def __init__(self, client: httpx.Client):
        self._client = client

    def get(
        self,
        symbol: str,
        contract_type: ContractType = "futopt",
        lookback_weeks: int = 156,
        as_dataframe: bool = True,
    ) -> Union[pd.DataFrame, list[dict]]:
        """Fetch historical positioning data.
        
        Args:
            symbol: Asset ticker (e.g., 'GC', 'ES', 'CL', 'ZC').
            contract_type: 'fut' (Futures only), 'futopt' (Combined), or 'opt' (Options delta).
            lookback_weeks: Number of weekly reports to pull (default 156 = 3 years).
            as_dataframe: Returns a DatetimeIndex-sorted Pandas DataFrame if True.
        """
        params = {
            "contract_type": contract_type,
            "lookback_weeks": lookback_weeks,
        }
        resp = self._client.get(f"/timeseries/{symbol.upper()}", params=params)

        if resp.status_code == 401:
            raise AuthenticationError("Invalid API key", status_code=401)
        elif resp.status_code == 404:
            raise NotFoundError(f"Market '{symbol}' not found", status_code=404)
        elif resp.status_code != 200:
            raise CotApiError(f"Timeseries request failed: {resp.text}", status_code=resp.status_code)

        data = resp.json().get("data", [])

        if not as_dataframe:
            return data

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        if "report_date" in df.columns:
            df["report_date"] = pd.to_datetime(df["report_date"])
            df = df.set_index("report_date").sort_index(ascending=True)

        return df


class AsyncTimeseriesResource:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def get(
        self,
        symbol: str,
        contract_type: ContractType = "futopt",
        lookback_weeks: int = 156,
        as_dataframe: bool = True,
    ) -> Union[pd.DataFrame, list[dict]]:
        params = {"contract_type": contract_type, "lookback_weeks": lookback_weeks}
        resp = await self._client.get(f"/timeseries/{symbol.upper()}", params=params)

        if resp.status_code != 200:
            raise CotApiError(f"Request failed: {resp.text}", status_code=resp.status_code)

        data = resp.json().get("data", [])
        if not as_dataframe or not data:
            return data

        df = pd.DataFrame(data)
        if "report_date" in df.columns:
            df["report_date"] = pd.to_datetime(df["report_date"])
            df = df.set_index("report_date").sort_index(ascending=True)
        return df