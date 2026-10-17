"""NSE Bulk & Block Deals Weekly/Daily Automated Updater.

Fetches latest official bulk and block deal disclosures from NSE archives,
classifies investor entities, deduplicates records, and exports Parquet/CSV.
"""

import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

# Add local src to path for direct execution
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from nse_bulk_block_deals.fetcher import BulkBlockFetcher

def update_bulk_block_deals():
    print(f"[{datetime.now().isoformat()}] Starting Bulk & Block Deals update...")
    fetcher = BulkBlockFetcher()
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_file = output_dir / "bulk_block_deals.csv"
    parquet_file = output_dir / "bulk_block_deals.parquet"

    existing_df = pd.DataFrame()
    if parquet_file.exists():
        existing_df = pd.read_parquet(parquet_file)
        print(f"Loaded {len(existing_df):,} existing transactions from {parquet_file.name}")

    # Fetch latest deals from NSE
    print("Fetching latest bulk and block disclosures from NSE archives...")
    new_df = fetcher.fetch_latest_deals()

    if new_df.empty and existing_df.empty:
        raise RuntimeError("No bulk/block deals retrieved and no existing database found.")

    combined = []
    if not existing_df.empty:
        combined.append(existing_df)
    if not new_df.empty:
        print(f"Retrieved {len(new_df)} transactions from latest exchange feeds.")
        combined.append(new_df)

    merged = pd.concat(combined, ignore_index=True)

    # Core key deduplication
    merged = merged.drop_duplicates(subset=["trade_date", "symbol", "client_name", "buy_sell", "quantity"], keep="last")

    # Sort deterministically
    merged = merged.sort_values(by=["trade_date", "deal_value_cr"], ascending=[False, False]).reset_index(drop=True)

    # Save
    merged.to_parquet(parquet_file, index=False, compression="snappy")
    merged.to_csv(csv_file, index=False)
    print(f"Saved {len(merged):,} transactions to {parquet_file.name} and {csv_file.name}")

    # Run quality gate
    from evaluate_quality import audit_quality
    audit_quality()
    print("Bulk & Block Deals update completed successfully.")

if __name__ == "__main__":
    update_bulk_block_deals()
