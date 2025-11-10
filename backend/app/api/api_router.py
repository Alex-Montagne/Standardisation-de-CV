from fastapi import APIRouter
from .endpoints import upload

router = APIRouter()
router.include_router(upload.router, prefix="/cv", tags=["CV Upload"])