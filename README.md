# Document Review AI

A proof-of-concept system that automates document review workflows using LLMs (OpenAI, Claude, Gemini). Accepts text input, summarizes content, classifies into categories, and generates actionable next steps with structured output validation.

## Features

- **Summarization** — extracts key points from documents
- **Classification** — categorizes by type (email, contract, invoice, report, etc.)
- **Next Steps** — generates structured action items
- **Guardrails** — validated, constrained outputs with confidence scoring
- **Multi-Provider** — supports OpenAI, Anthropic Claude, and Google Gemini
- **Batch Processing** — analyze multiple documents at once

## Architecture

```
frontend/         Next.js UI (Tailwind, ReactDropzone, ReactMarkdown)
backend/          FastAPI (Python 3.11)
  app/
    api/          REST endpoints
    core/         config, settings
    services/     AI logic, guardrails, prompt building
    schemas/      Pydantic models
docker-compose.yml
```

## Quick Start

```bash
# 1. Set your API key
export OPENAI_API_KEY="sk-..."

# 2. Start both services
docker compose up -d

# 3. Open the app
open http://localhost:3000
```

### API Usage

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Your document text here"}'
```

Response includes `summary`, `classification`, `next_steps`, `confidence_score`, and `timestamp`.

### Configuration

Set via environment variables or `backend/.env`:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | OpenAI API key |
| `ANTHROPIC_API_KEY` | — | Anthropic API key |
| `GEMINI_API_KEY` | — | Google Gemini API key |
| `LLM_PROVIDER` | `openai` | Provider: `openai`, `claude`, or `gemini` |
| `LLM_MODEL` | `gpt-4` | Model name |

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic, Uvicorn
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **Infrastructure:** Docker, Docker Compose
# document-review-ai
