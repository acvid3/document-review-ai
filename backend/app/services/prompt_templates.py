class PromptTemplates:
    
    @staticmethod
    def get_summary_prompt(text: str) -> str:
        return f"""Please provide a concise summary of the following document. 
Focus on key points, main topics, and important details.

Document:
{text}

Summary (max 500 characters):"""
    
    @staticmethod
    def get_classification_prompt(text: str) -> str:
        return f"""Classify the following document into one of these categories:
- contract
- invoice
- report
- email
- proposal
- legal_document
- technical_doc
- other

Document:
{text}

Classification (just the category name):"""
    
    @staticmethod
    def get_next_steps_prompt(text: str, summary: str, classification: str) -> str:
        return f"""Based on the following document analysis, generate 3-5 specific next steps or action items.

Document Summary: {summary}
Document Classification: {classification}

Original Document:
{text}

Please provide numbered next steps (1. 2. 3. etc.):"""
