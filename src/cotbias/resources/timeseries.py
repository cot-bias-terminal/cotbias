from __future__ import annotations

from typing import Literal, Union, cast, overload
import httpx
import pandas as pd

from cotbias.exceptions import handle_error_response
from cotbias.models.timeseries import TimeseriesResponse

ContractType = Literal["fut", "futopt", "opt"]
ReportType = Literal["legacy", "pro", "disaggregated", "tff", "supplemental"]


class TimeseriesResource:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    @overload
    def get(
        self,
        symbol: str,
        contract_type: ContractType = ...,
        lookback_weeks: int = ...,
        report: ReportType = ...,
        as_dataframe: Literal[True] = ...,
    ) -> pd.DataFrame: ...

    @overload
    def get(
        self,
        symbol: str,
        contract_type: ContractType = ...,
        lookback_weeks: int = ...,
        report: ReportType = ...,
        as_dataframe: Literal[False] = ...,
    ) -> TimeseriesResponse: ...

    def get(
        self,
        symbol: str,
        contract_type: ContractType = "futopt",
        lookback_weeks: int = 156,
        report: ReportType = "legacy",
        as_dataframe: bool = True,
    ) -> Union[pd.DataFrame, TimeseriesResponse]:
        """Fetch historical positioning data.

        Args:
            symbol: Asset ticker (e.g., 'GC', 'ES', 'CL', 'ZC').
            contract_type: 'fut' (Futures only), 'futopt' (Combined), or 'opt' (Options delta).
            lookback_weeks: Number of weekly reports to pull (default 156 = 3 years).
            report: 'legacy' (default), 'pro', 'disaggregated', 'tff', or 'supplemental'.
            as_dataframe: Returns a DatetimeIndex-sorted Pandas DataFrame if True, or TimeseriesResponse if False.
        """
        params = {
            "contract_type": contract_type,
            "lookback_weeks": lookback_weeks,
            "report": report,
        }
        resp = self._client.get(f"/timeseries/{symbol.upper()}", params=params)
        handle_error_response(resp)

        parsed = TimeseriesResponse.model_validate(resp.json())

        if not as_dataframe:
            return parsed

        raw_data = [row.model_dump() for row in parsed.data]
        if not raw_data:
            return cast(pd.DataFrame, pd.DataFrame())

        df = pd.DataFrame(raw_data)
        if "report_date" in df.columns:
            df["report_date"] = pd.to_datetime(df["report_date"])
            df = df.set_index("report_date").sort_index(ascending=True)

        return cast(pd.DataFrame, df)


class AsyncTimeseriesResource:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    @overload
    async def get(
        self,
        symbol: str,
        contract_type: ContractType = ...,
        lookback_weeks: int = ...,
        report: ReportType = ...,
        as_dataframe: Literal[True] = ...,
    ) -> pd.DataFrame: ...

    @overload
    async def get(
        self,
        symbol: str,
        contract_type: ContractType = ...,
        lookback_weeks: int = ...,
        report: ReportType = ...,
        as_dataframe: Literal[False] = ...,
    ) -> TimeseriesResponse: ...

    async def get(
        self,
        symbol: str,
        contract_type: ContractType = "futopt",
        lookback_weeks: int = 156,
        report: ReportType = "legacy",
        as_dataframe: bool = True,
    ) -> Union[pd.DataFrame, TimeseriesResponse]:
        params = {
            "contract_type": contract_type,
            "lookback_weeks": lookback_weeks,
            "report": report,
        }
        resp = await self._client.get(f"/timeseries/{symbol.upper()}", params=params)
        handle_error_response(resp)

        parsed = TimeseriesResponse.model_validate(resp.json())

        if not as_dataframe:
            return parsed

        raw_data = [row.model_dump() for row in parsed.data]
        if not raw_data:
            return cast(pd.DataFrame, pd.DataFrame())

        df = pd.DataFrame(raw_data)
        if "report_date" in df.columns:
            df["report_date"] = pd.to_datetime(df["report_date"])
            df = df.set_index("report_date").sort_index(ascending=True)

        return cast(pd.DataFrame, df)
