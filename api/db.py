#Database connection and table creation for saving warehouse data to disk

import os 
import sqlite3

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