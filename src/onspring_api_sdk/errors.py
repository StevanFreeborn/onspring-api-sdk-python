"""Custom exception hierarchy for Onspring API errors."""

import json

import httpx


def _get_error_message(response: httpx.Response) -> str | None:
    """Safely extract an error message from an API response body."""
    try:
        body = response.json()
        if isinstance(body, dict):
            return body.get("message")
    except (json.JSONDecodeError, ValueError, AttributeError):
        pass
    return None


class OnspringError(Exception):
    """Base exception for all Onspring API errors."""


class OnspringAuthenticationError(OnspringError):
    """Raised when the API returns a 401 or 403 status code."""


class OnspringNotFoundError(OnspringError):
    """Raised when the API returns a 404 status code."""


class OnspringRateLimitError(OnspringError):
    """Raised when the API returns a 429 status code."""
