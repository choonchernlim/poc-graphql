[![Backend Tests](https://github.com/choonchernlim/poc-graphql/actions/workflows/backend-test.yml/badge.svg?branch=main)](https://github.com/choonchernlim/poc-graphql/actions/workflows/backend-test.yml)

# Backend

The backend is built using FastAPI and Strawberry GraphQL. It simulates a simple user-account relationship to
demonstrate the N+1 query problem and its solution using the Data Loader pattern.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

## Getting Started

- Install dependencies:

```bash
uv sync
```

### Interactive

- Run the server:

```bash
uv run uvicorn main:app --reload
```

- Visit http://127.0.0.1:8000/graphql

### Testcases

- Run tests:

```bash
uv run pytest -v -s tests
```
