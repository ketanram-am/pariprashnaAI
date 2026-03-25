from fastapi import APIRouter

from bhagavad_gita_api.api.api_v2.endpoints import gita

try:
    from bhagavad_gita_api.api.api_v2.endpoints import social
except Exception:
    social = None

api_router = APIRouter()
api_router.include_router(gita.router)
if social is not None:
    api_router.include_router(social.router, include_in_schema=True)
