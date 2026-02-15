import pytest
from src.schema import schema
from main import get_context

@pytest.mark.asyncio
async def test_dataloader_gql():
    query = """
        query TestDataLoader {
            users {
                name
                accounts {
                    name
                }
            }
        }
    """

    print("\n--- Testing Optimized (DataLoader) via GraphQL ---")
    print("Observe the logs: You should see a SINGLE 'Batch fetching...' and ONE 'SQL EXECUTE' log for ALL users.")

    context = await get_context()
    result = await schema.execute(query, context_value=context)

    assert result.errors is None
    assert result.data is not None
    
    users_data = result.data["users"]
    expected_counts = {"Alice": 2, "Bob": 1, "Charlie": 0}

    for user_data in users_data:
        name = user_data["name"]
        accounts = user_data["accounts"]
        count = len(accounts)
        print(f"User {name} has {count} accounts")
        assert count == expected_counts[name]
