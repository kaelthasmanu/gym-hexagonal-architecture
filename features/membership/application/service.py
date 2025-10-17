import \
    uuid
from typing import Any, Dict, Optional
from features.membership.application.dtos.membership_dtos import (
    MembershipCreateDTO,
    MembershipResponseDTO,
    MembershipUpdateDTO,
    MembershipListResponseDTO
)
from features.membership.application.use_cases.create_membership import CreateMembershipUseCase
from features.membership.application.use_cases.delete_membership import DeleteMembershipUseCase
from features.membership.application.use_cases.get_daily_membership import GetDailyMembershipUseCase
from features.membership.application.use_cases.get_membership import GetMembershipUseCase
from features.membership.application.use_cases.get_memberships import GetMembershipsUseCase
from features.membership.application.use_cases.update_membership import UpdateMembershipUseCase
from features.membership.domain.membership_aggregate import MembershipAggregate

class MembershipService:
    def __init__(self, membership_aggregate: MembershipAggregate, current_user: Dict[str, Any]):
        self.membership_aggregate = membership_aggregate
        self.current_user = current_user

    async def create_membership(self, membership_data: MembershipCreateDTO) -> MembershipResponseDTO:

        use_case = CreateMembershipUseCase(self.membership_aggregate, self.current_user)

        return await use_case.execute(membership_data)

    async def get_membership(self, membership_id: uuid.UUID) -> MembershipResponseDTO:

        use_case = GetMembershipUseCase(self.membership_aggregate, self.current_user)

        return await use_case.execute(membership_id)

    async def get_daily_membership(self) -> MembershipResponseDTO:

        use_case = GetDailyMembershipUseCase(self.membership_aggregate, self.current_user)

        return await use_case.execute()

    async def list_memberships(
        self,
        page: int = 1,
        size: int = 10,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> MembershipListResponseDTO:

        use_case = GetMembershipsUseCase(self.membership_aggregate, self.current_user)

        return await use_case.execute(page=page, size=size, status=status, search=search)

    async def update_membership(
        self,
        membership_id: uuid.UUID,
        update_data: MembershipUpdateDTO
    ) -> MembershipResponseDTO:

        use_case = UpdateMembershipUseCase(self.membership_aggregate, self.current_user)

        return await use_case.execute(membership_id, update_data)

    async def delete_membership(self, membership_id: uuid.UUID) -> bool:

        use_case = DeleteMembershipUseCase(self.membership_aggregate, self.current_user)

        return await use_case.execute(membership_id)