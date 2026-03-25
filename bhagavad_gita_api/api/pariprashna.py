from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from bhagavad_gita_api.api import deps
from bhagavad_gita_api.pariprashna_schemas import (
    BlockchainLogRequest,
    BlockchainLogResponse,
    ChatRequest,
    ChatResponse,
)
from bhagavad_gita_api.services.blockchain_service import (
    BlockchainDisabledError,
    BlockchainError,
    log_chat_hash,
    normalize_chat_hash,
)
from bhagavad_gita_api.services.chat_service import build_chat_response

router = APIRouter(tags=["Pariprashna AI"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(deps.get_db)):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    return build_chat_response(
        message=request.message,
        learn_mode=request.learn_mode,
        target_language=request.target_language,
        db=db,
    )


@router.post("/blockchain/log-chat", response_model=BlockchainLogResponse)
async def blockchain_log_chat(request: BlockchainLogRequest):
    try:
        normalized_hash = normalize_chat_hash(request.hash)
        transaction_hash = log_chat_hash(normalized_hash)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except BlockchainDisabledError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except BlockchainError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return BlockchainLogResponse(hash=normalized_hash, transaction_hash=transaction_hash)
