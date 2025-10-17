import uuid
from dataclasses import dataclass

@dataclass(frozen=True)
class MembershipId:
    value: uuid.UUID

    def __post_init__(self):
        if not isinstance(self.value, uuid.UUID):
            try:
                object.__setattr__(self, 'value', uuid.UUID(str(self.value)))
            except (ValueError, AttributeError) as e:
                raise ValueError("Invalid UUID format for MembershipId") from e

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def generate(cls) -> 'MembershipId':
        return cls(uuid.uuid4())

    @classmethod
    def from_string(cls, value: str) -> 'MembershipId':
        return cls(uuid.UUID(value))