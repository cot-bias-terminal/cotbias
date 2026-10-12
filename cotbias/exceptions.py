from typing import Optional


class CotApiError(Exception):
    """Base exception for all COT Bias API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(CotApiError):
    """401: Invalid, missing, or revoked API key."""
    pass


class PermissionDeniedError(CotApiError):
    """403: Tier does not permit access to this resource."""
    pass


class NotFoundError(CotApiError):
    """404: Symbol or resource not found in market universe."""
    pass


class RateLimitExceededError(CotApiError):
    """429: API rate limit hit."""
    def __init__(self, message: str, retry_after: int = 60, **kwargs):
        super().__init__(message, status_code=429, **kwargs)
        self.retry_after = retry_after


class ServerError(CotApiError):
    """500+: Backend Cloud Function or Cloud SQL error."""
    pass