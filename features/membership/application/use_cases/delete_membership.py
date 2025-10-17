from typing import Any, Dict, Union
from uuid import UUID
from features.membership.application.errors.membership_errors import (
    MembershipNotFoundError,
    MembershipInUseError,
    UnauthorizedMembershipAccessError
)
from features.membership.application.use_cases.base_use_case import BaseUseCase
from features.membership.domain.entities.membership import Membership
from features.membership.domain.membership_aggregate import MembershipAggregate
from features.membership.domain.object_values.membership_id import MembershipId

class DeleteMembershipUseCase(BaseUseCase[bool]):

    def __init__(self, membership_aggregate: MembershipAggregate, current_user: Dict[str, Any]):
        self.membership_aggregate = membership_aggregate
        self.current_user = current_user

    async def execute(self, membership_id: Union[str, UUID]) -> bool:
        membership_uuid = membership_id if isinstance(membership_id, UUID) else UUID(membership_id)
        try:

            existing_membership = await self.membership_aggregate.get_membership(MembershipId(membership_uuid))

            if not existing_membership:
                raise MembershipNotFoundError(membership_uuid)

            self._check_authorization(existing_membership)

            is_in_use = await self.membership_aggregate._repository.is_used_by_active_clients(
                MembershipId(membership_uuid)
            )
            
            if is_in_use:
                raise MembershipInUseError(membership_uuid)

            deleted = await self.membership_aggregate.delete_membership(MembershipId(membership_uuid))

            if not deleted:
                raise MembershipNotFoundError(membership_uuid)
            return True

        except ValueError as e:
            error_message = str(e).lower()
            if "in use" in error_message:
                raise MembershipInUseError(membership_uuid) from e
            raise MembershipNotFoundError(membership_uuid) from e

    def _check_authorization(self, membership: Membership) -> None:

        user_gym_id = UUID(self.current_user["id_gym"])

        if membership.gym_id != user_gym_id:
            raise UnauthorizedMembershipAccessError(
                membership_id=membership.id,
                user_id=self.current_user["id"]
            )