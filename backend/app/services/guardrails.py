from typing import Dict, Any, List
from app.core.config import settings

class GuardrailsService:
    def __init__(self):
        self.max_summary_length = settings.MAX_SUMMARY_LENGTH
        self.max_next_steps_length = settings.MAX_NEXT_STEPS_LENGTH
        self.required_fields = settings.REQUIRED_OUTPUT_FIELDS

    def validate_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        for field in self.required_fields:
            if field not in output:
                raise ValueError(f"Missing required field: {field}")

        if len(output.get("summary", "")) > self.max_summary_length:
            output["summary"] = output["summary"][:self.max_summary_length]

        next_steps = output.get("next_steps", [])
        validated_steps = []
        for step in next_steps:
            if len(step) > self.max_next_steps_length:
                step = step[:self.max_next_steps_length]
            validated_steps.append(step)
        output["next_steps"] = validated_steps

        confidence = output.get("confidence_score", 0.0)
        if not isinstance(confidence, (int, float)):
            confidence = 0.0
        output["confidence_score"] = max(0.0, min(1.0, float(confidence)))

        valid_categories = [
            "contract", "invoice", "report", "email",
            "proposal", "legal_document", "technical_doc", "other"
        ]
        classification = output.get("classification", "").lower()
        if classification not in valid_categories:
            output["classification"] = "other"

        return output

    def sanitize_input(self, text: str) -> str:
        import re
        sanitized = re.sub(r'[<>\'"]', '', text)
        return sanitized.strip()
