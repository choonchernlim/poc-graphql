import pytest
from src.schema import schema
from main import get_context


@pytest.mark.asyncio
async def test_n_plus_one_gql():
    query = """
        query BadQuery {
            users {
                name
                accountsNPlusOneProblem {
                    name
                }
            }
        }
    """

    print("\n--- Testing N+1 via GraphQL ---")
    print("Observe the logs: You should see a separate 'SQL EXECUTE' log for EACH user's accounts.")

    context = await get_context()
    result = await schema.execute(query, context_value=context)

    assert result.errors is None
    assert result.data is not None

    users_data = result.data["users"]
    expected_counts = {
        "Alice": 2,
        "Bob": 1,
        "Charlie": 0,
        "Tom": 0,
        "Josh": 0,
        "Brady": 0,
        "John": 0,
        "Mike": 0,
        "Mary": 0,
        "Jane": 0,
    }

    for user_data in users_data:
        name = user_data["name"]
        accounts = user_data["accountsNPlusOneProblem"]
        count = len(accounts)
        print(f"User {name} has {count} accounts")
        assert count == expected_counts[name]
