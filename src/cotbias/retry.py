"""HTTP transport middleware with automatic exponential backoff and jitter."""

from __future__ import annotations

import asyncio
import json
import logging
import random
import time
from typing import Any

import httpx

logger = logging.getLogger("cotbias.retry")

DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
MAX_RETRY_AFTER_SEC = 10.0


def _should_retry_response(resp: httpx.Response) -> tuple[bool, float | None]:
    """Determine if an HTTP response is retriable and calculate the required delay.

    Args:
        resp: The HTTP response to inspect.

    Returns:
        A tuple `(should_retry, delay_seconds)`.
    """
    # 5xx Server Errors are transient and retriable
    if resp.status_code in {500, 502, 503, 504}:
        return True, None

    # 429 Rate Limit - only retry if transient (not quota exhaustion and Retry-After <= 10s)
    if resp.status_code == 429:
        try:
            body: dict[str, Any] = resp.json()
            code = body.get("error", {}).get("code", "")
            if code in {"QUOTA_EXCEEDED", "DAILY_LIMIT_EXCEEDED"}:
                return False, None
        except (ValueError, TypeError, json.JSONDecodeError):
            logger.debug("Failed to decode 429 error response body as JSON.")

        raw_retry_after = resp.headers.get("Retry-After")
        if raw_retry_after is not None:
            try:
                retry_sec = float(raw_retry_after)
                if retry_sec <= MAX_RETRY_AFTER_SEC:
                    return True, retry_sec
                # If retry after is longer than 10s (e.g. daily quota reset), don't hold the caller
                return False, None
            except (ValueError, TypeError):
                pass
        # Default transient 429 without Retry-After
        return True, None

    return False, None


class RetryTransport(httpx.BaseTransport):
    """Synchronous HTTP transport middleware with exponential backoff and jitter.

    Retries transient 5xx server errors, connection timeouts, and short-duration
    transient 429 rate limit responses.
    """

    def __init__(
        self,
        transport: httpx.BaseTransport,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    ) -> None:
        """Initialize the retry transport wrapper.

        Args:
            transport: The underlying HTTP transport to delegate requests to.
            max_retries: Maximum number of retry attempts before raising.
            backoff_factor: Multiplier for exponential backoff calculations.
        """
        self._inner = transport
        self._max_retries = max(0, max_retries)
        self._backoff = backoff_factor

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        """Send the request through the inner transport with automatic retry on transient failure.

        Args:
            request: The outgoing HTTP request.

        Returns:
            The HTTP response received from the server.
        """
        request.read()
        attempts = 0

        while True:
            try:
                resp = self._inner.handle_request(request)
                if resp.status_code >= 400:
                    resp.read()
                if attempts < self._max_retries:
                    retry, delay = _should_retry_response(resp)
                    if retry:
                        attempts += 1
                        sleep_time = (
                            delay
                            if delay is not None
                            else self._backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                        )
                        logger.warning(
                            "Transient %d received for %s. Retrying in %.2fs (attempt %d/%d)...",
                            resp.status_code,
                            request.url,
                            sleep_time,
                            attempts,
                            self._max_retries,
                        )
                        time.sleep(sleep_time)
                        continue
                return resp
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                if attempts < self._max_retries:
                    attempts += 1
                    sleep_time = self._backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    logger.warning(
                        "Network/timeout error (%s) on %s. Retrying in %.2fs (attempt %d/%d)...",
                        type(e).__name__,
                        request.url,
                        sleep_time,
                        attempts,
                        self._max_retries,
                    )
                    time.sleep(sleep_time)
                    continue
                raise

    def close(self) -> None:
        """Close the underlying inner transport."""
        self._inner.close()


class AsyncRetryTransport(httpx.AsyncBaseTransport):
    """Asynchronous HTTP transport middleware with exponential backoff and jitter.

    Retries transient 5xx server errors, connection timeouts, and short-duration
    transient 429 rate limit responses asynchronously.
    """

    def __init__(
        self,
        transport: httpx.AsyncBaseTransport,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    ) -> None:
        """Initialize the async retry transport wrapper.

        Args:
            transport: The underlying async HTTP transport to delegate requests to.
            max_retries: Maximum number of retry attempts before raising.
            backoff_factor: Multiplier for exponential backoff calculations.
        """
        self._inner = transport
        self._max_retries = max(0, max_retries)
        self._backoff = backoff_factor

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        """Send the async request through the inner transport with automatic retry on transient failure.

        Args:
            request: The outgoing HTTP request.

        Returns:
            The HTTP response received from the server.
        """
        await request.aread()
        attempts = 0

        while True:
            try:
                resp = await self._inner.handle_async_request(request)
                if resp.status_code >= 400:
                    await resp.aread()
                if attempts < self._max_retries:
                    retry, delay = _should_retry_response(resp)
                    if retry:
                        attempts += 1
                        sleep_time = (
                            delay
                            if delay is not None
                            else self._backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                        )
                        logger.warning(
                            "Transient %d received for %s. Retrying in %.2fs (attempt %d/%d)...",
                            resp.status_code,
                            request.url,
                            sleep_time,
                            attempts,
                            self._max_retries,
                        )
                        await asyncio.sleep(sleep_time)
                        continue
                return resp
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                if attempts < self._max_retries:
                    attempts += 1
                    sleep_time = self._backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    logger.warning(
                        "Network/timeout error (%s) on %s. Retrying in %.2fs (attempt %d/%d)...",
                        type(e).__name__,
                        request.url,
                        sleep_time,
                        attempts,
                        self._max_retries,
                    )
                    await asyncio.sleep(sleep_time)
                    continue
                raise

    async def aclose(self) -> None:
        """Close the underlying inner async transport."""
        await self._inner.aclose()
