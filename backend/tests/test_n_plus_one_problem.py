import pytest

from src.db import get_users


@pytest.mark.asyncio
async def test_n_plus_one():
    print("Fetching users...")
    users = get_users()

    print("\n--- Testing N+1 (Direct DB Call) ---")
    print("Observe the logs: You should see a separate 'Fetching accounts...' log for EACH user.")

    expected_counts = {"Alice": 2, "Bob": 1, "Charlie": 0}

    for u in users:
        # This calls get_accounts directly for each user
        accounts = u.accounts_n_plus_one_problem()
        count = len(accounts)
        print(f"User {u.name} has {count} accounts")
        assert count == expected_counts[u.name]
