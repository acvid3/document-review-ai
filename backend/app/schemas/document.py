from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class DocumentInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Document text to analyze")
    metadata: Optional[dict] = Field(default=None, description="Optional metadata about the document")

    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v.strip()

class DocumentOutput(BaseModel):
    summary: str = Field(..., max_length=500, description="Summarized content of the document")
    classification: str = Field(..., description="Document classification category")
    next_steps: List[str] = Field(..., description="Structured next-step notes")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the analysis")
    processing_time: Optional[float] = Field(default=None, description="Time taken to process in seconds")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    @validator('classification')
    def classification_must_be_valid(cls, v):
        valid_categories = [
            "contract", "invoice", "report", "email",
            "proposal", "legal_document", "technical_doc", "other"
        ]
        if v.lower() not in valid_categories:
            raise ValueError(f"Classification must be one of: {', '.join(valid_categories)}")
        return v.lower()
