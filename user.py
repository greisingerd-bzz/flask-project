"""This module defines the User class used for authentication with Flask-Login."""

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
