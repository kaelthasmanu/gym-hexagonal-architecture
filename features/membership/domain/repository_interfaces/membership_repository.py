from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from features.membership.domain.entities.membership import Membership
from features.membership.domain.object_values.membership_id import MembershipId

class IMembershipRepository(ABC):

    @abstractmethod
    async def create(self, membership: Membership) -> Membership:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, membership_id: MembershipId) -> Optional[Membership]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_gym_id(
        self, 
        gym_id: UUID,
        page: int = 1,
        size: int = 10,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[Membership], int]:
        raise NotImplementedError

    @abstractmethod
    async def get_daily_membership(self, gym_id: UUID) -> Optional[Membership]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, membership: Membership) -> Optional[Membership]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, membership_id: MembershipId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def exists_with_name(self, name: str, gym_id: UUID, exclude_id: Optional[MembershipId] = None) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def is_used_by_active_clients(self, membership_id: MembershipId) -> bool:
        raise NotImplementedError