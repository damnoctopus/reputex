# RepuTex Backend (Gemini Intelligence Engine)

A clean, contract-first reputation intelligence backend built with FastAPI, PostgreSQL/SQLite, and the Google Gemini API (`gemini-3.6-flash`).

## 🌟 Overview

RepuTex collects recent public customer mentions across **Google**, **Reddit**, and **X / Twitter** using **Gemini Google Search Grounding**, analyzes them using structured Gemini semantic intelligence, and accumulates a business's reputation history over time.

It answers:
1. **What are people saying about this business?** (Public sentiment across platforms)
2. **What are the main recurring problems?** (Semantic complaint clustering with cross-platform aggregation)
3. **Are there potentially manipulated review patterns?** (Multi-signal review authenticity and coordinated burst detection)
4. **Is there a reputation crisis developing?** (Deterministic early warning crisis engine)
5. **Show me the evidence.** (Traceable evidence quotes linked to every finding)

---

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.12+)
- **Validation**: Pydantic v2
- **Database**: SQLAlchemy 2.x + AsyncPG / Aiosqlite + Alembic
- **AI Intelligence**: Google Gemini API (`gemini-3.6-flash` via `google-genai` SDK)
- **Web Discovery**: Gemini Google Search Grounding (bounded, budgeted, cached)
- **Background Execution**: In-process background tasks (default) or Celery + Redis
- **Security**: Password hashing (Bcrypt) + JWT Authentication (PyJWT)
- **Frontend**: Flutter mobile app (`Reputex-App`) reused unchanged

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone or navigate to directory
cd c:\Users\adira\Projects\major\Reputex-GeminiBackend

# Create virtual environment and install dependencies
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```ini
APP_NAME=RepuTex Intelligence Backend
ENVIRONMENT=development
DATABASE_URL=sqlite+aiosqlite:///./reputex.db
SYNC_DATABASE_URL=sqlite:///./reputex.db
SECRET_KEY=reputex_super_secret_jwt_key_change_in_production_32bytes!

# Set your Gemini API key (or leave empty for 100% offline mock mode)
GEMINI_API_KEY=
USE_MOCK_ACQUISITION=true
USE_MOCK_GEMINI=true
```

### 3. Run Database Migrations
```bash
alembic upgrade head
```

### 4. Start the Application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API documentation will be available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

All 16 unit, contract, and end-to-end scan tests run 100% offline with zero external network dependencies.
