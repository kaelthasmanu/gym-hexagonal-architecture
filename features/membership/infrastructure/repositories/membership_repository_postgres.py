from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from features.membership.domain.entities.membership import Membership
from features.membership.domain.object_values.membership_id import MembershipId
from features.membership.domain.repository_interfaces.membership_repository import IMembershipRepository
from features.membership.infrastructure.entities.membership_model import MembershipModel

class MembershipRepositoryPostgres(IMembershipRepository):

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, membership: Membership) -> Membership:
        membership_model = MembershipModel.from_domain(membership)
        self.session.add(membership_model)
        await self.session.commit()
        await self.session.refresh(membership_model)
        print(membership_model, "membership_model")
        return membership_model.to_domain()
    
    async def get_by_id(self, membership_id: MembershipId) -> Optional[Membership]:
        result = await self.session.execute(
            select(MembershipModel).where(MembershipModel.id == membership_id.value)
        )
        membership_model = result.scalar_one_or_none()
        return membership_model.to_domain() if membership_model else None
    
    async def get_by_gym_id(
        self, 
        gym_id: UUID,
        page: int = 1,
        size: int = 10,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[Membership], int]:
        query = select(MembershipModel).where(MembershipModel.gym_id == gym_id)
        
        from features.membership.domain.enums.membership_enums import MembershipStatus
        status_enum = None
        if status:
            status_enum = MembershipStatus.ACTIVE if status.lower() == "active" else MembershipStatus.INACTIVE
            query = query.where(MembershipModel.status == status_enum)
        
        if search:
            query = query.where(
                or_(
                    MembershipModel.name.ilike(f"%{search}%"),
                    MembershipModel.description.ilike(f"%{search}%")
                )
            )
        
        count_query = select(MembershipModel).where(MembershipModel.gym_id == gym_id)
        if status:
            count_query = count_query.where(MembershipModel.status == status_enum)
        if search:
            count_query = count_query.where(
                or_(
                    MembershipModel.name.ilike(f"%{search}%"),
                    MembershipModel.description.ilike(f"%{search}%")
                )
            )
        count_result = await self.session.execute(count_query)
        total = len(count_result.scalars().all())
        
        offset = (page - 1) * size
        query = query.order_by(MembershipModel.created_at.desc()).offset(offset).limit(size)
        
        result = await self.session.execute(query)
        memberships = [model.to_domain() for model in result.scalars().all()]
        
        return memberships, total
    
    async def get_daily_membership(self, gym_id: UUID) -> Optional[Membership]:
        from features.membership.domain.enums.membership_enums import MembershipStatus
        result = await self.session.execute(
            select(MembershipModel)
            .where(
                and_(
                    MembershipModel.gym_id == gym_id,
                    MembershipModel.duration_days == 1,
                    MembershipModel.status == MembershipStatus.ACTIVE
                )
            )
        )
        membership_model = result.scalar_one_or_none()
        return membership_model.to_domain() if membership_model else None
    
    async def update(self, membership: Membership) -> Optional[Membership]:
        result = await self.session.execute(
            select(MembershipModel).where(MembershipModel.id == membership.id.value)
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            return None
        
        update_data = {
            "name": membership.name,
            "description": membership.description,
            "price": membership.price.to_float(),
            "duration_days": membership.duration.to_int(),
            "type": membership.type,
            "status": membership.status,  # Direct enum assignment
            "updated_at": membership.updated_at
        }
        
        await self.session.execute(
            update(MembershipModel)
            .where(MembershipModel.id == membership.id.value)
            .values(**update_data)
        )
        
        await self.session.commit()
        
        await self.session.refresh(existing)
        return existing.to_domain()
    
    async def delete(self, membership_id: MembershipId) -> bool:
        result = await self.session.execute(
            delete(MembershipModel).where(MembershipModel.id == membership_id.value)
        )
        await self.session.commit()
        return result.rowcount > 0
    
    async def exists_with_name(
        self, 
        name: str, 
        gym_id: UUID, 
        exclude_id: Optional[MembershipId] = None
    ) -> bool:
        query = select(MembershipModel).where(
            and_(
                MembershipModel.name == name,
                MembershipModel.gym_id == gym_id
            )
        )
        
        if exclude_id:
            query = query.where(MembershipModel.id != exclude_id.value)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def is_used_by_active_clients(self, membership_id: MembershipId) -> bool:
        
        return False
