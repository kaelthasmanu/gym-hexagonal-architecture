from fastapi import APIRouter

from features.membership.presentation.routes.membership_routes import router as membership_router

#router = APIRouter(prefix="/memberships", tags=[ApiTags.memberships])
router = APIRouter(prefix="/api/v1", tags=["membership"])

router.include_router(membership_router, prefix="/memberships")

__all__ = ["router"]
