from typing import List

import strawberry


@strawberry.type
class Account:
    id: strawberry.ID
    user_id: strawberry.ID
    name: str


@strawberry.type
class User:
    id: strawberry.ID
    name: str

    @strawberry.field
    def accounts(self) -> List[Account]:
        from .db import get_accounts
        return get_accounts(self.id)
