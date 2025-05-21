# database.py
import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    username TEXT,
                    stars INTEGER,
                    status TEXT,
                    timestamp TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    order_id TEXT,
                    user_id INTEGER,
                    stars INTEGER,
                    status TEXT,
                    timestamp TEXT
                )
            """)

    def add_order(self, order_id, user_id, username, stars, status, timestamp):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (order_id, user_id, username, stars, status, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (order_id, user_id, username, stars, status, timestamp)
            )

    def update_order_status(self, order_id, status):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (status, order_id))

    def get_order(self, order_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
            return cursor.fetchone()

    def get_user_orders(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
            return cursor.fetchall()

    def add_to_history(self, order_id, user_id, stars, status, timestamp):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (order_id, user_id, stars, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                (order_id, user_id, stars, status, timestamp)
            )

    def get_user_history(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
            return cursor.fetchall()

    def delete_order(self, order_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))