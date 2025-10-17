from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import \
    BaseModel, \
    Field, \
    field_validator
from features.membership.domain.enums.membership_enums import MembershipStatus, MembershipType

class MembershipBaseDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the membership")
    description: str = Field(..., min_length=1, max_length=500, description="Description of the membership")
    price: float = Field(..., gt=0, description="Price of the membership (must be greater than 0)")
    type: Optional[MembershipType] = Field(default=MembershipType.REGULAR, description="Type of the membership")
    duration_days: int = Field(..., gt=0, description="Duration of the membership in days (must be greater than 0)")
    status: Optional[MembershipStatus] = Field(default=MembershipStatus.ACTIVE, description="Status of the membership")
    @field_validator('name', 'description')
    @classmethod
    def check_not_empty(cls, v):
        if isinstance(v, str) and not v.strip():
            raise ValueError("Field cannot be empty or just whitespace")
        return v.strip() if isinstance(v, str) else v

class MembershipCreateDTO(MembershipBaseDTO):
    pass

class MembershipUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the membership")
    description: Optional[str] = Field(None, min_length=1, max_length=500, description="Description of the membership")
    price: Optional[float] = Field(None, gt=0, description="Price of the membership (must be greater than 0)")
    duration_days: Optional[int] = Field(None, gt=0, description="Duration of the membership in days (must be greater than 0)")
    status: Optional[MembershipStatus] = Field(None, description="Status of the membership")
    type: Optional[MembershipType] = Field(None, description="Type of the membership")
    @field_validator('name', 'description')
    def check_not_empty(cls, v):
        if v is not None and isinstance(v, str) and not v.strip():
            raise ValueError("Field cannot be empty or just whitespace")
        return v.strip() if v is not None and isinstance(v, str) else v

class MembershipResponseDTO(BaseModel):
    id: UUID = Field(..., description="Unique identifier for the membership")
    name: str = Field(..., description="Name of the membership")
    description: str = Field(..., description="Description of the membership")
    price: float = Field(..., description="Price of the membership")
    duration_days: int = Field(..., description="Duration of the membership in days")
    status: MembershipStatus = Field(..., description="Status of the membership")
    type: MembershipType = Field(..., description="Type of the membership (derived from duration)")
    created_at: datetime = Field(..., description="When the membership was created")
    updated_at: datetime = Field(..., description="When the membership was last updated")
    gym_id: UUID = Field(..., description="ID of the gym this membership belongs to")
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: str
        }
        orm_mode = True

class MembershipListResponseDTO(BaseModel):
    items: list[MembershipResponseDTO] = Field(..., description="List of memberships")
    total: int = Field(..., description="Total number of memberships")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")