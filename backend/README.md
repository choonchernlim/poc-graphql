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

## Schema

The GraphQL schema includes a `User` type:

```graphql
type User {
  id: ID!
  name: String!
}

type Query {
  users: [User!]!
}
```
