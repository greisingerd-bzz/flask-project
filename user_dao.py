""" This module contains the UserDao class, which is responsible for handling all database operations related to the User model. """
import sqlite3
from user import User

class UserDao:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_user_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS users""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT,
                password TEXT
            )"""
        )
        self.conn.commit()

    def add_user(self, user):
        self.cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (user.username, user.email, user.password),
        )
        self.conn.commit()

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None

    def get_user_by_username(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        """Closes the database connection."""
        self.conn.close()
