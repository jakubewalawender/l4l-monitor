import sqlite3
from typing import List
import config  # Import your config file


import sqlite3
from typing import List, Tuple
import config  # Import your config file

class SQLiteDatabase:
    def __init__(self):
        # Use the DB_PATH from config.py
        self.db_name = config.DB_PATH
        self.create_table()

    def create_table(self):
        """Create the table to store product IDs and names."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_ids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def store_products(self, products: List[Tuple[str, str]]):
        """Replaces old product IDs and names with the new ones in the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Step 1: Clear all old product IDs and names
        cursor.execute("DELETE FROM product_ids")

        # Step 2: Insert new product IDs and names
        cursor.executemany("""
            INSERT INTO product_ids (product_id, name) VALUES (?, ?)
        """, products)

        conn.commit()
        conn.close()

    def retrieve_products(self) -> List[Tuple[str, str]]:
        """Retrieve all stored product IDs and names from the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, name FROM product_ids")
        rows = cursor.fetchall()
        conn.close()

        return rows

    def clear_products(self):
        """Clear the stored product IDs and names (for testing or resetting purposes)."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM product_ids")
        conn.commit()
        conn.close()