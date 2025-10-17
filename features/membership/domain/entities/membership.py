from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID
from features.membership.domain.enums.membership_enums import MembershipStatus, MembershipType
from features.membership.domain.object_values.membership_duration import MembershipDuration
from features.membership.domain.object_values.membership_id import MembershipId
from features.membership.domain.object_values.membership_price import MembershipPrice

@dataclass
class Membership:
    id: MembershipId
    name: str
    description: str
    price: MembershipPrice
    duration: MembershipDuration
    type: MembershipType
    gym_id: UUID
    status: MembershipStatus = field(default=MembershipStatus.ACTIVE)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_domain(self):
        return Membership(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            duration=self.duration,
            type=self.type,
            gym_id=self.gym_id,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.name or not self.name.strip():
            raise ValueError("Membership name cannot be empty")
        if not self.description or not self.description.strip():
            raise ValueError("Membership description cannot be empty")
        if not isinstance(self.gym_id, UUID):
            raise ValueError("Invalid gym ID format")

    def update(self,
              name: Optional[str] = None, 
              description: Optional[str] = None,
              price: Optional[MembershipPrice] = None,
              duration: Optional[MembershipDuration] = None,
              status: Optional[MembershipStatus] = None) -> None:
        if name is not None:
            if not name.strip():
                raise ValueError("Membership name cannot be empty")
            self.name = name
        if description is not None:
            if not description.strip():
                raise ValueError("Membership description cannot be empty")
            self.description = description
        if price is not None:
            self.price = price
        if duration is not None:
            self.duration = duration
        if status is not None:
            self.status = status
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.status = MembershipStatus.ACTIVE
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.status = MembershipStatus.INACTIVE
        self.updated_at = datetime.now()

    def archive(self) -> None:
        self.status = MembershipStatus.ARCHIVED
        self.updated_at = datetime.now()

    def is_active(self) -> bool:
        return self.status == MembershipStatus.ACTIVE

    def is_daily(self) -> bool:
        return self.duration.is_daily()

    def get_type(self) -> MembershipType:
        return MembershipType.from_duration_days(self.duration.to_int())

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "price": self.price.to_float(),
            "duration_days": self.duration.to_int(),
            "status": self.status.value,
            "type": self.type.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "gym_id": str(self.gym_id)
        }