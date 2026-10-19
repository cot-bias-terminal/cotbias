"""Exception classes and error handling utilities for the COT Bias Quant API."""

from __future__ import annotations

import json
from typing import Any

import httpx


class CotApiError(Exception):
    """Base exception for all COT Bias API errors.

    Attributes:
        message: Human-readable error message.
        status_code: HTTP status code returned by the upstream API (e.g. 401, 403, 429, 500).
        code: Machine-readable error code string (e.g. `'RATE_LIMIT_EXCEEDED'`).
        response_body: Decoded JSON response payload from the API server, if available.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        code: str | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the API error.

        Args:
            message: Human-readable error message.
            status_code: HTTP status code if known.
            code: Internal error code string if returned by API.
            response_body: Raw parsed dictionary from the server error response.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.response_body = response_body


class AuthenticationError(CotApiError):
    """Raised when an API request fails authentication (HTTP 401).

    Typically indicates a missing, invalid, or expired Quant tier API key.
    """


class PermissionDeniedError(CotApiError):
    """Raised when the provided API key does not have access permissions (HTTP 403).

    Typically indicates an account on a tier insufficient for quant/API data access.
    """


class NotFoundError(CotApiError):
    """Raised when the requested asset, ticker symbol, or report was not found (HTTP 404)."""


class RateLimitExceededError(CotApiError):
    """Raised when the API rate limit or daily quota is exceeded (HTTP 429).

    Attributes:
        retry_after: Seconds to wait before attempting another request.
    """

    def __init__(
        self,
        message: str,
        retry_after: int = 60,
        code: str = "RATE_LIMIT_EXCEEDED",
        response_body: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the rate limit error.

        Args:
            message: Human-readable rate limit message.
            retry_after: Recommended wait interval in seconds.
            code: Machine-readable error code.
            response_body: Raw parsed error dictionary.
        """
        super().__init__(message, status_code=429, code=code, response_body=response_body)
        self.retry_after = retry_after


class ServerError(CotApiError):
    """Raised when the upstream COT Bias server encounters an internal error (HTTP 5xx)."""


def handle_error_response(resp: httpx.Response) -> None:
    """Parse API error response envelopes and raise corresponding typed exceptions.

    Args:
        resp: HTTPX response object to inspect.

    Raises:
        AuthenticationError: If status code is 401.
        PermissionDeniedError: If status code is 403.
        NotFoundError: If status code is 404.
        RateLimitExceededError: If status code is 429.
        ServerError: If status code is >= 500.
        CotApiError: If status code is any other HTTP error (>= 400).
    """
    if resp.is_success:
        return

    body: dict[str, Any] = {}
    try:
        body = resp.json()
    except (ValueError, TypeError, json.JSONDecodeError):
        body = {}

    err = body.get("error", {})
    code = err.get("code")
    message = err.get("message") or resp.text or f"HTTP {resp.status_code}"
    status = resp.status_code

    if status == 401:
        raise AuthenticationError(message, status_code=401, code=code, response_body=body)
    elif status == 403:
        raise PermissionDeniedError(message, status_code=403, code=code, response_body=body)
    elif status == 404:
        raise NotFoundError(message, status_code=404, code=code, response_body=body)
    elif status == 429:
        try:
            retry_after = int(resp.headers.get("Retry-After", 60))
        except (ValueError, TypeError):
            retry_after = 60
        raise RateLimitExceededError(message, retry_after=retry_after, code=code, response_body=body)
    elif status >= 500:
        raise ServerError(message, status_code=status, code=code, response_body=body)
    else:
        raise CotApiError(message, status_code=status, code=code, response_body=body)
