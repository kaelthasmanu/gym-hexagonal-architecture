from typing import Any, Dict
from features.membership.application.dtos.membership_dtos import MembershipResponseDTO
from features.membership.application.errors.membership_errors import MembershipNotFoundError
from features.membership.application.use_cases.base_use_case import BaseUseCase
from features.membership.application.use_cases.get_membership import GetMembershipUseCase
from features.membership.domain.entities.membership import Membership
from features.membership.domain.membership_aggregate import MembershipAggregate

class GetDailyMembershipUseCase(BaseUseCase[MembershipResponseDTO]):

    def __init__(self, membership_aggregate: MembershipAggregate, current_user: Dict[str, Any]):
        self.membership_aggregate = membership_aggregate
        self.current_user = current_user
        self.get_membership_use_case = GetMembershipUseCase(membership_aggregate, current_user)

    async def execute(self) -> MembershipResponseDTO:

        from uuid import UUID
        gym_id = UUID(self.current_user["id_gym"])

        daily_membership = await self.membership_aggregate.get_daily_membership_for_gym(gym_id)

        if not daily_membership:
            raise MembershipNotFoundError("No daily membership found for this gym")

        return self._to_response_dto(self,daily_membership)

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