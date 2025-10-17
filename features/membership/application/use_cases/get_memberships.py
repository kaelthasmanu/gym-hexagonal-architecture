from typing import Any, Dict, Optional
from uuid import UUID
from features.membership.application.dtos.membership_dtos import MembershipListResponseDTO, MembershipResponseDTO
from features.membership.application.use_cases.base_use_case import BaseUseCase
from features.membership.domain.entities.membership import Membership
from features.membership.domain.membership_aggregate import MembershipAggregate

class GetMembershipsUseCase(BaseUseCase[MembershipListResponseDTO]):

    def __init__(self, membership_aggregate: MembershipAggregate, current_user: Dict[str, Any]):
        self.membership_aggregate = membership_aggregate
        self.current_user = current_user

    async def execute(
        self,
        page: int = 1,
        size: int = 10,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> MembershipListResponseDTO:

        gym_id = UUID(self.current_user["id_gym"])

        memberships, total = await self.membership_aggregate.list_memberships(
            gym_id, page, size, status, search
        )

        total_pages = (total + size - 1) // size if size > 0 else 1

        items = [self._to_response_dto(self, membership) for membership in memberships]

        return MembershipListResponseDTO(
            items=items,
            total=total,
            page=page,
            size=size,
            total_pages=total_pages
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