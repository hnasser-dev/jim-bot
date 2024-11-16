import sqlite3
import sys


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            # self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print("Database connected.")
        except sqlite3.Error as e:
            sys.exit(f"Database connection error: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("Database disconnected.")

    def execute_query(self, query, params={}, return_columns=False):
        self.cursor.execute(query, params)
        data = self.cursor.fetchall()
        if return_columns: 
            column_names = [description[0] for description in self.cursor.description]
            return data, column_names
        self.conn.commit()
        return data