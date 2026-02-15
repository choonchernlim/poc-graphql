# Backend

The project demonstrates GraphQL's N+1 query problem and how it is solved using the **DataLoader** pattern.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

## Getting Started

- Install dependencies:
```bash
uv sync
```

## Interactive

- Run the server:
```bash
uv run uvicorn main:app --reload
```

- Visit http://127.0.0.1:8000/graphql

- `BadQuery` demonstrates the N+1 problem, where fetching accounts for each user results in multiple queries.
```graphql
query BadQuery {
    users {
        name
        accountsNPlusOneProblem {
            name
        }
    }
}
```

- `GoodQuery` demonstrates the solution using DataLoader, where accounts for all users are fetched in a single batch query.
```graphql
query GoodQuery {
    users {
        name
        accounts {
            name
        }
    }
}
```

## Testcases

- Run tests:
```bash
uv run pytest -v -s tests
```
