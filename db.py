import sqlite3
from typing import List
import config  # Import your config file


class SQLiteDatabase:
    def __init__(self):
        # Use the DB_PATH from config.py
        self.db_name = config.DB_PATH
        self.create_table()

    def create_table(self):
        """Create the table to store product IDs."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_ids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT UNIQUE NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def store_product_ids(self, product_ids: List[str]):
        """Replaces old product IDs with the new ones in the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Step 1: Clear all old product IDs
        cursor.execute("DELETE FROM product_ids")

        # Step 2: Insert new product IDs
        cursor.executemany("""
            INSERT INTO product_ids (product_id) VALUES (?)
        """, [(product_id,) for product_id in product_ids])

        conn.commit()
        conn.close()

    def retrieve_product_ids(self) -> List[str]:
        """Retrieve all stored product IDs from the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT product_id FROM product_ids")
        rows = cursor.fetchall()
        conn.close()

        return [row[0] for row in rows]

    def clear_product_ids(self):
        """Clear the stored product IDs (for testing or resetting purposes)."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM product_ids")
        conn.commit()
        conn.close()
