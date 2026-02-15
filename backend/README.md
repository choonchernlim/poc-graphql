# Backend

This is a simple GraphQL API built with [FastAPI](https://fastapi.tiangolo.com/) and [Strawberry](https://strawberry.rocks/), managed by [uv](https://github.com/astral-sh/uv).

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

## Setup & Running

1. **Install dependencies:**

```bash
uv sync
```

2. **Run the server:**

```bash
uv run uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql).

## Testing & N+1 Problem Demonstration

The project includes tests to demonstrate the N+1 query problem and how it is solved using the **DataLoader** pattern.

To see the difference in database access patterns, run the tests with the `-v` (verbose) and `-s` (show stdout/logs) flags:

```bash
uv run pytest -v -s tests
```

### Testcases:

- **`test_n_plus_one_problem.py`**: You will see multiple `SQL EXECUTE` logs (one for each user) as the application fetches accounts sequentially.
- **`test_dataloader.py`**: You will see a single `Batch fetching...` log followed by one optimized `SQL EXECUTE` query using `IN (?,?,?)`, demonstrating that all accounts were retrieved in a single trip to the database.

## Schema

The GraphQL schema includes `User` and `Account` types:

```graphql
type Account {
  id: ID!
  userId: ID!
  name: String!
}

type User {
  id: ID!
  name: String!
  accounts: [Account!]!
}

type Query {
  users: [User!]!
  user(id: ID!): User
}
```
