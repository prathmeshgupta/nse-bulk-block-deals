"""CLI Tool for NSE Bulk and Block Deals.

Usage:
    python runner.py --symbol INFY
    python runner.py --type DOMESTIC_MUTUAL_FUND
    python runner.py --min-value 5.0
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="NSE Bulk & Block Deals CLI")
    parser.add_argument("--symbol", help="Target equity ticker")
    parser.add_argument("--type", help="Filter by entity type (DOMESTIC_MUTUAL_FUND, FII_FPI_SOVEREIGN, INSURANCE_COMPANY, etc.)")
    parser.add_argument("--min-value", type=float, default=0.0, help="Minimum deal value in Rs. Crore")
    args = parser.parse_args()

    parquet_path = Path(__file__).parent / "output" / "bulk_block_deals.parquet"
    if not parquet_path.exists():
        print("Dataset not found. Run python update.py first.")
        return

    df = pd.read_parquet(parquet_path)

    if args.symbol:
        df = df[df["symbol"] == args.symbol.upper()]
    if args.type:
        df = df[df["entity_type"] == args.type.upper()]
    if args.min_value > 0:
        df = df[df["deal_value_cr"] >= args.min_value]

    if df.empty:
        print("No matching transactions found.")
        return

    latest_date = df["trade_date"].max()
    print(f"\n--- NSE Bulk & Block Transactions (Showing {len(df)} deals) ---")
    cols = ["trade_date", "symbol", "deal_type", "buy_sell", "client_name", "quantity", "trade_price", "deal_value_cr", "entity_type"]
    print(df[cols].to_string(index=False))

if __name__ == "__main__":
    main()
