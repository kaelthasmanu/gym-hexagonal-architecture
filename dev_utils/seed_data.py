"""Seed data for development database"""
import asyncio
from uuid import UUID
from datetime import datetime

from dev_utils.dev_database import AsyncSessionLocal, init_db
from dev_utils.dev_gym_model import GymModel


async def seed_gym_data():
    """Create a test gym with the ID used in dev_security"""
    async with AsyncSessionLocal() as session:
        # Check if gym already exists
        from sqlalchemy import select
        
        gym_id = UUID("00000000-0000-0000-0000-000000000000")
        result = await session.execute(
            select(GymModel).where(GymModel.id == gym_id)
        )
        existing_gym = result.scalar_one_or_none()
        
        if not existing_gym:
            # Create test gym
            test_gym = GymModel(
                id=gym_id,
                name="Test Gym",
                address="123 Test Street, Test City",
                is_active=True
            )
            session.add(test_gym)
            await session.commit()
            print(f"✅ Created test gym: {test_gym.name} (ID: {test_gym.id})")
        else:
            print(f"ℹ️  Test gym already exists: {existing_gym.name}")


async def seed_membership_data():
    """Create test memberships"""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        from features.membership.infrastructure.entities.membership_model import MembershipModel
        from features.membership.domain.enums.membership_enums import MembershipStatus
        
        gym_id = UUID("00000000-0000-0000-0000-000000000000")
        
        # Check if memberships already exist
        result = await session.execute(
            select(MembershipModel).where(MembershipModel.gym_id == gym_id)
        )
        existing_memberships = result.scalars().all()
        
        if existing_memberships:
            print(f"ℹ️  Memberships already exist ({len(existing_memberships)} found)")
            return
        
        # Create test memberships
        memberships = [
            MembershipModel(
                name="Daily Pass",
                description="Access for one day",
                price=15.0,
                duration_days=1,
                status=MembershipStatus.ACTIVE,
                gym_id=gym_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            MembershipModel(
                name="Weekly Pass",
                description="Access for one week",
                price=50.0,
                duration_days=7,
                status=MembershipStatus.ACTIVE,
                gym_id=gym_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            MembershipModel(
                name="Monthly Membership",
                description="Full month access with all amenities",
                price=100.0,
                duration_days=30,
                status=MembershipStatus.ACTIVE,
                gym_id=gym_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            MembershipModel(
                name="Annual Membership",
                description="Best value - full year access",
                price=1000.0,
                duration_days=365,
                status=MembershipStatus.ACTIVE,
                gym_id=gym_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
        ]
        
        for membership in memberships:
            session.add(membership)
        
        await session.commit()
        print(f"✅ Created {len(memberships)} test memberships")


async def seed_all():
    """Initialize database and seed all test data"""
    print("🌱 Seeding database...")
    await init_db()
    await seed_gym_data()
    print("✅ Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_all())
