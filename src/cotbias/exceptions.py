from __future__ import annotations

from typing import Any
import httpx


class CotApiError(Exception):
    """Base exception for all COT Bias API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        code: str | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.response_body = response_body


class AuthenticationError(CotApiError):
    """401: Invalid, missing, or expired API key."""

    pass


class PermissionDeniedError(CotApiError):
    """403: API key revoked or tier does not permit access."""

    pass


class NotFoundError(CotApiError):
    """404: Symbol, report, or resource not found in market universe."""

    pass


class RateLimitExceededError(CotApiError):
    """429: API rate limit or daily quota exceeded."""

    def __init__(
        self,
        message: str,
        retry_after: int = 60,
        code: str = "RATE_LIMIT_EXCEEDED",
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=429, code=code, response_body=response_body)
        self.retry_after = retry_after


class ServerError(CotApiError):
    """500+: Backend Cloud Function or Cloud SQL error."""

    pass


def handle_error_response(resp: httpx.Response) -> None:
    """Parse API error envelope and raise the appropriate typed exception."""
    if resp.is_success:
        return

    body: dict[str, Any] = {}
    try:
        body = resp.json()
    except Exception:
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
