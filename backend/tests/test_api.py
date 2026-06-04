import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_document_success():
    """Test successful document analysis."""
    test_document = {
        "text": "This is a test contract document for evaluation purposes."
    }
    response = client.post("/api/v1/analyze", json=test_document)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "classification" in data
    assert "next_steps" in data
    assert "confidence_score" in data

def test_analyze_document_empty_text():
    """Test document analysis with empty text."""
    test_document = {"text": ""}
    response = client.post("/api/v1/analyze", json=test_document)
    assert response.status_code == 422  # Validation error

def test_analyze_document_long_text():
    """Test document analysis with very long text."""
    long_text = "A" * 10001  # Exceeds max length
    test_document = {"text": long_text}
    response = client.post("/api/v1/analyze", json=test_document)
    assert response.status_code == 422

def test_batch_analysis():
    """Test batch document analysis."""
    documents = [
        {"text": "First test document"},
        {"text": "Second test document"}
    ]
    response = client.post("/api/v1/analyze/batch", json=documents)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2

@pytest.mark.asyncio
async def test_ai_service_integration():
    """Test AI service integration (requires API keys)."""
    from app.services.ai_service import AIService
    service = AIService()
    
    # Skip if no API key configured
    if not settings.OPENAI_API_KEY:
        pytest.skip("No API key configured")
    
    result = await service.process_document("Test document for integration testing")
    assert "summary" in result
    assert "classification" in result
    assert "next_steps" in result
