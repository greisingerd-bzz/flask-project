import sqlite3
from todo_item import TodoItem


class TodoDao:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, description TEXT, completed BOOLEAN, user_id INTEGER)"
            )

    def add_item(self, item):
        with self.connection:
            self.connection.execute(
                "INSERT INTO todos (description, completed, user_id) VALUES (?, ?, ?)",
                (item.description, item.completed, item.user_id),
            )

    def get_items_by_user_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, description, completed, user_id FROM todos WHERE user_id = ?", (user_id,)
        )
        rows = cursor.fetchall()
        return [TodoItem(id=row[0], description=row[1], completed=bool(row[2]), user_id=row[3]) for row in rows]

    def close(self):
        self.connection.close()

    def delete_item(self, todo_id):
        with self.connection:
            self.connection.execute(
                "DELETE FROM todos WHERE id = ?", (todo_id,)
            )