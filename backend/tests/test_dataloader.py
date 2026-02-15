import asyncio

import pytest

from src.db import get_users, get_accounts_loader


# Mock context
class MockInfo:
    def __init__(self, loader):
        self.context = {"accounts_loader": loader}


@pytest.mark.asyncio
async def test_dataloader():
    print("Fetching users...")
    users = get_users()
    loader = get_accounts_loader()
    info = MockInfo(loader)

    print("\n--- Testing Optimized (DataLoader) ---")
    print("Observe the logs: You should see a SINGLE 'Batch fetching...' log for ALL users.")

    # We gather all the coroutines to run them concurrently, which allows the DataLoader to batch them
    tasks = [u.accounts(info) for u in users]
    results = await asyncio.gather(*tasks)

    expected_counts = {"Alice": 2, "Bob": 1, "Charlie": 0}

    for i, u in enumerate(users):
        count = len(results[i])
        print(f"User {u.name} has {count} accounts")
        assert count == expected_counts[u.name]
