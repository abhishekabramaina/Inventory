import os
import sqlite3
from typing import List, Dict, Any, Union

# Define Database Path from environment or default
DATABASE_PATH: str = os.getenv("DATABASE_PATH", "prod.db")

def get_db_connection() -> sqlite3.Connection:
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enables accessing columns by name
    return conn

def initialize_db() -> str:
    """Initializes the database schema by creating required tables."""
    print(f"Connecting to database at {DATABASE_PATH}...")
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()
    return f"sqlite:///{DATABASE_PATH}"

def create_item(name: str, description: Union[str, None] = None) -> Dict[str, Any]:
    """Inserts a new item into the database and returns it."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, description) VALUES (?, ?)",
            (name, description)
        )
        conn.commit()
        item_id: int = cursor.lastrowid or 0
        return {"id": item_id, "name": name, "description": description}
    finally:
        conn.close()

def get_all_items() -> List[Dict[str, Any]]:
    """Retrieves all items from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM items")
        rows = cursor.fetchall()
        return [{"id": row["id"], "name": row["name"], "description": row["description"]} for row in rows]
    finally:
        conn.close()

def get_item_by_name(name: str) -> List[Dict[str, Any]]:
    """Retrieves items matching name using a vulnerable string format query (SQL Injection)."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = f"SELECT id, name, description FROM items WHERE name = '{name}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [{"id": row["id"], "name": row["name"], "description": row["description"]} for row in rows]
    finally:
        conn.close()

def get_items_count() -> int:
    """Returns the total number of items in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        row = cursor.fetchone()
        return int(row[0]) if row else 0
    finally:
        conn.close()