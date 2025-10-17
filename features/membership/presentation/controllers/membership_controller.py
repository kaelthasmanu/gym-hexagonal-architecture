import \
    uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from features.membership.application.dtos.membership_dtos import (
    MembershipCreateDTO,
    MembershipResponseDTO,
    MembershipUpdateDTO,
    MembershipListResponseDTO
)
from features.membership.application.errors.membership_errors import (
    MembershipNotFoundError,
    MembershipAlreadyExistsError,
    DailyMembershipExistsError,
    MembershipInUseError,
    UnauthorizedMembershipAccessError,
    InvalidMembershipDataError
)
from features.membership.application.service import MembershipService

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

class MembershipController:

    def __init__(self, membership_service: MembershipService):
        self.membership_service = membership_service
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            "/",
            self.create_membership,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
            response_model=MembershipResponseDTO,
            responses={
                400: {"model": ErrorResponse},
                409: {"model": ErrorResponse},
            },
        )

        self.router.add_api_route(
            "/daily",
            self.get_daily_membership,
            methods=["GET"],
            response_model=MembershipResponseDTO,
            responses={
                404: {"model": ErrorResponse},
            },
        )

        self.router.add_api_route(
            "/{membership_id}",
            self.get_membership,
            methods=["GET"],
            response_model=MembershipResponseDTO,
            responses={
                404: {"model": ErrorResponse},
                403: {"model": ErrorResponse},
            },
        )

        self.router.add_api_route(
            "/",
            self.list_memberships,
            methods=["GET"],
            response_model=MembershipListResponseDTO,
        )

        self.router.add_api_route(
            "/{membership_id}",
            self.update_membership,
            methods=["PUT"],
            response_model=MembershipResponseDTO,
            responses={
                400: {"model": ErrorResponse},
                403: {"model": ErrorResponse},
                404: {"model": ErrorResponse},
                409: {"model": ErrorResponse},
            },
        )

        self.router.add_api_route(
            "/{membership_id}",
            self.delete_membership,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
            responses={
                403: {"model": ErrorResponse},
                404: {"model": ErrorResponse},
                409: {"model": ErrorResponse},
            },
        )

    async def create_membership(self, membership_data: MembershipCreateDTO) -> MembershipResponseDTO:
        try:
            return await self.membership_service.create_membership(membership_data)
        except (MembershipAlreadyExistsError, DailyMembershipExistsError, InvalidMembershipDataError) as e:
            status_code = 400 if isinstance(e, InvalidMembershipDataError) else 409
            raise HTTPException(
                status_code=status_code,
                detail={"detail": str(e), "error_code": e.__class__.__name__}
            )

    async def get_membership(self, membership_id: uuid.UUID) -> MembershipResponseDTO:
        try:
            return await self.membership_service.get_membership(membership_id)

        except MembershipNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"detail": str(e), "error_code": e.__class__.__name__}
            )

        except UnauthorizedMembershipAccessError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"detail": str(e), "error_code": e.__class__.__name__}
            )

    async def get_daily_membership(self) -> MembershipResponseDTO:
        try:
            return await self.membership_service.get_daily_membership()

        except MembershipNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"detail": str(e), "error_code": e.__class__.__name__}
            )

    async def list_memberships(
        self,
        page: int = 1,
        size: int = 10,
        membership_status: Optional[str] = None,
        search: Optional[str] = None
    ) -> MembershipListResponseDTO:
        return await self.membership_service.list_memberships(
            page=page,
            size=size,
            status=membership_status,
            search=search
        )

    async def update_membership(
        self,
        membership_id: uuid.UUID,
        update_data: MembershipUpdateDTO
    ) -> MembershipResponseDTO:
        try:
            return await self.membership_service.update_membership(membership_id, update_data)

        except (MembershipNotFoundError, UnauthorizedMembershipAccessError) as e:
            status_code = 404 if isinstance(e, MembershipNotFoundError) else 403
            raise HTTPException(
                status_code=status_code,
                detail={"detail": str(e), "error_code": e.__class__.__name__}
            )

        except (MembershipAlreadyExistsError, DailyMembershipExistsError, InvalidMembershipDataError) as e:
            status_code = 400 if isinstance(e, InvalidMembershipDataError) else 409
            raise HTTPException(
                status_code=status_code,
                detail={"detail": str(e), "error_code": e.__class__.__name__}
            )

    async def delete_membership(self, membership_id: uuid.UUID) -> None:
        try:
            deleted = await self.membership_service.delete_membership(membership_id)

            if not deleted:
                raise MembershipNotFoundError(membership_id)
            
            return None

        except MembershipNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"detail": str(e), "error_code": e.__class__.__name__}
            )

        except UnauthorizedMembershipAccessError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"detail": str(e), "error_code": e.__class__.__name__}
            )

        except MembershipInUseError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"detail": str(e), "error_code": e.__class__.__name__}
            )