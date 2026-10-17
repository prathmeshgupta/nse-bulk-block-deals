"""Quality and Integrity Audit for NSE Bulk & Block Deals Dataset."""

import pandas as pd
from pathlib import Path

def audit_quality():
    print("=" * 65)
    print(" NSE BULK & BLOCK DEALS - DATA QUALITY AUDIT")
    print("=" * 65)

    parquet_path = Path(__file__).parent / "output" / "bulk_block_deals.parquet"
    assert parquet_path.exists(), f"Missing {parquet_path.name}"

    df = pd.read_parquet(parquet_path)
    print(f"Total Transactions Indexed: {len(df):,}")

    null_syms = df["symbol"].isnull().sum()
    null_dates = df["trade_date"].isnull().sum()
    null_clients = df["client_name"].isnull().sum()

    print(f"Null Symbols: {null_syms} {'[PASS]' if null_syms == 0 else '[FAIL]'}")
    print(f"Null Trade Dates: {null_dates} {'[PASS]' if null_dates == 0 else '[FAIL]'}")
    print(f"Null Client Names: {null_clients} {'[PASS]' if null_clients == 0 else '[FAIL]'}")

    # Integrity: quantity > 0 and price > 0
    invalid_trades = ((df["quantity"] <= 0) | (df["trade_price"] <= 0.0)).sum()
    print(f"Invalid Trades (Qty <= 0 or Price <= 0): {invalid_trades} {'[PASS]' if invalid_trades == 0 else '[FAIL]'}")

    # Entity breakdown
    print("\nTransactions by Institutional Entity Type:")
    for ent, cnt in df["entity_type"].value_counts().items():
        print(f"  • {ent:<28}: {cnt:>4} deals")

    assert null_syms == 0, "Symbols contain nulls!"
    assert null_dates == 0, "Trade dates contain nulls!"
    assert invalid_trades == 0, "Invalid quantities or prices!"

    print("=" * 65)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 65)

if __name__ == "__main__":
    audit_quality()
