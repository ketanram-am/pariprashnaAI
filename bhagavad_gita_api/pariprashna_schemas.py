from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    learn_mode: bool = False
    target_language: Optional[str] = None


class ChatResponse(BaseModel):
    reference: str
    shloka: str
    meaning: str
    word_meaning: str = ""
    advice: str
    source_language: str = "en"
    response_language: str = "en"
    response_hash: str
    transaction_hash: Optional[str] = None


class BlockchainLogRequest(BaseModel):
    hash: str = Field(..., description="0x-prefixed bytes32 chat hash")


class BlockchainLogResponse(BaseModel):
    hash: str
    transaction_hash: str
    status: str = "submitted"
