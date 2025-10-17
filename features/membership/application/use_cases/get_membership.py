from typing import Any, Dict, Union
from uuid import UUID
from features.membership.application.dtos.membership_dtos import MembershipResponseDTO
from features.membership.application.errors.membership_errors import (
    MembershipNotFoundError,
    UnauthorizedMembershipAccessError
)
from features.membership.application.use_cases.base_use_case import BaseUseCase
from features.membership.domain.entities.membership import Membership
from features.membership.domain.membership_aggregate import MembershipAggregate
from features.membership.domain.object_values.membership_id import MembershipId

class GetMembershipUseCase(BaseUseCase[MembershipResponseDTO]):

    def __init__(self, membership_aggregate: MembershipAggregate, current_user: Dict[str, Any]):
        self.membership_aggregate = membership_aggregate
        self.current_user = current_user

    async def execute(self, membership_id: Union[str, UUID]) -> MembershipResponseDTO:
        membership_uuid = membership_id if isinstance(membership_id, UUID) else UUID(membership_id)
        try:


            membership = await self.membership_aggregate.get_membership(MembershipId(membership_uuid))

            if not membership:
                raise MembershipNotFoundError(membership_uuid)

            self._check_authorization(membership)

            return self._to_response_dto(self, membership)

        except ValueError as e:
            raise MembershipNotFoundError(membership_uuid) from e

    def _check_authorization(self, membership: Membership) -> None:
        user_gym_id = UUID(self.current_user["id_gym"])
        if membership.gym_id != user_gym_id:
            raise UnauthorizedMembershipAccessError(
                membership_id=membership.id,
                user_id=self.current_user["id"]
            )

    @staticmethod
    def _to_response_dto(_self, membership: Membership) -> MembershipResponseDTO:
        return MembershipResponseDTO(
            id=membership.id.value,
            name=membership.name,
            description=membership.description,
            price=membership.price.to_float(),
            duration_days=membership.duration.to_int(),
            status=membership.status,
            type=membership.type,
            created_at=membership.created_at,
            updated_at=membership.updated_at,
            gym_id=membership.gym_id
        )