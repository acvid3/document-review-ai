from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class DocumentInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    document_id: Optional[str] = None
    metadata: Optional[dict] = None

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()


class ClassificationResult(BaseModel):
    category: str = Field(..., pattern="^(legal|financial|technical|administrative|other)$")
    confidence: float = Field(..., ge=0.0, le=1.0)
    subcategories: List[str] = Field(default_factory=list)


class NextStep(BaseModel):
    action: str = Field(..., min_length=1, max_length=200)
    priority: str = Field(..., pattern="^(high|medium|low)$")
    assignee: Optional[str] = None
    deadline: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)


class DocumentOutput(BaseModel):
    document_id: str
    summary: str = Field(..., min_length=10, max_length=1000)
    classification: ClassificationResult
    next_steps: List[NextStep]
    processing_time: float
    warnings: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ReviewResponse(BaseModel):
    success: bool
    data: Optional[DocumentOutput] = None
    error: Optional[str] = None


class BatchReviewResponse(BaseModel):
    success: bool
    results: List[DocumentOutput]
    errors: List[dict] = Field(default_factory=list)
    total_processing_time: float


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
