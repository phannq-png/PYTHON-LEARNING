import sqlite3
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS glossary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            japanese TEXT NOT NULL,
            vietnamese TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(query)
        self.conn.commit()
    
    def fetch_all(self):
        query = "SELECT * FROM glossary ORDER BY id"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        # return [dict(zip(column_names, row)) for row in rows]
        return rows

    def add_entry(self, japanese, vietnamese):
        query = "INSERT INTO glossary (japanese, vietnamese) VALUES (?, ?)"
        self.cursor.execute(query, (japanese, vietnamese))
        self.conn.commit()

    def update_entry(self, id, japanese, vietnamese):
        query = "UPDATE glossary SET japanese = ?, vietnamese = ? WHERE id = ?"
        self.cursor.execute(query, (japanese, vietnamese, id))
        self.conn.commit()

    def delete_entry(self, id):
        query = "DELETE FROM glossary WHERE id = ?"
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def is_dupplicate(self, japanese):
        query = "SELECT COUNT(*) FROM glossary WHERE japanese = ?"
        self.cursor.execute(query, (japanese,))
        count = self.cursor.fetchone()[0]
        return count > 0
    
    def clear_all(self):
        query = "DELETE FROM glossary"
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.conn.close()