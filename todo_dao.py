""" This module contains the TodoDao class, which is responsible for interacting with the SQLite database. """
import sqlite3
from todo_item import TodoItem

class TodoDao:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS todo_items""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS todo_items (
                item_id INTEGER PRIMARY KEY,
                title TEXT,
                is_completed BOOLEAN,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )"""
        )
        self.conn.commit()

    def add_item(self, todo_item):
        self.cursor.execute(
            "INSERT INTO todo_items (user_id, title, is_completed) VALUES (?, ?, ?)",
            (todo_item.user_id, todo_item.title, todo_item.is_completed),
        )
        self.conn.commit()

    def get_item(self, item_id, user_id):
        self.cursor.execute(
            "SELECT * FROM todo_items WHERE item_id = ? AND user_id = ?",
            (item_id, user_id),
        )
        row = self.cursor.fetchone()
        if row:
            return TodoItem(row[0], row[3], row[1], row[2])
        return None

    def get_all_items(self, user_id):
        self.cursor.execute("SELECT * FROM todo_items WHERE user_id = ?", (user_id,))
        rows = self.cursor.fetchall()
        todo_items = [TodoItem(row[0], row[3], row[1], row[2]) for row in rows]
        return todo_items

    def update_item(self, todo_item):
        self.cursor.execute(
            "UPDATE todo_items SET title = ?, is_completed = ? WHERE item_id = ?",
            (todo_item.title, todo_item.is_completed, todo_item.item_id),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_item(self, item_id, user_id):
        self.cursor.execute(
            "DELETE FROM todo_items WHERE item_id = ? AND user_id = ?",
            (item_id, user_id),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        """Closes the database connection."""
        self.conn.close()
