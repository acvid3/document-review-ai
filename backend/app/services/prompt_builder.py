class PromptBuilder:
    
    SYSTEM_PROMPT = """You are an AI document review assistant. Your task is to analyze documents 
and provide structured outputs. Always respond with valid JSON only, no additional text."""
    
    @staticmethod
    def build_summary_prompt(text: str, max_length: int = 500) -> str:
        return f"""Summarize the following document in {max_length} characters or less. 
Focus on key points, main arguments, and critical information.

Document:
{text}

Provide a concise summary:"""
    
    @staticmethod
    def build_classification_prompt(text: str) -> str:
        return f"""Classify the following document into exactly one of these categories:
- legal: Legal documents, contracts, agreements, court filings
- financial: Financial reports, invoices, budgets, accounting
- technical: Technical documentation, specifications, code, architecture
- administrative: Internal memos, HR documents, policies, procedures
- other: Any document that doesn't fit the above categories

Also provide a confidence score (0.0 to 1.0) and relevant subcategories.

Document:
{text}

Respond with JSON in this exact format:
{{"category": "category_name", "confidence": 0.95, "subcategories": ["sub1", "sub2"]}}"""
    
    @staticmethod
    def build_next_steps_prompt(summary: str, classification: dict) -> str:
        return f"""Based on the following document summary and classification, 
generate 1-3 structured next-step actions.

Summary: {summary}
Classification: {classification['category']} (confidence: {classification['confidence']})

For each action, provide:
- action: Clear actionable step (max 200 chars)
- priority: high, medium, or low
- assignee: Suggested role/department
- deadline: Suggested timeframe
- notes: Additional context (max 500 chars)

Respond with JSON array:
[{{"action": "...", "priority": "high", "assignee": "...", "deadline": "...", "notes": "..."}}]"""
    
    @staticmethod
    def build_full_review_prompt(text: str) -> str:
        return f"""Analyze the following document and provide:
1. A concise summary (max 500 characters)
2. Classification into one category: legal, financial, technical, administrative, or other
3. Confidence score (0.0 to 1.0)
4. Relevant subcategories
5. 1-3 recommended next steps with priority levels

Document:
{text}

Respond with valid JSON only:
{{
    "summary": "concise summary here",
    "classification": {{
        "category": "category_name",
        "confidence": 0.95,
        "subcategories": ["sub1", "sub2"]
    }},
    "next_steps": [
        {{
            "action": "action description",
            "priority": "high|medium|low",
            "assignee": "suggested role",
            "deadline": "timeframe",
            "notes": "additional context"
        }}
    ]
}}"""
