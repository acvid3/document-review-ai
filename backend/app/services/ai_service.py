import re
from typing import Dict, Any, Optional
from app.services.llm_client import LLMClient
from app.services.prompt_templates import PromptTemplates
from app.core.config import settings

class AIService:
    def __init__(self):
        self.llm_client = LLMClient()
        self.prompts = PromptTemplates()

    async def process_document(self, text: str) -> Dict[str, Any]:
        summary_prompt = self.prompts.get_summary_prompt(text)
        summary = await self.llm_client.generate(summary_prompt)

        summary = self._clean_text(summary)

        classification_prompt = self.prompts.get_classification_prompt(text)
        classification = await self.llm_client.generate(classification_prompt)
        classification = self._clean_classification(classification)

        next_steps_prompt = self.prompts.get_next_steps_prompt(text, summary, classification)
        next_steps_raw = await self.llm_client.generate(next_steps_prompt)
        next_steps = self._parse_next_steps(next_steps_raw)

        confidence_score = self._calculate_confidence(summary, classification, next_steps)

        return {
            "summary": summary[:settings.MAX_SUMMARY_LENGTH],
            "classification": classification,
            "next_steps": next_steps[:3],
            "confidence_score": confidence_score
        }

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _clean_classification(self, classification: str) -> str:
        classification = classification.lower().strip()
        valid_categories = [
            "contract", "invoice", "report", "email",
            "proposal", "legal_document", "technical_doc", "other"
        ]

        for category in valid_categories:
            if category in classification:
                return category
        return "other"

    def _parse_next_steps(self, text: str) -> list:
        steps = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                clean_line = re.sub(r'^[\d\-\*\.\s]+', '', line).strip()
                if clean_line and len(clean_line) > 10:
                    steps.append(clean_line)

        if not steps:
            steps = [text.strip()]

        return steps

    def _calculate_confidence(self, summary: str, classification: str, next_steps: list) -> float:
        score = 0.7

        if len(summary) > 50:
            score += 0.1
        if len(summary) > 100:
            score += 0.1

        if classification != "other":
            score += 0.1

        if len(next_steps) >= 2:
            score += 0.1

        return min(score, 1.0)
