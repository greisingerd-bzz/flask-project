from flask import Blueprint, request, jsonify, render_template, g
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from user_dao import UserDao
from user import User

user_blueprint = Blueprint('user_blueprint', __name__)


def get_user_dao():
    if 'user_dao' not in g:
        g.user_dao = UserDao('todo_example.db')
    return g.user_dao


@user_blueprint.teardown_app_request
def close_connection(exception):
    user_dao = g.pop('user_dao', None)
    if user_dao is not None:
        user_dao.close()


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    user_dao = get_user_dao()
    if user_dao.get_user_by_email(email):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(None, name, email, hashed_password)
    user_dao.add_user(new_user)
    return jsonify({"message": "User successfully registered"}), 201


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_dao = get_user_dao()
    user = user_dao.get_user_by_email(email)

    if not user:
        print(f"User with email {email} not found.")
        return jsonify({"error": "Invalid credentials"}), 401

    print(f"User found: {user.email}")
    print(f"Entered password: {password}")

    if not check_password_hash(user.password, password):
        print(f"Stored hashed password: {user.password}")
        print("Invalid password.")
        return jsonify({"error": "Invalid credentials"}), 401

    login_user(user)
    return jsonify({"message": "Successfully logged in"}), 200


@user_blueprint.route('/register_new', methods=['POST'])
def register_new_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request did not contain JSON data"}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Validation der Eingabedaten
    if not all([name, email, password]):
        return jsonify({"error": "Name, Email und Passwort sind erforderlich"}), 400

    user_dao = UserDao('todo_example.db')
    existing_user = user_dao.get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "Ein Benutzer mit dieser E-Mail existiert bereits"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(None, name, email, hashed_password)
    user_dao.add_user(new_user)
    return jsonify({"message": "Registrierung erfolgreich"}), 201


@user_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Successfully logged out"}), 200
