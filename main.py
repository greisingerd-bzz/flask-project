"""Main file for Flask application with user registration, login, and todo management."""

from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, login_required, current_user
from user_blueprint import user_blueprint
from todo_blueprint import todo_blueprint
from user_dao import UserDao
from user import User
from todo_dao import TodoDao
from todo_item import TodoItem

# Flask app setup
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'user_blueprint.login'
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(todo_blueprint)


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user_dao = UserDao('todo_example.db')
    return user_dao.get_user_by_id(int(user_id))


@app.route('/')
def home():
    """Redirect to registration page if not logged in."""
    if not current_user.is_authenticated:
        return redirect(url_for('user_blueprint.register'))
    return redirect(url_for('index'))


def generate_testdata():
    """Generate test data for the application."""
    print("Erstellen von Testdaten...")
    todo_dao = TodoDao('todo_example.db')
    user_dao = UserDao('todo_example.db')

    # Create user table and add test user
    user_dao.create_user_table()
    print("Erstelle Benutzer 'Dennis' mit Passwort 'password123'.")
    user_dao.add_user(User(None, 'Dennis', 'dennis@example.com', 'password123'))

    # Create todo table and add test todos
    todo_dao.create_table()
    print("Erstelle Test-Todos für Benutzer 'Dennis'.")
    todo_dao.add_item(TodoItem(None, 'Buy milk', False, 1))
    todo_dao.add_item(TodoItem(None, 'Buy eggs', False, 1))

    # Close connections
    todo_dao.close()
    user_dao.close()
    print("Testdaten wurden erfolgreich erstellt.")


if __name__ == '__main__':
    generate_testdata()
    app.run(debug=True)
