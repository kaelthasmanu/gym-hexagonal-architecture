from enum import Enum

class MembershipStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

class MembershipType(Enum):
    REGULAR = "regular"
    DAILY = "daily"
    PREMIUM = "premium"
    STUDENT = "student"
    CORPORATE = "corporate"

    @classmethod
    def from_duration_days(cls, duration_days: int) -> 'MembershipType':
        if duration_days == 1:
            return cls.DAILY
        elif 2 <= duration_days <= 30:
            return cls.REGULAR
        else:
            return cls.PREMIUM