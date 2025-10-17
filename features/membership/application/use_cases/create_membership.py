from typing import Any, Dict
from uuid import UUID
from features.membership.application.dtos.membership_dtos import MembershipCreateDTO, MembershipResponseDTO
from features.membership.application.errors.membership_errors import (
    MembershipAlreadyExistsError,
    DailyMembershipExistsError,
    InvalidMembershipDataError
)
from features.membership.application.use_cases.base_use_case import BaseUseCase
from features.membership.domain.entities.membership import Membership
from features.membership.domain.enums.membership_enums import \
    MembershipType
from features.membership.domain.membership_aggregate import MembershipAggregate
from features.membership.domain.object_values.create_membership_input import \
    CreateMembershipInput


class CreateMembershipUseCase(BaseUseCase[MembershipResponseDTO]):

    def __init__(self, membership_aggregate: MembershipAggregate, current_user: Dict[str, Any]):
        self.membership_aggregate = membership_aggregate
        self.current_user = current_user

    async def execute(self, membership_data: MembershipCreateDTO) -> MembershipResponseDTO:
        gym_id = UUID(self.current_user["id_gym"])
        try:
            from features.membership.domain.enums.membership_enums import MembershipStatus
            status = getattr(membership_data, 'status', MembershipStatus.ACTIVE)
            type_membership = getattr(membership_data, 'type', MembershipType.DAILY)

            membership_input = CreateMembershipInput(
                name=membership_data.name,
                description=membership_data.description,
                price=membership_data.price,
                duration=membership_data.duration_days,
                type=type_membership,
                gym_id=gym_id,
                status=status
            )
            membership = await self.membership_aggregate.create_membership(membership_input)
            return self._to_response_dto(membership)
        except ValueError as e:
            error_message = str(e).lower()
            if "already exists" in error_message:
                if "daily" in error_message:
                    raise DailyMembershipExistsError(gym_id) from e
                else:
                    raise MembershipAlreadyExistsError(membership_data.name, gym_id) from e
            raise InvalidMembershipDataError("membership_data", str(e)) from e

    @staticmethod
    def _to_response_dto(
            membership: Membership) -> MembershipResponseDTO:
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