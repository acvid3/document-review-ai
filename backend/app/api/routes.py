from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any
from app.schemas.document import DocumentInput, DocumentOutput
from app.services.ai_service import AIService
from app.services.guardrails import GuardrailsService
from app.core.config import settings

router = APIRouter()

async def get_ai_service(request: Request) -> AIService:
    return AIService()

async def get_guardrails_service() -> GuardrailsService:
    return GuardrailsService()

@router.post("/analyze", response_model=DocumentOutput)
async def analyze_document(
    document: DocumentInput,
    ai_service: AIService = Depends(get_ai_service),
    guardrails: GuardrailsService = Depends(get_guardrails_service)
):
    try:
        result = await ai_service.process_document(document.text)

        validated_result = guardrails.validate_output(result)

        return validated_result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/analyze/batch")
async def analyze_documents_batch(
    documents: list[DocumentInput],
    ai_service: AIService = Depends(get_ai_service),
    guardrails: GuardrailsService = Depends(get_guardrails_service)
):
    results = []
    for doc in documents:
        try:
            result = await ai_service.process_document(doc.text)
            validated = guardrails.validate_output(result)
            results.append(validated)
        except Exception as e:
            results.append({"error": str(e), "document": doc.text[:100]})

    return {"results": results, "total": len(results)}
