"""This module defines the TodoItem dataclass representing a todo item."""

from dataclasses import dataclass

@dataclass
class TodoItem:
    item_id: int
    user_id: int
    title: str
    is_completed: bool
