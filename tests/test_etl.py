import sqlite3

import pandas as pd

from src.etl import run_etl


def test_revenue_column_exists_and_non_negative(tmp_path):
    raw_data_dir = tmp_path / "raw"
    processed_data_dir = tmp_path / "processed"
    database_path = tmp_path / "db" / "orders.db"

    run_etl(raw_data_dir, processed_data_dir, database_path)

    orders = pd.read_csv(processed_data_dir / "orders_clean.csv")
    assert "revenue" in orders.columns
    assert (orders["revenue"] >= 0).all()
    with sqlite3.connect(database_path) as connection:
        loaded_orders = pd.read_sql_query("SELECT * FROM orders_clean", connection)
    assert len(loaded_orders) == len(orders)


def test_missing_quantity_filled_with_one(tmp_path):
    raw_data_dir = tmp_path / "raw"
    processed_data_dir = tmp_path / "processed"
    database_path = tmp_path / "db" / "orders.db"

    run_etl(raw_data_dir, processed_data_dir, database_path)

    raw_orders = pd.read_csv(raw_data_dir / "orders.csv")
    orders = pd.read_csv(processed_data_dir / "orders_clean.csv")
    missing_quantity_rows = raw_orders.index[raw_orders["quantity"].isna()]
    assert len(missing_quantity_rows) == 3
    assert (orders.loc[missing_quantity_rows, "quantity"] == 1).all()
