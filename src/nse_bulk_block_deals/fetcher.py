"""NSE Bulk and Block Deals Fetcher.

Downloads daily bulk and block deal transactions published by NSE,
standardizes schemas, computes deal value in Crore, and tags entity types.
"""

import io
import requests
import pandas as pd
from datetime import datetime, date
from typing import Optional, List
from .classifier import classify_client

NSE_BULK_URL = "https://archives.nseindia.com/content/equities/bulk.csv"
NSE_BLOCK_URL = "https://archives.nseindia.com/content/equities/block.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

class BulkBlockFetcher:
    """Fetches daily bulk and block transactions from NSE archives."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_latest_deals(self) -> pd.DataFrame:
        """Fetches both bulk and block deals currently published on NSE archives."""
        deals = []

        # 1. Bulk Deals
        df_bulk = self._fetch_feed(NSE_BULK_URL, deal_type="BULK")
        if not df_bulk.empty:
            deals.append(df_bulk)

        # 2. Block Deals
        df_block = self._fetch_feed(NSE_BLOCK_URL, deal_type="BLOCK")
        if not df_block.empty:
            deals.append(df_block)

        if not deals:
            return pd.DataFrame()

        merged = pd.concat(deals, ignore_index=True)
        return merged

    def _fetch_feed(self, url: str, deal_type: str) -> pd.DataFrame:
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code != 200 or not resp.text.strip():
                return pd.DataFrame()

            # Some files might have 'NO RECORDS' or be empty
            if "NO RECORDS" in resp.text:
                return pd.DataFrame()

            df = pd.read_csv(io.StringIO(resp.text))
            df.columns = [c.strip() for c in df.columns]

            if "Symbol" not in df.columns or "Client Name" not in df.columns:
                return pd.DataFrame()

            # Filter out any empty rows
            df = df.dropna(subset=["Symbol", "Client Name"]).copy()

            # Strip whitespace
            for col in ["Date", "Symbol", "Security Name", "Client Name", "Buy/Sell"]:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()

            # Parse Trade Date to YYYY-MM-DD
            def parse_date(d_str):
                try:
                    return pd.to_datetime(d_str).strftime("%Y-%m-%d")
                except:
                    return d_str

            df["trade_date"] = df["Date"].apply(parse_date)

            # Clean numerics
            qty_col = [c for c in df.columns if "Quantity" in c][0]
            price_col = [c for c in df.columns if "Price" in c][0]

            df["quantity"] = pd.to_numeric(df[qty_col].astype(str).str.replace(",", ""), errors="coerce").fillna(0).astype("int64")
            df["trade_price"] = pd.to_numeric(df[price_col].astype(str).str.replace(",", ""), errors="coerce").fillna(0.0)

            # Deal value in ₹ Crore (Quantity * Price / 10,000,000)
            df["deal_value_cr"] = ((df["quantity"] * df["trade_price"]) / 10000000.0).round(4)

            # Entity classification
            df["entity_type"] = df["Client Name"].apply(classify_client)

            # Standardized schema
            result = pd.DataFrame({
                "trade_date": df["trade_date"],
                "symbol": df["Symbol"],
                "security_name": df.get("Security Name", df["Symbol"]),
                "client_name": df["Client Name"],
                "deal_type": deal_type,
                "buy_sell": df["Buy/Sell"].str.upper(),
                "quantity": df["quantity"],
                "trade_price": df["trade_price"],
                "deal_value_cr": df["deal_value_cr"],
                "entity_type": df["entity_type"],
                "remarks": df.get("Remarks", "-"),
                "source": f"NSE_{deal_type}_DEALS"
            })

            # Drop invalid rows
            result = result[(result["quantity"] > 0) & (result["trade_price"] > 0.0)]
            return result

        except Exception as e:
            print(f"Error fetching {deal_type} deals from {url}: {e}")
            return pd.DataFrame()
