from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from todo_dao import TodoDao
from todo_item import TodoItem

todo_blueprint = Blueprint('todo_blueprint', __name__)
todo_dao = TodoDao('todo_example.db')

@todo_blueprint.route('/todos', methods=['GET'])
@login_required
def get_all_todos():
    items = todo_dao.get_all_items(current_user.id)
    return jsonify([item.__dict__ for item in items]), 200

@todo_blueprint.route('/todos', methods=['POST'])
@login_required
def add_todo():
    data = request.get_json()
    new_item = TodoItem(None, current_user.id, data['title'], data['is_completed'])
    todo_dao.add_item(new_item)
    return jsonify({'message': 'Todo item created'}), 201
