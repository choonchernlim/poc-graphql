from typing import List, Optional
import strawberry
from .types import User
import logging

# Sample data
users_db = [
    User(id=strawberry.ID("1"), name="Alice"),
    User(id=strawberry.ID("2"), name="Bob"),
    User(id=strawberry.ID("3"), name="Charlie"),
]


def get_users() -> List[User]:
    logging.info("Fetching all users...")
    return users_db


def get_user(user_id: strawberry.ID) -> Optional[User]:
    logging.info(f"Fetching user [id: {user_id}]...")
    return next((user for user in users_db if user.id == user_id), None)
