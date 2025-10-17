from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from dev_utils.dev_database import Base


class GymModel(Base):
    """Simple Gym model for development purposes"""
    __tablename__ = "gyms"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(200), nullable=False)
    address = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    memberships = relationship("MembershipModel", back_populates="gym")
    
    def __repr__(self) -> str:
        return f"<Gym(id={self.id}, name='{self.name}')>"
