from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

@dataclass(frozen=True)
class MembershipPrice:
    value: Decimal

    def __post_init__(self):
        if not isinstance(self.value, Decimal):
            try:
                decimal_value = Decimal(str(self.value))
                object.__setattr__(self, 'value', decimal_value)
            except (ValueError, InvalidOperation) as e:
                raise ValueError("Price must be a valid decimal number") from e
        if self.value < 0:
            raise ValueError("Price cannot be negative")
        # Ensure exactly 2 decimal places
        object.__setattr__(self, 'value', self.value.quantize(Decimal('0.00')))

    def __str__(self) -> str:
        return f"${self.value:.2f}"

    def to_float(self) -> float:
        return float(self.value)

    @classmethod
    def from_float(cls, value: float) -> 'MembershipPrice':
        return cls(Decimal(str(value)))

    @classmethod
    def from_string(cls, value: str) -> 'MembershipPrice':
        try:
            return cls(Decimal(value))
        except (ValueError, InvalidOperation) as e:
            raise ValueError("Invalid price format") from e