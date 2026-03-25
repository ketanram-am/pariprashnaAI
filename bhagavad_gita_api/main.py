import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

from bhagavad_gita_api.api import deps
from bhagavad_gita_api.api.pariprashna import router as pariprashna_router
from bhagavad_gita_api.api.api_v2.api import api_router
from bhagavad_gita_api.config import settings
from bhagavad_gita_api.crud import get_valid_api_keys

API_KEY_NAME = "X-API-KEY"
api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(
    db: Session = Depends(deps.get_db),
    api_key_header: str = Security(api_key_header_auth),
) -> None:
    valid_api_keys = set(get_valid_api_keys(db))
    valid_api_keys.add(settings.TESTER_API_KEY)

    if api_key_header not in valid_api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key.",
        )


app = FastAPI(
    title="Pariprashna AI - Enquire Within",
    description="A simple hackathon prototype that blends Bhagavad Gita wisdom, "
    "multilingual chat, Learn Mode, and minimal EVM blockchain logging.",
    version="3.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def index():
    return {"message": "Pariprashna AI - Enquire Within"}


app.include_router(pariprashna_router)
app.include_router(
    api_router,
    prefix=settings.API_V2_STR,
    dependencies=[Security(get_api_key, scopes=["openid"])],
)

# app.add_route(
#     "/graphql",
#     GraphQLApp(executor_class=AsyncioExecutor, schema=graphene.Schema(query=Query)),
# )


def cli():
    # this function will be called when run from cli
    uvicorn.run(
        "bhagavad_gita_api.main:app",
        host="0.0.0.0",
        port=8081,
        reload=bool(settings.debug),
    )
