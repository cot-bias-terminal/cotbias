from __future__ import annotations

from typing import TYPE_CHECKING, Literal, cast, overload

import httpx

from cotbias.exceptions import handle_error_response
from cotbias.models.timeseries import TimeseriesResponse

if TYPE_CHECKING:
    import pandas as pd

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
        as_dataframe: Literal[False] = ...,
    ) -> TimeseriesResponse: ...

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
        contract_type: str = ...,
        lookback_weeks: int = ...,
        report: str = ...,
        as_dataframe: bool = ...,
    ) -> pd.DataFrame | TimeseriesResponse: ...

    def get(
        self,
        symbol: str,
        contract_type: str = "futopt",
        lookback_weeks: int = 156,
        report: str = "legacy",
        as_dataframe: bool = False,
    ) -> pd.DataFrame | TimeseriesResponse:
        """Fetch historical positioning data.

        Args:
            symbol: Asset ticker (e.g., 'GC', 'ES', 'CL', 'ZC').
            contract_type: 'fut' (Futures only), 'futopt' (Combined), or 'opt' (Options delta).
            lookback_weeks: Number of weekly reports to pull (default 156 = 3 years).
            report: 'legacy' (default), 'pro', 'disaggregated', 'tff', or 'supplemental'.
            as_dataframe: Returns a DatetimeIndex-sorted Pandas DataFrame if True, or TimeseriesResponse if False (default).
        """
        params: dict[str, str | int] = {
            "contract_type": contract_type,
            "lookback_weeks": lookback_weeks,
            "report": report,
        }
        resp = self._client.get(f"/timeseries/{symbol.upper()}", params=params)
        handle_error_response(resp)

        parsed = TimeseriesResponse.model_validate(resp.json())

        if not as_dataframe:
            return parsed

        try:
            import pandas as pd  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "pandas is required when as_dataframe=True. Install it via 'pip install cotbias[pandas]'."
            ) from exc

        raw_data = [row.model_dump() for row in parsed.data]
        if not raw_data:
            return cast("pd.DataFrame", pd.DataFrame())

        df = pd.DataFrame(raw_data)
        if "report_date" in df.columns:
            df["report_date"] = pd.to_datetime(df["report_date"])
            df = df.set_index("report_date").sort_index(ascending=True)

        return cast("pd.DataFrame", df)


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
        as_dataframe: Literal[False] = ...,
    ) -> TimeseriesResponse: ...

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
        contract_type: str = ...,
        lookback_weeks: int = ...,
        report: str = ...,
        as_dataframe: bool = ...,
    ) -> pd.DataFrame | TimeseriesResponse: ...

    async def get(
        self,
        symbol: str,
        contract_type: str = "futopt",
        lookback_weeks: int = 156,
        report: str = "legacy",
        as_dataframe: bool = False,
    ) -> pd.DataFrame | TimeseriesResponse:
        params: dict[str, str | int] = {
            "contract_type": contract_type,
            "lookback_weeks": lookback_weeks,
            "report": report,
        }
        resp = await self._client.get(f"/timeseries/{symbol.upper()}", params=params)
        handle_error_response(resp)

        parsed = TimeseriesResponse.model_validate(resp.json())

        if not as_dataframe:
            return parsed

        try:
            import pandas as pd  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "pandas is required when as_dataframe=True. Install it via 'pip install cotbias[pandas]'."
            ) from exc

        raw_data = [row.model_dump() for row in parsed.data]
        if not raw_data:
            return cast("pd.DataFrame", pd.DataFrame())

        df = pd.DataFrame(raw_data)
        if "report_date" in df.columns:
            df["report_date"] = pd.to_datetime(df["report_date"])
            df = df.set_index("report_date").sort_index(ascending=True)

        return cast("pd.DataFrame", df)
