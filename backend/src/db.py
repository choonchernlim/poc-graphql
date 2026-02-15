from typing import List, Optional
import strawberry
from .types import User, Account
import logging

# Sample data
users_db = [
    User(id=strawberry.ID("1"), name="Alice"),
    User(id=strawberry.ID("2"), name="Bob"),
    User(id=strawberry.ID("3"), name="Charlie"),
]

accounts_db = [
    Account(id=strawberry.ID("1"), user_id=strawberry.ID("1"), name="Alice's Checking"),
    Account(id=strawberry.ID("2"), user_id=strawberry.ID("1"), name="Alice's Savings"),
    Account(id=strawberry.ID("3"), user_id=strawberry.ID("2"), name="Bob's Checking"),
]


def get_users() -> List[User]:
    logging.info("Fetching all users...")
    return users_db

def get_user(user_id: strawberry.ID) -> Optional[User]:
    logging.info(f"Fetching user [id: {user_id}]...")
    return next((user for user in users_db if user.id == user_id), None)

def get_accounts(user_id: strawberry.ID) -> List[Account]:
    logging.info(f"Fetching accounts for user [id: {user_id}]...")
    return [account for account in accounts_db if account.user_id == user_id]
