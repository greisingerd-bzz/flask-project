"""Blueprint for user authentication."""
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required
from user_dao import UserDao
from user import User

user_blueprint = Blueprint('user_blueprint', __name__)
user_dao = UserDao('todo_example.db')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Handle registration."""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        print("Registrierungsversuch:", username)

        user_dao.add_user(User(None, username, None, password))
        return redirect(url_for('user_blueprint.login'))

    return render_template('register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login."""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        print("Login-Versuch für Benutzer:", username)

        user = user_dao.get_user_by_username(username)

        if user:
            print("Benutzer gefunden:", user.username)

        if user and user.password == password:
            login_user(user)
            print("Login erfolgreich.")
            return jsonify({"success": True}), 200
        else:
            print("Login fehlgeschlagen: Falsches Passwort oder Benutzername.")
            return jsonify({"error": "Unauthorized"}), 401

    return render_template('login.html')


@user_blueprint.route('/logout')
@login_required
def logout():
    """Handle logout."""
    logout_user()
    return redirect(url_for('user_blueprint.login'))
