from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# PostgreSQL connection URL for development
# Format: postgresql+asyncpg://user:password@host:port/database
DATABASE_USER = os.getenv("DB_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DATABASE_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_PORT = os.getenv("DB_PORT", "5432")
DATABASE_NAME = os.getenv("DB_NAME", "gym_dev")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Async engine for PostgreSQL
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Log SQL queries for debugging
    future=True
)
# Async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def init_db():
    """Create all tables in the database"""
    # Import models to register them with Base.metadata
    from dev_utils.dev_gym_model import GymModel
    from features.membership.infrastructure.entities.membership_model import MembershipModel

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    """Dependency to get async DB session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def drop_all_tables():
    """Drop all tables (useful for testing)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def reset_db():
    """Reset database: drop all tables and recreate them"""
    await drop_all_tables()
    await init_db()
