"""Timeseries resource endpoint for historical CFTC Commitment of Traders data."""

from __future__ import annotations

from typing import Literal, cast, overload

import httpx
import pandas as pd

from cotbias.exceptions import handle_error_response
from cotbias.models.timeseries import TimeseriesResponse

ContractType = Literal["fut", "futopt", "opt"]
ReportType = Literal["legacy", "pro", "disaggregated", "tff", "supplemental"]


class TimeseriesResource:
    """Synchronous resource for querying historical weekly COT positioning timeseries."""

    def __init__(self, client: httpx.Client) -> None:
        """Initialize the timeseries resource with an active HTTP client.

        Args:
            client: Active synchronous HTTP client session.
        """
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
        as_dataframe: bool = True,
    ) -> pd.DataFrame | TimeseriesResponse:
        """Fetch historical weekly positioning metrics for a market.

        Args:
            symbol: Asset ticker symbol (e.g., 'GC', 'ES', 'CL', '6E', 'ZB').
            contract_type: Position breakdown type:
                - `'fut'`: Futures only.
                - `'futopt'`: Combined Futures and Options (default).
                - `'opt'`: Options delta equivalent only.
            lookback_weeks: Number of weekly CFTC reports to retrieve (1 to 156, default 156).
            report: CFTC report family:
                - `'legacy'`: Commercial / Non-Commercial classifications (default).
                - `'disaggregated'`: Producer, Swap Dealer, Managed Money, Other.
                - `'tff'`: Financial Traders (Dealer, Asset Mgr, Leveraged Money).
                - `'supplemental'`: Commodity Index Trader (CIT) reports.
            as_dataframe: When `True` (default), returns a Pandas DataFrame indexed
                by `report_date` in ascending order. When `False`, returns a validated
                :class:`~cotbias.models.timeseries.TimeseriesResponse` model.

        Returns:
            A DatetimeIndex-sorted Pandas DataFrame if `as_dataframe=True`, or a
            `TimeseriesResponse` Pydantic model if `as_dataframe=False`.

        Raises:
            AuthenticationError: If API key is missing or invalid (HTTP 401).
            PermissionDeniedError: If account tier lacks access (HTTP 403).
            NotFoundError: If symbol is unrecognized or report data is missing (HTTP 404).
            RateLimitExceededError: If daily request quota is exceeded (HTTP 429).
            ServerError: If upstream COT Bias servers return an error (HTTP 5xx).
            CotApiError: Base exception for any unexpected API errors.

        Example:
            ```python
            from cotbias import CotClient

            client = CotClient()
            df = client.timeseries.get("ES", lookback_weeks=52, as_dataframe=True)
            print(df[["commercial_net", "cot_52w_commercial"]].tail())
            ```
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

        raw_data = [row.model_dump() for row in parsed.data]
        if not raw_data:
            return cast("pd.DataFrame", pd.DataFrame())

        df = pd.DataFrame(raw_data)
        if "report_date" in df.columns:
            df["report_date"] = pd.to_datetime(df["report_date"])
            df = df.set_index("report_date").sort_index(ascending=True)

        return cast("pd.DataFrame", df)


class AsyncTimeseriesResource:
    """Asynchronous resource for querying historical weekly COT positioning timeseries."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        """Initialize the async timeseries resource with an active async HTTP client.

        Args:
            client: Active asynchronous HTTP client session.
        """
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
        as_dataframe: bool = True,
    ) -> pd.DataFrame | TimeseriesResponse:
        """Fetch historical weekly positioning metrics for a market asynchronously.

        Args:
            symbol: Asset ticker symbol (e.g., 'GC', 'ES', 'CL', '6E', 'ZB').
            contract_type: Position breakdown type:
                - `'fut'`: Futures only.
                - `'futopt'`: Combined Futures and Options (default).
                - `'opt'`: Options delta equivalent only.
            lookback_weeks: Number of weekly CFTC reports to retrieve (1 to 156, default 156).
            report: CFTC report family ('legacy', 'disaggregated', 'tff', 'supplemental').
            as_dataframe: When `True` (default), returns a Pandas DataFrame indexed
                by `report_date` in ascending order. When `False`, returns a validated
                `TimeseriesResponse` model.

        Returns:
            A DatetimeIndex-sorted Pandas DataFrame if `as_dataframe=True`, or a
            `TimeseriesResponse` Pydantic model if `as_dataframe=False`.

        Raises:
            AuthenticationError: If API key is missing or invalid (HTTP 401).
            PermissionDeniedError: If account tier lacks access (HTTP 403).
            NotFoundError: If symbol is unrecognized or report data is missing (HTTP 404).
            RateLimitExceededError: If daily request quota is exceeded (HTTP 429).
            ServerError: If upstream COT Bias servers return an error (HTTP 5xx).
            CotApiError: Base exception for any unexpected API errors.

        Example:
            ```python
            import asyncio
            from cotbias import AsyncCotClient

            async def main():
                async with AsyncCotClient() as client:
                    df = await client.timeseries.get("GC", lookback_weeks=26)
                    print(df.tail())

            asyncio.run(main())
            ```
        """
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

        raw_data = [row.model_dump() for row in parsed.data]
        if not raw_data:
            return cast("pd.DataFrame", pd.DataFrame())

        df = pd.DataFrame(raw_data)
        if "report_date" in df.columns:
            df["report_date"] = pd.to_datetime(df["report_date"])
            df = df.set_index("report_date").sort_index(ascending=True)

        return cast("pd.DataFrame", df)
