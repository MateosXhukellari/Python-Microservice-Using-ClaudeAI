# DocuMind AI — Python Service 🐍

The AI brain of the DocuMind platform. A FastAPI microservice that handles all document parsing and Claude AI integration. Called exclusively by the Java Spring Boot backend — never directly by the frontend.

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-green)
![Claude](https://img.shields.io/badge/Claude-Anthropic-purple)

---

## What it does

- **Parses documents** — extracts plain text from PDF, DOCX, and TXT files
- **AI summarization** — sends extracted text to Claude and returns a clean summary with key topics
- **Document chat** — handles Q&A conversations about a document with full streaming support
- **Document comparison** — sends two document texts to Claude and returns a structured analysis
- **Data extraction** — pulls structured fields (dates, parties, amounts) from contracts and invoices

---

## Tech Stack

| Tool | Purpose |
|---|---|
| FastAPI | Web framework with automatic API docs |
| Uvicorn | ASGI server |
| Anthropic SDK | Claude API integration |
| pdfplumber | PDF text extraction |
| python-docx | DOCX text extraction |
| httpx | Async HTTP client for Supabase file downloads |
| Pydantic | Request/response validation |
| python-dotenv | Environment variable management |

---

## Project Structure

```
backend-python/
├── main.py                  # FastAPI app, CORS, router registration
├── config.py                # Reads ANTHROPIC_API_KEY from .env
├── .env                     # API keys — never committed to Git
├── requirements.txt         # All dependencies
├── models/
│   ├── __init__.py
│   └── schemas.py           # Pydantic request/response models
├── routers/
│   ├── __init__.py
│   ├── health.py            # GET /health
│   ├── parse.py             # POST /parse
│   ├── summarize.py         # POST /summarize
│   ├── chat.py              # POST /chat (streaming)
│   ├── compare.py           # POST /compare
│   └── extract.py           # POST /extract
└── services/
    ├── __init__.py
    ├── parser.py            # PDF, DOCX, TXT text extraction
    ├── claude_service.py    # All Claude API calls
    └── chunker.py           # Splits large documents for token limits
```

---

## API Endpoints

| Method | Endpoint | Called by Java when... | Description |
|---|---|---|---|
| GET | `/health` | Railway uptime check | Returns service status |
| POST | `/parse` | Document uploaded | Downloads file from Supabase, extracts text |
| POST | `/summarize` | After /parse completes | Sends text to Claude, returns summary + topics |
| POST | `/chat` | User sends a message | Streams Claude response token by token |
| POST | `/compare` | User clicks Compare | Sends two texts to Claude for diff analysis |
| POST | `/extract` | User clicks Extract Data | Returns structured fields as JSON |

---

## Getting Started

### Prerequisites

- Python 3.11+
- Anthropic API key from [console.anthropic.com](https://console.anthropic.com)

### 1. Clone and navigate

```bash
git clone https://github.com/yourusername/documind-ai.git
cd documind-ai/python-ai-service/backend-python
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create .env file

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 6. Run the service

```bash
uvicorn main:app --reload --port 8000
```

### 7. Test it

- Health check: `http://localhost:8000/health`
- Interactive API docs: `http://localhost:8000/docs`

---

## How it connects to Java

The Java Spring Boot backend calls this service via HTTP using `RestTemplate`. The Python service URL is configured in Java's `application.properties`:

```properties
python.service.url=http://localhost:8000
```

**Upload flow:**
```
User uploads file
    → Java saves to Supabase
    → Java calls POST /parse with file URL
    → Python extracts text
    → Java calls POST /summarize with extracted text
    → Claude generates summary
    → Java saves summary to PostgreSQL
    → Document status set to READY
```

**Chat flow:**
```
User sends question
    → Java calls POST /chat with question + document text + history
    → Python streams Claude response
    → Java forwards stream to React frontend
    → User sees tokens appearing in real time
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Claude API key from console.anthropic.com |

---

## Interactive Docs

FastAPI automatically generates interactive API documentation. Once the service is running visit:

```
http://localhost:8000/docs
```

You can test every endpoint directly from the browser — no Postman needed.

---

## Part of DocuMind AI

This is the Python microservice component of the DocuMind AI platform. See the main repository for the full system including the Java Spring Boot backend and React frontend.

---

## Author

Built by [Your Name] — student developer from Albania.

GitHub: [github.com/yourusername](https://github.com/yourusername)
