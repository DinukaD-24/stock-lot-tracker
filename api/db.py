#Database connection and table creation for saving warehouse data to disk

import os 
import sqlite3
from datetime import date
from decimal import Decimal

from core.models import Lot, Product, StockItem
from core.warehouse import Warehouse

DB_PATH = os.environ.get("DB_PATH", "data/stock.db")

def _connect() -> sqlite3.Connection:
    #Connection to the SQLite database file and creates the data folder if needed
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    #creates database tables if they do not exist yet
    conn = _connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            selling_price TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lots (
            lot_number TEXT PRIMARY KEY,
            item_code TEXT NOT NULL,
            quantity_received TEXT NOT NULL,
            unit_cost TEXT NOT NULL,
            received_date TEXT NOT NULL,
            quantity_remaining TEXT NOT NULL,
            FOREIGN KEY(item_code) REFERENCES items (code)
        )
        """
    )
    conn.commit()
    conn.close()

def load_warehouse() -> Warehouse:
    #reads stored items and lots from SQLite to rebuild the warehouse in memory on startup
    wh = Warehouse()
    conn = _connect()
    for row in conn.execute("SELECT * FROM items"):
        if row["selling_price"] is not None:
            item = Product(
                row["code"], row["name"], row["unit"], Decimal(row["selling_price"])
            )
        else:
            item = StockItem(row["code"], row["name"], row["unit"])
        wh.add_item(item)

    for row in conn.execute(
        "SELECT * FROM lots ORDER BY received_date, lot_number"
    ):
        lot = Lot(
            lot_number=row["lot_number"],
            item_code=row["item_code"],
            quantity_received=Decimal(row["quantity_received"]),
            unit_cost=Decimal(row["unit_cost"]),
            received_date=date.fromisoformat(row["received_date"]),
        )
        #restore current remaining stock quantity for this lot
        lot.quantity_remaining = Decimal(row["quantity_remaining"])
        wh._lots[lot.item_code].append(lot)

    conn.close()
    return wh

def save_item(item: StockItem) -> None:
    #saves a single new item or product into the database table
    conn = _connect()
    selling_price = (
        str(item.selling_price) if isinstance(item, Product) else None
    )
    conn.execute(
        "INSERT INTO items (code, name, unit, selling_price) VALUES (?, ?, ?, ?)",
        (item.code, item.name, item.unit, selling_price),
    )
    conn.commit()
    conn.close()

def save_lot(lot: Lot) -> None:
    #Saves a new inventory lot batch into the database table
    conn = _connect()
    conn.execute(
        """INSERT INTO lots
            (lot_number, item_code, quantity_received, unit_cost, received_date, quantity_remaining)
            VALUES (?, ? ,? ,? ,?, ?)""",
        (
            lot.lot_number,
            lot.item_code,
            str(lot.quantity_received),
            str(lot.unit_cost),
            lot.received_date.isoformat(),
            str(lot.quantity_remaining),
        ),
    )
    conn.commit()
    conn.close()

def update_lot_remaining(lot_number: str, quantity_remaning: Decimal) -> None:
    #updates remaining quantity of a lot in the database after stock is issued
    conn = _connect()
    conn.execute(
        "UPDATE lots SET quantity_remaining = ? WHERE lot_number = ?",
        (str(quantity_remaning), lot_number),
    )
    conn.commit()
    conn.close()