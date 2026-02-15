# [POC] GraphQL

The project demonstrates GraphQL's N+1 query problem and how it is solved using the **DataLoader** pattern.

## Getting Started

- Follow the [instruction](backend/README.md) to run the backend.

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