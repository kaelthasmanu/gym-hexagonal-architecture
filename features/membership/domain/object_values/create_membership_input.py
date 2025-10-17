from dataclasses import dataclass, field
from uuid import UUID

from features.membership.domain.enums.membership_enums import \
    MembershipType, \
    MembershipStatus

@dataclass
class CreateMembershipInput:
    name: str
    description: str
    price: float
    duration: int
    type: MembershipType
    gym_id: UUID
    status: MembershipStatus = field(default=MembershipStatus.ACTIVE)