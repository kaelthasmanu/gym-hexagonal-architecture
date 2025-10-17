from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

# Enums
class Scopes(str, Enum):
    GymSuperAdmin = "gym:superadmin"
    GymAdmin = "gym:admin"
    GymWorker = "gym:worker"

class SystemModulesEnum(str, Enum):
    MEMBERSHIP = "membership"
    # Add other modules as needed

class SystemOperationsEnum(str, Enum):
    ADDITION = "addition"
    MODIFICATION = "modification"
    DELETION = "deletion"
    # Add other operations as needed

# Base Models
class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    email: str
    full_name: str
    disabled: bool = False
    scopes: List[str] = []
    id_gym: UUID = Field(default_factory=uuid4)

    class Config:
        from_attributes = True

class MembershipBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    price: float = Field(..., gt=0)
    duration_days: int = Field(..., gt=0)
    status: bool = True

class MembershipCreate(MembershipBase):
    pass

class MembershipUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    duration_days: Optional[int] = Field(None, gt=0)
    status: Optional[bool] = None

class MembershipPublic(MembershipBase):
    id: UUID
    id_gym: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Helper functions
def membership_to_dict(membership: 'MembershipPublic') -> Dict[str, Any]:
    """Convierte un objeto Membership a un diccionario para el logging"""
    return {
        "id": str(membership.id),
        "name": membership.name,
        "description": membership.description,
        "price": float(membership.price) if membership.price else None,
        "duration_days": membership.duration_days,
        "status": membership.status,
        "created_at": membership.created_at.isoformat() if membership.created_at else None,
        "updated_at": membership.updated_at.isoformat() if membership.updated_at else None,
        "id_gym": str(membership.id_gym) if membership.id_gym else None
    }

# Database Models (SQLAlchemy)
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Membership(Base):
    __tablename__ = "memberships"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    id_gym = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "duration_days": self.duration_days,
            "status": self.status,
            "id_gym": self.id_gym,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
