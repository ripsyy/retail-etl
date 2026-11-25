from datetime import date, timedelta
from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATABASE_PATH = PROJECT_ROOT / "db" / "orders.db"


def create_sample_orders(input_path: Path) -> None:
    """Write 30 example orders, including a few blank quantities."""
    products = [("Widget", 9.99), ("Gadget", 19.50), ("Cable", 4.25)]
    orders = []
    for index in range(30):
        product, unit_price = products[index % len(products)]
        quantity = None if index in (4, 12, 23) else index % 5 + 1
        order_date = date(2025, 1, 1) + timedelta(days=index)
        orders.append(
            {
                "order_id": 1001 + index,
                "order_date": order_date.isoformat(),
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
            }
        )

    input_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(orders).to_csv(input_path, index=False)


def run_etl(
    raw_data_dir: Path,
    processed_data_dir: Path,
    database_path: Path,
) -> None:
    """Create, clean, and load orders, then print a few summary KPIs."""
    input_path = raw_data_dir / "orders.csv"
    if not input_path.exists():
        create_sample_orders(input_path)

    orders = pd.read_csv(input_path)
    orders["quantity"] = orders["quantity"].fillna(1).astype(int)
    orders["unit_price"] = orders["unit_price"].astype(float)
    orders["revenue"] = orders["quantity"] * orders["unit_price"]

    processed_data_dir.mkdir(parents=True, exist_ok=True)
    output_path = processed_data_dir / "orders_clean.csv"
    orders.to_csv(output_path, index=False)

    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        orders.to_sql("orders_clean", connection, if_exists="replace", index=False)

    top_product = orders.groupby("product")["revenue"].sum().idxmax()
    print(f"total_orders: {len(orders)}")
    print(f"total_revenue: {orders['revenue'].sum():.2f}")
    print(f"top_product_by_revenue: {top_product}")


def main() -> None:
    run_etl(RAW_DATA_DIR, PROCESSED_DATA_DIR, DATABASE_PATH)


if __name__ == "__main__":
    main()
