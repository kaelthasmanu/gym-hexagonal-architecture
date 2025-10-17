from dataclasses import dataclass
from typing import Optional

from features.membership.domain.enums.membership_enums import MembershipType, MembershipStatus


@dataclass
class UpdateMembershipInput:
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[int] = None
    type: Optional[MembershipType] = None
    status: Optional[MembershipStatus] = None
