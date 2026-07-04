import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "shop.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            delivered_content TEXT,
            purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_purchase(user_id: int, username: str | None, product_id: int, product_name: str, price: int, content: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO purchases (user_id, username, product_id, product_name, price, delivered_content) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, username, product_id, product_name, price, content),
    )
    conn.commit()
    conn.close()
