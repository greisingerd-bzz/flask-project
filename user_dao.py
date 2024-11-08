import sqlite3
from user import User


class UserDao:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT)"
            )

    def add_user(self, user):
        existing_user = self.get_user_by_email(user.email)
        if existing_user:
            print(f"Benutzer mit E-Mail {user.email} existiert bereits.")
            return

        with self.connection:
            self.connection.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (user.name, user.email, user.password),
            )

    def get_user_by_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, name, email, password FROM users WHERE id = ?", (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return User(id=row[0], name=row[1], email=row[2], password=row[3])
        return None

    def get_user_by_email(self, email):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, name, email, password FROM users WHERE email = ?", (email,)
        )
        row = cursor.fetchone()
        if row:
            return User(id=row[0], name=row[1], email=row[2], password=row[3])
        return None

    def close(self):
        self.connection.close()
