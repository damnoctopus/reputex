# RepuTex Backend — AI Reputation Intelligence Engine

RepuTex is an enterprise-grade AI-powered business reputation monitoring and management platform. This repository contains the production FastAPI backend built specifically to power the companion Flutter mobile application.

---

## Architecture Overview

RepuTex uses a clean **Modular Monolith** architecture with strict unidirectional dependency flow:

```
                  Flutter Mobile App (Dio)
                             │
                  HTTPS (Bearer JWT Auth)
                             │
                             ▼
                    FastAPI REST API
             (Dual mounts: /api/v1/ and /api/)
                             │
            ┌────────────────┴────────────────┐
            │                                 │
       API Routers                      Core Security & DB
            │                                 │
            ▼                                 ▼
        Services                     AI & Integrations
    (Business Logic)                (Mock & Gemini API)
            │                                 │
            ▼                                 ▼
       Repositories                      Background
     (Data Access)                    (Celery & Redis)
            │
            ▼
       PostgreSQL / SQLite
```

### Core Design Rules
1. **Zero Database Access in Routes**: All database operations must pass through Repositories and Services.
2. **Strict Multi-Tenant Isolation**: Every business-scoped resource is verified against user ownership or active `BusinessMember` membership.
3. **Resilient Dual-Mode Operation**: `PLATFORM_MODE=mock` and `AI_PROVIDER=mock` allow 100% offline local development and test suite execution without external paid API keys.
4. **100% Flutter Compatibility**: Fully compatible with the existing Freezed models, Riverpod providers, and `RealApiService` endpoints (`/dashboard`, `/mentions`, `/fraud`, `/crisis`, `/alerts`, `/responses`).

---

## Technology Stack

- **Framework**: FastAPI (async / ASGI)
- **Language**: Python 3.12+
- **Validation**: Pydantic v2
- **ORM & Migrations**: SQLAlchemy 2.0 (asyncio) & Alembic
- **Database**: PostgreSQL (production) / aiosqlite (local development & testing)
- **Security**: Argon2id password hashing, PyJWT (HMAC-SHA256)
- **Background Tasks**: Celery with Redis broker
- **HTTP Client**: httpx (async)
- **Testing**: pytest, pytest-asyncio, httpx ASGI transport
- **Linting & Formatting**: Ruff (100% compliant)
- **Containerization**: Docker, Docker Compose

---

## Directory Layout

```
backend/
├── app/
│   ├── main.py                  # Application factory, CORS, exception handlers
│   ├── api/
│   │   └── v1/
│   │       ├── router.py        # Master router aggregating all domain endpoints
│   │       ├── auth.py          # Authentication (/auth/register, /auth/login, /auth/me)
│   │       ├── businesses.py    # Business management (/business, /businesses)
│   │       ├── keywords.py      # Brand keywords (/keywords)
│   │       ├── mentions.py      # Mentions & reviews (/mentions, /reviews)
│   │       ├── sentiment.py     # Sentiment & aspect analysis (/sentiment, /analytics/aspects)
│   │       ├── fraud.py         # Explainable fraud detection (/fraud)
│   │       ├── reputation.py    # Isolated reputation scoring (/reputation)
│   │       ├── dashboard.py     # Aggregated analytics (/dashboard, /analytics)
│   │       ├── crisis.py        # Crisis monitoring & alerts (/crisis)
│   │       ├── alerts.py        # System alerts (/alerts)
│   │       └── ai_response.py   # AI response studio (/responses, /ai/responses)
│   │
│   ├── core/
│   │   ├── config.py            # Pydantic BaseSettings environment configuration
│   │   ├── database.py          # Async engine, sessionmaker, and Base
│   │   ├── security.py          # Argon2 hashing & JWT lifecycle
│   │   ├── exceptions.py        # Custom domain exceptions & global handlers
│   │   ├── logging.py           # Structured logging configuration
│   │   └── dependencies.py      # JWT Bearer, RBAC, and get_current_user dependencies
│   │
│   ├── models/                  # SQLAlchemy ORM models
│   ├── schemas/                 # Pydantic v2 request & response schemas
│   ├── repositories/            # Data access layer with pagination & filtering
│   ├── services/                # Pure business logic & isolated scoring algorithms
│   ├── integrations/            # Platform connectors (Mock, Google, Reddit, Twitter)
│   ├── ai/                      # AI providers (MockAIProvider, GeminiAIProvider)
│   └── workers/                 # Celery app and asynchronous background tasks
│
├── migrations/                  # Alembic migration scripts and versions
├── tests/                       # 19 comprehensive pytest integration tests
├── scripts/
│   └── seed.py                  # Deterministic database seeding script
├── Dockerfile                   # Production container definition
├── docker-compose.yml           # PostgreSQL, Redis, Backend, and Celery Worker
├── requirements.txt             # Locked dependencies
├── .env.example                 # Template environment variables
├── alembic.ini                  # Alembic migration configuration
├── pyproject.toml               # Ruff and tool configurations
├── ARCHITECTURE.md              # Detailed technical architecture document
└── API_CONTRACT.md              # Detailed API contract cross-referenced with Flutter
```

---

## Quick Start & Setup

### 1. Prerequisites
- Python 3.12+
- Git

### 2. Virtual Environment & Dependencies
```bash
cd backend
python -m venv .venv

# Activate virtual environment:
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default values connect to a local SQLite database (`sqlite+aiosqlite:///./reputex.db`) with mock providers enabled.

### 4. Database Migrations
Run Alembic to apply all database tables:
```bash
alembic upgrade head
```

### 5. Seed Demo Data
Populate realistic, populated intelligence data for the demo business (**Spice Symphony**):
```bash
python scripts/seed.py
```
**Demo Login Credentials**:
- **Email**: `adira@spicesymphony.com`
- **Password**: `Password123!`

### 6. Start the Backend Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Interactive Swagger API documentation is available at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Schema**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## Running Background Workers (Celery & Redis)

Start Celery worker in a separate terminal:
```bash
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

---

## Running with Docker Compose

To start the full production stack (FastAPI, PostgreSQL 16, Redis 7, and Celery Worker):
```bash
docker compose up --build
```

---

## Testing & Quality Assurance

Run the automated test suite:
```bash
# Run all 19 tests with verbose output
pytest -v

# Run linter checks
ruff check .

# Check code formatting
ruff format --check .

# Validate database migrations
alembic check
```

---

## Connecting the Flutter Mobile Application

1. Open `lib/core/constants/api_constants.dart` in the Flutter project.
2. Toggle `useMockApi` to `false`:
   ```dart
   static const bool useMockApi = false;
   ```
3. Ensure `baseUrl` matches your environment:
   - **Android Emulator**: `http://10.0.2.2:8000/api`
   - **iOS Simulator**: `http://127.0.0.1:8000/api`
   - **Physical Device**: `http://<YOUR_LOCAL_IP>:8000/api`
4. Login using `adira@spicesymphony.com` / `Password123!` to view live metrics!
