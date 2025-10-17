import \
    uuid
from typing import Optional
from uuid import UUID

from features.membership.domain.object_values.membership_id import \
    MembershipId


class MembershipError(Exception):
    status_code: int = 400
    detail: str = "An error occurred with the membership operation"
    def __init__(self, detail: Optional[str] = None, status_code: Optional[int] = None):
        if detail is not None:
            self.detail = detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.detail)

class MembershipNotFoundError(MembershipError):
    status_code = 404
    def __init__(self, membership_id: uuid.UUID):
        self.detail = f"Membership with ID {membership_id} not found"
        super().__init__(self.detail, self.status_code)

class MembershipAlreadyExistsError(MembershipError):
    status_code = 409
    def __init__(self, name: str, gym_id: UUID):
        self.detail = f"A membership with the name '{name}' already exists in gym {gym_id}"
        super().__init__(self.detail, self.status_code)

class DailyMembershipExistsError(MembershipError):
    status_code = 409
    def __init__(self, gym_id: UUID):
        self.detail = f"A daily membership already exists for gym {gym_id}"
        super().__init__(self.detail, self.status_code)

class MembershipInUseError(MembershipError):
    status_code = 409
    def __init__(self, membership_id: uuid.UUID):
        self.detail = (
            f"Membership with ID {membership_id} cannot be deleted because it is in use by active clients. "
            "Wait for all memberships to expire or cancel them first."
        )
        super().__init__(self.detail, self.status_code)

class InvalidMembershipDataError(MembershipError):
    status_code = 400
    def __init__(self, field: str, message: str):
        self.detail = f"Invalid membership data for field '{field}': {message}"
        super().__init__(self.detail, self.status_code)

class UnauthorizedMembershipAccessError(MembershipError):
    status_code = 403
    def __init__(self, membership_id: MembershipId, user_id: uuid.UUID):
        self.detail = f"User {user_id} is not authorized to access membership {membership_id}"
        super().__init__(self.detail, self.status_code)