# Data Engineering Architecture: Retail ABM to OLAP

## 1. System Pipeline Overview

```text
[ Retail ABM Simulator ]
           │
           ▼ (POS Log Generation)
[ Raw Landing Zone: /data/raw/ ]
  ├── pos_transactions.csv
  ├── pos_transaction_items.csv
  ├── cashier_shifts.csv
  └── inventory_catalog.csv
           │
           ▼ (Ingestion Script: OLTP Loader)
[ PostgreSQL: OLTP Layer (3NF) ]
  ├── stores
  ├── cashiers
  ├── customers
  ├── products
  ├── orders
  ├── order_items
  └── cashier_shifts
           │
           ▼ (Extract & Staging - Scheduled by Apache Airflow)
[ Staging Area: Bronze / Silver Cleanse ]
  - Filter voided items
  - Deduplicate double scans (< 1s interval)
  - Reconcile invalid / mutated SKU typos against product catalog
  - Handle null or missing member IDs
           │
           ▼ (Transform & Dimensional Modeling via Python / PySpark)
[ PostgreSQL / Parquet: OLAP Layer (Star Schema) ]
  ├── dim_date
  ├── dim_product
  ├── dim_cashier
  ├── dim_customer
  ├── fact_sales
  └── fact_cashier_daily_performance
           │
           ▼ (Analytics & Machine Learning)
[ Tableau Dashboard & Time-Series Forecasting ]
```

## 2. Injected Human Error Matrix & Cleansing Rules

| Error Category | Simulation Trigger | Data Engineering Cleansing Strategy |
| :--- | :--- | :--- |
| **DOUBLE_SCAN** | High scan velocity in senior cashiers or fatigued cashiers | Detect identical `transaction_id` + `sku` within consecutive sequences. Consolidate into single legitimate scan or flag for reconciliation. |
| **TYPO_SKU** | Wrinkled barcode requiring manual cashier entry | Join `order_items.sku` against `products.sku`. Unmatched keys get routed to a dead-letter quarantine table (`quarantine_unmatched_skus`). |
| **VOID_ITEM** | Customer budget shortfall or cashier scan correction | Exclude items where `is_void = TRUE` from gross revenue calculations in `fact_sales`, but track in audit/loss metric facts. |
| **MISSING_MEMBER** | Cashier rush / fatigue neglecting loyalty query | Impute customer identifier to `CUST-GUEST` and link to `dim_customer` default anonymous record. |
| **WRONG_PAYMENT** | Muscle memory cashier button mismatch | Cross-validate against settlement logs during daily bank audit reconciliation. |

## 3. Recommended Next Implementation Steps

1. Execute `oltp_schema.sql` inside a local PostgreSQL instance.
2. Build an ingestion script (`load_oltp.py`) to stream raw CSV data into PostgreSQL tables.
3. Write an extraction and cleansing script (`cleanse_silver.py`) implementing the deduplication and quarantine rules.
4. Populate the dimensional Star Schema tables using `olap_star_schema.sql`.
5. Create an Apache Airflow DAG (`retail_daily_etl_dag.py`) to automate steps 2 through 4 on a scheduled trigger.
