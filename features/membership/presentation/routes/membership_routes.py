
from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
import uuid


from features.membership.application.service import MembershipService
from features.membership.application.dtos.membership_dtos import (
    MembershipListResponseDTO,
    MembershipCreateDTO,
    MembershipUpdateDTO,
    MembershipResponseDTO
)
from features.membership.domain.membership_aggregate import MembershipAggregate
from features.membership.infrastructure.repositories.membership_repository_postgres import MembershipRepositoryPostgres

# Import from our new development modules
from dev_utils.dev_database import get_session
from dev_utils.dev_security import get_current_active_user, Scopes, User

# Router
router = APIRouter(
    prefix="/api/memberships",
    tags=["memberships"],
    responses={404: {"description": "Not found"}},
)


def get_membership_service(db: AsyncSession, current_user: User) -> MembershipService:
    repository = MembershipRepositoryPostgres(db)
    aggregate = MembershipAggregate(repository)
    return MembershipService(aggregate, current_user.model_dump())

# Routes

@router.post("/", response_model=MembershipResponseDTO, status_code=201)
async def create_membership(
    membership_data: MembershipCreateDTO,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[
        User,
        Security(
            get_current_active_user,
            scopes=[Scopes.GymSuperAdmin.value],
        ),
    ]
):
    service = get_membership_service(db, current_user)
    return await service.create_membership(membership_data)

@router.get("/daily", response_model=MembershipResponseDTO)
async def get_membership_daily(
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[
        User,
        Security(
            get_current_active_user,
            scopes=[Scopes.GymSuperAdmin.value, Scopes.GymAdmin.value, Scopes.GymWorker.value],
        ),
    ]
):
    service = get_membership_service(db, current_user)
    return await service.get_daily_membership()

@router.get("/{membership_id}", response_model=MembershipResponseDTO)
async def get_membership(
    membership_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[
        User,
        Security(
            get_current_active_user,
            scopes=[Scopes.GymSuperAdmin.value, Scopes.GymAdmin.value, Scopes.GymWorker.value],
        ),
    ]
):

    service = get_membership_service(db, current_user)
    return await service.get_membership(membership_id)

@router.get("/", response_model=MembershipListResponseDTO)
async def get_memberships(
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[
        User,
        Security(
            get_current_active_user,
            scopes=[Scopes.GymSuperAdmin.value, Scopes.GymAdmin.value, Scopes.GymWorker.value],
        ),
    ],
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    status: Optional[str] = Query(None, description="Filter by status (active/inactive)"),
    search: Optional[str] = Query(None, description="Search by name or description")
):

    service = get_membership_service(db, current_user)
    return await service.list_memberships(page=page, size=size, status=status, search=search)

@router.put("/{membership_id}", status_code=204)
async def update_membership(
    membership_id: uuid.UUID,
    membership_data: MembershipUpdateDTO,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[
        User,
        Security(
            get_current_active_user,
            scopes=[Scopes.GymSuperAdmin.value],
        ),
    ]
):

    service = get_membership_service(db, current_user)
    await service.update_membership(membership_id, membership_data)
    return None

@router.delete("/{membership_id}", status_code=204)
async def delete_membership(
    membership_id: uuid.UUID,
    db:Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[
        User,
        Security(
            get_current_active_user,
            scopes=[Scopes.GymSuperAdmin.value],
        ),
    ]
):
    service = get_membership_service(db, current_user)
    await service.delete_membership(membership_id)
    return None