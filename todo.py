class TodoItem:
    _id_counter = 1

    def __init__(self, title, is_completed=False):
        self.id = TodoItem._id_counter
        TodoItem._id_counter += 1
        self.title = title
        self.is_completed = is_completed

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'is_completed': self.is_completed}

# Initial todo list
todos = [
    TodoItem("Buy milk"),
    TodoItem("Read book", True),
    TodoItem("Write code"),
]

# Basic CRUD operations
def add_todo(todo):
    todos.append(todo)

def get_todo(todo_id):
    return next((todo for todo in todos if todo.id == todo_id), None)

def update_todo(todo_id, title=None, is_completed=None):
    todo = get_todo(todo_id)
    if todo:
        if title is not None:
            todo.title = title
        if is_completed is not None:
            todo.is_completed = is_completed
    return todo

def delete_todo(todo_id):
    global todos
    todos = list(filter(lambda x: x.id != todo_id, todos))
    return True
