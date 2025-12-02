class PaySimSDKError(Exception):
    """Base SDK error."""

class APIRequestError(PaySimSDKError):
    """Raised when the API returns a non-2xx response."""

class NotFoundError(APIRequestError):
    """Resource not found."""

class ValidationError(APIRequestError):
    """Validation error from API."""

class ConnectionError(PaySimSDKError):
    """Network / connection error."""
