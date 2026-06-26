"""Onspring API SDK.

Provides sync and async clients for interacting with the Onspring API v2.
"""

from onspring_api_sdk.async_client import AsyncOnspringClient
from onspring_api_sdk.client import OnspringClient
from onspring_api_sdk.errors import (
    OnspringAuthenticationError,
    OnspringError,
    OnspringNotFoundError,
    OnspringRateLimitError,
)

__all__ = [
    "OnspringClient",
    "AsyncOnspringClient",
    "OnspringError",
    "OnspringAuthenticationError",
    "OnspringNotFoundError",
    "OnspringRateLimitError",
]
