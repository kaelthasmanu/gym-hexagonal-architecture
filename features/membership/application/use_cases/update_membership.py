from typing import Any, Dict, Union
from uuid import UUID
from features.membership.application.dtos.membership_dtos import MembershipResponseDTO, MembershipUpdateDTO
from features.membership.application.errors.membership_errors import (
    MembershipNotFoundError,
    UnauthorizedMembershipAccessError,
    MembershipAlreadyExistsError,
    DailyMembershipExistsError,
    InvalidMembershipDataError
)
from features.membership.application.use_cases.base_use_case import BaseUseCase
from features.membership.domain.entities.membership import Membership
from features.membership.domain.membership_aggregate import MembershipAggregate
from features.membership.domain.object_values.membership_id import MembershipId
from features.membership.domain.object_values.update_membership_input import \
    UpdateMembershipInput

class UpdateMembershipUseCase(BaseUseCase[MembershipResponseDTO]):

    def __init__(self, membership_aggregate: MembershipAggregate, current_user: Dict[str, Any]):
        self.membership_aggregate = membership_aggregate
        self.current_user = current_user

    async def execute(self, membership_id: Union[str, UUID], update_data: MembershipUpdateDTO) -> MembershipResponseDTO:
        membership_uuid = membership_id if isinstance(
            membership_id,
            UUID) else UUID(
            membership_id)
        existing_membership = await self.membership_aggregate.get_membership(MembershipId(membership_uuid))
        try:

            if not existing_membership:
                raise MembershipNotFoundError(membership_uuid)

            self._check_authorization(existing_membership)


            update_membership_input = UpdateMembershipInput(
               name=update_data.name,
               description=update_data.description,
               price=update_data.price,
               duration=update_data.duration_days,
               type=update_data.type,
               status=update_data.status,
            )
            updated_membership = await self.membership_aggregate.update_membership(
                MembershipId(membership_uuid),
                update_membership_input
            )

            if not updated_membership:
                raise MembershipNotFoundError(membership_uuid)

            return self._to_response_dto(self, updated_membership)

        except ValueError as e:
            error_message = str(e).lower()
            if "already exists" in error_message:
                if "daily" in error_message:
                    raise DailyMembershipExistsError(UUID(self.current_user["id_gym"])) from e
                else:
                    raise MembershipAlreadyExistsError(
                        update_data.name if update_data.name else existing_membership.name,
                        UUID(self.current_user["id_gym"])
                    ) from e
            raise InvalidMembershipDataError("update_data", str(e)) from e

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