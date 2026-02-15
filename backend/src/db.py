import logging
import sqlite3
from typing import List, Optional

import strawberry
from strawberry.dataloader import DataLoader

from .types import User, Account

DATABASE_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
        conn.commit()
    
    conn.close()

# Initialize DB on module import
init_db()

def get_users() -> List[User]:
    logging.info("Fetching all users from DB...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM user")
    rows = cursor.fetchall()
    conn.close()
    return [User(id=strawberry.ID(row["id"]), name=row["name"]) for row in rows]


def get_user(user_id: strawberry.ID) -> Optional[User]:
    logging.info(f"Fetching user [id: {user_id}] from DB...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM user WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return User(id=strawberry.ID(row["id"]), name=row["name"])
    return None


def get_accounts(user_id: strawberry.ID) -> List[Account]:
    logging.info(f"Fetching accounts for user [id: {user_id}] from DB...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, name FROM account WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        Account(
            id=strawberry.ID(row["id"]), 
            user_id=strawberry.ID(row["user_id"]), 
            name=row["name"]
        ) for row in rows
    ]


async def load_accounts(user_ids: List[strawberry.ID]) -> List[List[Account]]:
    logging.info(f"Batch fetching accounts for user ids: {user_ids}")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    placeholders = ",".join("?" for _ in user_ids)
    query = f"SELECT id, user_id, name FROM account WHERE user_id IN ({placeholders})"
    
    # Execute with the actual IDs
    # Note: user_ids are strawberry.ID which are strings, so this is safe for sqlite text columns
    cursor.execute(query, user_ids)
    rows = cursor.fetchall()
    conn.close()

    # Group accounts by user_id
    accounts_by_user = {}
    for row in rows:
        uid = row["user_id"]
        if uid not in accounts_by_user:
            accounts_by_user[uid] = []
        accounts_by_user[uid].append(
            Account(
                id=strawberry.ID(row["id"]),
                user_id=strawberry.ID(row["user_id"]),
                name=row["name"]
            )
        )

    # Return in order of requested user_ids
    return [accounts_by_user.get(str(uid), []) for uid in user_ids]

def get_accounts_loader() -> DataLoader:
    return DataLoader(load_fn=load_accounts)
