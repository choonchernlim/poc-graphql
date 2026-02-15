from typing import List
import strawberry
from strawberry.types import Info

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
    async def accounts(self, info: Info) -> List[Account]:
        return await info.context["accounts_loader"].load(self.id)

    @strawberry.field
    def accounts_n_plus_one_problem(self) -> List[Account]:
        from .db import get_accounts
        return get_accounts(self.id)
