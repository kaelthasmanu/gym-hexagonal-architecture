from dataclasses import dataclass

@dataclass(frozen=True)
class MembershipDuration:
    days: int

    def __post_init__(self):
        if not isinstance(self.days, int) or self.days <= 0:
            raise ValueError("Duration must be a positive integer")

    def __str__(self) -> str:
        if self.days == 1:
            return "1 day"
        return f"{self.days} days"

    def to_int(self) -> int:
        return self.days

    @classmethod
    def from_int(cls, days: int) -> 'MembershipDuration':
        return cls(days)

    def is_daily(self) -> bool:
        return self.days == 1