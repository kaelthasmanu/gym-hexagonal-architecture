from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging


from features.membership import membership_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Gym Management API",
    description="API for managing gym memberships and related operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Application events
@app.on_event("startup")
async def startup_event():
    from dev_utils.seed_data import seed_all
    await seed_all()
    logger.info("Database initialized and seeded successfully")

app.include_router(membership_router)

from features.membership.application.errors.membership_errors import MembershipError

@app.exception_handler(MembershipError)
async def membership_error_handler(request: Request, exc: MembershipError):
    logger.warning(f"Membership error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": exc.__class__.__name__},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "error_code": "INTERNAL_SERVER_ERROR"},
    )

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Gym Management API",
        "documentation": "/docs",
        "version": "1.0.0"
    }
