from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from dev_utils.dev_database import Base
from features.membership.domain.enums.membership_enums import \
    MembershipStatus, \
    MembershipType


class MembershipModel(Base):
    __tablename__ = "memberships"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)
    type = Column(SQLEnum(MembershipType), nullable=False)
    status = Column(SQLEnum(MembershipStatus), default=MembershipStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    gym_id = Column(PG_UUID(as_uuid=True), ForeignKey("gyms.id"), nullable=False, index=True)

    # Relationships
    gym = relationship("GymModel", back_populates="memberships")

    def __repr__(self) -> str:
        return f"<Membership(id={self.id}, name='{self.name}', gym_id={self.gym_id})>"

    @classmethod
    def from_domain(cls, membership) -> 'MembershipModel':
        return cls(
            id=membership.id.value,
            name=membership.name,
            description=membership.description,
            price=membership.price.to_float(),
            duration_days=membership.duration.to_int(),
            type=membership.type,
            status=membership.status,
            created_at=membership.created_at,
            updated_at=membership.updated_at,
            gym_id=membership.gym_id
        )

    def to_domain(self):
        from features.membership.domain.entities.membership import Membership
        from features.membership.domain.object_values.membership_id import MembershipId
        from features.membership.domain.object_values.membership_price import MembershipPrice
        from features.membership.domain.object_values.membership_duration import MembershipDuration
        print(self.type, "self")
        return Membership(
            id=MembershipId(self.id),
            name=self.name,
            description=self.description,
            price=MembershipPrice.from_float(self.price),
            duration=MembershipDuration.from_int(self.duration_days),
            type=self.type,
            status=self.status,  # Direct enum assignment
            created_at=self.created_at,
            updated_at=self.updated_at,
            gym_id=self.gym_id
        )