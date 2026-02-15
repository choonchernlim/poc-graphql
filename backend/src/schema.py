from typing import List, Optional

import strawberry

from .db import get_users, get_user
from .types import User


@strawberry.type
class Query:
    users: List[User] = strawberry.field(resolver=get_users)
    user: Optional[User] = strawberry.field(resolver=get_user)
