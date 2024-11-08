from flask import Blueprint, jsonify, g, render_template, request
from flask_login import login_required, current_user
from todo_dao import TodoDao
from todo_item import TodoItem

todo_blueprint = Blueprint('todo_blueprint', __name__)


def get_todo_dao():
    if 'todo_dao' not in g:
        g.todo_dao = TodoDao('todo_example.db')
    return g.todo_dao


@todo_blueprint.teardown_app_request
def close_connection(exception):
    todo_dao = g.pop('todo_dao', None)
    if todo_dao is not None:
        todo_dao.close()


@todo_blueprint.route('/todos', methods=['GET'])
@login_required
def get_todos():
    todo_dao = get_todo_dao()
    todos = todo_dao.get_items_by_user_id(current_user.id)
    if request.accept_mimetypes.best == 'application/json':
        return jsonify([todo.__dict__ for todo in todos])
    else:
        return render_template('index.html', todos=todos)


@todo_blueprint.route('/todos', methods=['POST'])
@login_required
def add_todo():
    data = request.get_json()

    if not data or 'description' not in data:
        return jsonify({"error": "Beschreibung wird benötigt"}), 400

    description = data.get('description')

    todo_dao = get_todo_dao()
    todo_item = TodoItem(id=None, description=description, completed=False, user_id=current_user.id)
    todo_dao.add_item(todo_item)

    return jsonify({"message": "Todo erfolgreich hinzugefügt"}), 201

@todo_blueprint.route('/todos/<int:todo_id>', methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    todo_dao = get_todo_dao()
    todo_dao.delete_item(todo_id)
    return jsonify({"message": "Todo erfolgreich gelöscht"}), 204
