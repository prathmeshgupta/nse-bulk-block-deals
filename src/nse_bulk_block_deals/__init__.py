"""NSE Bulk and Block Deals Package."""

from .fetcher import BulkBlockFetcher
from .classifier import classify_client

__all__ = ["BulkBlockFetcher", "classify_client"]
__version__ = "0.1.0"
