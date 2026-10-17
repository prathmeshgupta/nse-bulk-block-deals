# NSE Bulk & Block Deals Registry

[![Daily/Weekly Bulk Block Deals Dataset Update](https://github.com/prathmeshgupta/nse-bulk-block-deals/actions/workflows/weekly_update.yml/badge.svg)](https://github.com/prathmeshgupta/nse-bulk-block-deals/actions/workflows/weekly_update.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Clean, audited, and deduplicated time-series dataset of National Stock Exchange of India (NSE) **Bulk Deals and Block Deals** with **automatic institutional entity classification**.

Tracks major institutional footprints, private equity exits, promoter transactions, and domestic mutual fund block accumulation in Indian equities.

---

### Regulatory Background & Definitions

* **Bulk Deal:** A transaction where the total quantity bought or sold exceeds **0.5% of the total outstanding equity shares** of the listed company, executed during normal market trading hours.
* **Block Deal:** A single transaction with a minimum value of **₹10 Crore**, executed through a separate dedicated 15-minute trading window (Morning session: 8:45 AM - 9:00 AM; Afternoon session: 2:05 PM - 2:20 PM) at a price within $\pm 1\%$ of previous close or current market price.

---

### Dataset Schema

Outputs are distributed in both **Apache Parquet (`snappy` compressed)** and standard **CSV**:
* `output/bulk_block_deals.parquet`
* `output/bulk_block_deals.csv`

| Field | Type | Description |
| :--- | :--- | :--- |
| `trade_date` | `string` | Trade session date in `YYYY-MM-DD` |
| `symbol` | `string` | NSE Trading Symbol (e.g. `AROGRANITE`, `AURUM`, `RELIANCE`) |
| `security_name` | `string` | Full corporate name of the equity |
| `client_name` | `string` | Full name of buying/selling client or institution |
| `deal_type` | `string` | `BULK` or `BLOCK` |
| `buy_sell` | `string` | `BUY` or `SELL` |
| `quantity` | `int64` | Number of shares executed |
| `trade_price` | `float` | Weighted average execution price |
| `deal_value_cr` | `float` | Total transaction value in ₹ Crore |
| `entity_type` | `string` | Institutional tag (`DOMESTIC_MUTUAL_FUND`, `FII_FPI_SOVEREIGN`, `INSURANCE_COMPANY`, `AIF_PE_VENTURE`, `CORPORATE_OR_HNI`) |
| `remarks` | `string` | Exchange remarks |
| `source` | `string` | Data source origin (`NSE_BULK_DEALS` / `NSE_BLOCK_DEALS`) |

---

### Automated Weekly & Daily Updates

* **Schedule**: Automated GitHub Actions workflow executes at **15:00 UTC (20:30 IST) Monday to Friday** after exchange EOD reconciliation, with a Sunday reconciliation at **02:00 UTC**.
* **Idempotent Deduplication**: Deduplicates on composite key `[trade_date, symbol, client_name, buy_sell, quantity]`.
* **Zero Secrets**: Pure public exchange feeds requiring no personal API tokens.

---

### Quickstart & CLI Usage

```bash
# 1. Clone the repository
git clone https://github.com/prathmeshgupta/nse-bulk-block-deals.git
cd nse-bulk-block-deals

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the automated updater locally
python update.py

# 4. Filter by specific ticker
python runner.py --symbol INFY

# 5. Filter by entity type and minimum deal value
python runner.py --type DOMESTIC_MUTUAL_FUND --min-value 10.0
```
