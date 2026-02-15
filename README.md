# [POC] GraphQL

[![Backend Tests](https://github.com/choonchernlim/poc-graphql/actions/workflows/backend-test.yml/badge.svg)](https://github.com/choonchernlim/poc-graphql/actions/workflows/backend-test.yml)

The project demonstrates GraphQL's N+1 query problem and how it is solved using the **DataLoader** pattern.

- Follow the [instruction](backend/README.md) to run the backend.

## N+1 Query Problem

`BadQuery` demonstrates the N+1 problem, where fetching accounts for each user results in multiple queries.

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

Logs:
```text
INFO root Fetching all users from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, name FROM user with params ()
INFO root Fetching accounts for user [id: 1] from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id = ? with params ('1',)
INFO root Fetching accounts for user [id: 2] from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id = ? with params ('2',)
INFO root Fetching accounts for user [id: 3] from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id = ? with params ('3',)
INFO root Fetching accounts for user [id: 4] from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id = ? with params ('4',)
INFO root Fetching accounts for user [id: 5] from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id = ? with params ('5',)
INFO root Fetching accounts for user [id: 6] from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id = ? with params ('6',)
INFO root Fetching accounts for user [id: 7] from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id = ? with params ('7',)
INFO root Fetching accounts for user [id: 8] from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id = ? with params ('8',)
INFO root Fetching accounts for user [id: 9] from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id = ? with params ('9',)
INFO root Fetching accounts for user [id: 10] from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id = ? with params ('10',)
```

## Data Loader Pattern

`GoodQuery` demonstrates the solution using Data Loader, where accounts for all users are fetched in a single batch query.

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
Logs:
```text
INFO root Fetching all users from DB...
INFO root SQL EXECUTE (fetchall): SELECT id, name FROM user with params ()
INFO root Batch fetching accounts for user ids: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
INFO root SQL EXECUTE (fetchall): SELECT id, user_id, name FROM account WHERE user_id IN (?,?,?,?,?,?,?,?,?,?) with params ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
```
