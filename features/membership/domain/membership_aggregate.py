from typing import \
    Optional
from uuid import \
    UUID

from features.membership.domain.entities.membership import \
    Membership
from features.membership.domain.enums.membership_enums import \
    MembershipStatus
from features.membership.domain.object_values.create_membership_input import \
    CreateMembershipInput
from features.membership.domain.object_values.membership_duration import \
    MembershipDuration
from features.membership.domain.object_values.membership_id import \
    MembershipId
from features.membership.domain.object_values.membership_price import \
    MembershipPrice
from features.membership.domain.object_values.update_membership_input import \
    UpdateMembershipInput
from features.membership.domain.repository_interfaces.membership_repository import \
    IMembershipRepository


class MembershipAggregate:
    def __init__(
            self,
            repository: IMembershipRepository):
        self._repository = repository

    async def create_membership(
            self,
            membership_input: CreateMembershipInput
    ) -> Membership:
        if await self._repository.exists_with_name(
                membership_input.name,
                membership_input.gym_id):
            raise ValueError(
                f"A membership with the name '{membership_input.name}' already exists in this gym.")

        duration = MembershipDuration.from_int(
            membership_input.duration)

        if duration.is_daily() and await self._repository.get_daily_membership(
                membership_input.gym_id):
            raise ValueError(
                "A daily membership already exists for this gym.")

        membership = Membership(
            id=MembershipId.generate(),
            name=membership_input.name,
            description=membership_input.description,
            price=MembershipPrice.from_float(
                membership_input.price),
            duration=duration,
            status=membership_input.status,
            gym_id=membership_input.gym_id,
            type=membership_input.type
        )

        return await self._repository.create(
            membership)

    async def update_membership(
            self,
            membership_id: MembershipId,
            update_membership_input: UpdateMembershipInput
    ) -> \
    Optional[
        Membership]:
        membership = await self._repository.get_by_id(
            membership_id)
        if not membership:
            return None

        print(update_membership_input, "update_membership_input")

        if update_membership_input.name is not None and update_membership_input.name != membership.name:
            if await self._repository.exists_with_name(
                    update_membership_input.name,
                    membership.gym_id,
                    exclude_id=membership_id):
                raise ValueError(
                    f"A membership with the name '{update_membership_input.name}' already exists in this gym.")

        if update_membership_input.duration is not None and update_membership_input.duration == 1 and not membership.is_daily():
            if await self._repository.get_daily_membership(
                    membership.gym_id):
                raise ValueError(
                    "A daily membership already exists for this gym.")

        if update_membership_input.name is not None:
            membership.name = update_membership_input.name
        if update_membership_input.description is not None:
            membership.description = update_membership_input.description
        if update_membership_input.price is not None:
            membership.price = MembershipPrice.from_float(
                update_membership_input.price)
        if update_membership_input.duration is not None:
            membership.duration = MembershipDuration.from_int(
                update_membership_input.duration)
        if update_membership_input.type is not None:
            membership.type = update_membership_input.type
        if update_membership_input.status is not None:
            membership.status = update_membership_input.status

        return await self._repository.update(
            membership)

    async def delete_membership(
            self,
            membership_id: MembershipId) -> bool:
        membership = await self._repository.get_by_id(
            membership_id)
        if not membership:
            return False

        if await self._repository.is_used_by_active_clients(
                membership_id):
            raise ValueError(
                "Cannot delete membership: it is being used by active clients.")

        return await self._repository.delete(
            membership_id)

    async def get_membership(
            self,
            membership_id: MembershipId) -> \
    Optional[
        Membership]:
        return await self._repository.get_by_id(
            membership_id)

    async def list_memberships(
            self,
            gym_id: UUID,
            page: int = 1,
            size: int = 10,
            status:
            Optional[
                MembershipStatus] = None,
            search:
            Optional[
                str] = None
    ) -> tuple[list[ Membership], int]:
        return await self._repository.get_by_gym_id(
            gym_id,
            page,
            size,
            status,
            search)

    async def get_daily_membership_for_gym(
            self,
            gym_id: UUID) ->Optional[Membership]:
        return await self._repository.get_daily_membership(
            gym_id)
