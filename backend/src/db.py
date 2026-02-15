import logging
import sqlite3
from collections import defaultdict
from contextlib import contextmanager
from typing import List, Optional, Callable, Any

import strawberry
from strawberry.dataloader import DataLoader

from .types import User, Account

DATABASE_NAME = "database.db"

@contextmanager
def get_db_cursor():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        conn.close()

def execute_fetchall(query: str, params: tuple = (), mapper: Optional[Callable[[sqlite3.Row], Any]] = None) -> List[Any]:
    logging.info(f"SQL EXECUTE (fetchall): {query} with params {params}")
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
    return [mapper(row) for row in rows] if mapper else rows

def execute_fetchone(query: str, params: tuple = (), mapper: Optional[Callable[[sqlite3.Row], Any]] = None) -> Optional[Any]:
    logging.info(f"SQL EXECUTE (fetchone): {query} with params {params}")
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        row = cursor.fetchone()
    if row:
        return mapper(row) if mapper else row
    return None

def init_db():
    with get_db_cursor() as cursor:
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS account (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        """)
        
        # Check if data exists
        cursor.execute("SELECT count(*) FROM user")
        if cursor.fetchone()[0] == 0:
            logging.info("Initializing database with sample data...")
            users_data = [
                ("1", "Alice"),
                ("2", "Bob"),
                ("3", "Charlie"),
            ]
            cursor.executemany("INSERT INTO user (id, name) VALUES (?, ?)", users_data)
            
            accounts_data = [
                ("1", "1", "Alice's Checking"),
                ("2", "1", "Alice's Savings"),
                ("3", "2", "Bob's Checking"),
            ]
            cursor.executemany("INSERT INTO account (id, user_id, name) VALUES (?, ?, ?)", accounts_data)

# Initialize DB on module import
init_db()

def _row_to_user(row: sqlite3.Row) -> User:
    return User(id=strawberry.ID(row["id"]), name=row["name"])

def _row_to_account(row: sqlite3.Row) -> Account:
    return Account(
        id=strawberry.ID(row["id"]),
        user_id=strawberry.ID(row["user_id"]),
        name=row["name"]
    )

def get_users() -> List[User]:
    logging.info("Fetching all users from DB...")
    return execute_fetchall("SELECT id, name FROM user", mapper=_row_to_user)


def get_user(user_id: strawberry.ID) -> Optional[User]:
    logging.info(f"Fetching user [id: {user_id}] from DB...")
    return execute_fetchone("SELECT id, name FROM user WHERE id = ?", (user_id,), mapper=_row_to_user)


def get_accounts(user_id: strawberry.ID) -> List[Account]:
    logging.info(f"Fetching accounts for user [id: {user_id}] from DB...")
    return execute_fetchall("SELECT id, user_id, name FROM account WHERE user_id = ?", (user_id,), mapper=_row_to_account)


async def load_accounts(user_ids: List[strawberry.ID]) -> List[List[Account]]:
    logging.info(f"Batch fetching accounts for user ids: {user_ids}")
    placeholders = ",".join("?" for _ in user_ids)
    query = f"SELECT id, user_id, name FROM account WHERE user_id IN ({placeholders})"
    
    # We use execute_fetchall to get mapped Account objects directly
    accounts = execute_fetchall(query, tuple(user_ids), mapper=_row_to_account)

    accounts_by_user = defaultdict(list)
    for account in accounts:
        # Group by user_id
        accounts_by_user[str(account.user_id)].append(account)

    return [accounts_by_user.get(str(uid), []) for uid in user_ids]

def get_accounts_loader() -> DataLoader:
    return DataLoader(load_fn=load_accounts)
