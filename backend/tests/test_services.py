import pytest
from app.services.guardrails import GuardrailsService
from app.services.ai_service import AIService

class TestGuardrailsService:
    def setup_method(self):
        self.guardrails = GuardrailsService()
    
    def test_validate_output_valid(self):
        """Test validation of valid output."""
        output = {
            "summary": "Test summary",
            "classification": "contract",
            "next_steps": ["Step 1", "Step 2"],
            "confidence_score": 0.85
        }
        result = self.guardrails.validate_output(output)
        assert result == output
    
    def test_validate_output_missing_field(self):
        """Test validation with missing required field."""
        output = {
            "summary": "Test summary",
            "classification": "contract"
        }
        with pytest.raises(ValueError, match="Missing required field"):
            self.guardrails.validate_output(output)
    
    def test_validate_output_invalid_classification(self):
        """Test validation with invalid classification."""
        output = {
            "summary": "Test summary",
            "classification": "invalid_category",
            "next_steps": ["Step 1"],
            "confidence_score": 0.5
        }
        result = self.guardrails.validate_output(output)
        assert result["classification"] == "other"
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        dirty_input = "<script>alert('xss')</script>"
        clean_input = self.guardrails.sanitize_input(dirty_input)
        assert "<" not in clean_input
        assert ">" not in clean_input

class TestAIService:
    def setup_method(self):
        self.ai_service = AIService()
    
    def test_clean_text(self):
        """Test text cleaning."""
        dirty_text = "This   has   extra   spaces"
        clean_text = self.ai_service._clean_text(dirty_text)
        assert clean_text == "This has extra spaces"
    
    def test_clean_classification(self):
        """Test classification cleaning."""
        assert self.ai_service._clean_classification("Contract") == "contract"
        assert self.ai_service._clean_classification("INVOICE") == "invoice"
        assert self.ai_service._clean_classification("Unknown") == "other"
    
    def test_parse_next_steps(self):
        """Test next steps parsing."""
        text = "1. First step\n2. Second step\n3. Third step"
        steps = self.ai_service._parse_next_steps(text)
        assert len(steps) == 3
        assert "First step" in steps[0]
