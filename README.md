# ⚡ DevPulse

> **Decoupled full-stack developer telemetry and system observability platform engineered with Python (FastAPI) and React (TypeScript + Tailwind CSS).**

DevPulse is an open-source, high-performance developer observability platform designed for real-time local environment monitoring and workflow event instrumentation. It provides a lightweight, asynchronous architectural foundation for tracking hardware utilization and developer lifecycle events with zero personal data collection, zero AI/ML training infrastructure, or external cloud dependencies.

---

## 🔬 Technical Overview & Architecture

### Backend Architecture (FastAPI & Python 3.12)
- **Asynchronous ASGI Runtime**: Built on FastAPI and Uvicorn running an asynchronous event loop (`asyncio`) with `@asynccontextmanager` application lifespan management.
- **Strict Data Contracts**: Request and response serializations are enforced strictly via **Pydantic v2** schemas (`BaseModel`, `Field`) with centralized 12-factor configuration through **pydantic-settings**.
- **OS-Level Telemetry Engine**: Interfaces with kernel performance counters via `psutil` to sample hardware resource utilization (CPU multi-core percentage, memory footprint in MB, disk saturation) with graceful fallback simulation.
- **In-Memory Event Bus**: Implements a thread-safe circular buffer (`threading.Lock`) for ephemeral, low-latency developer event ingestion and dispatch.
- **Zero-Setup Embedded UI**: FastAPI streams an interactive HTML5/Tailwind dashboard directly from the root `/` endpoint over ASGI without requiring an initial frontend compile step.

### Frontend Architecture (React 18 & TypeScript)
- **Strict Typing**: Fully typed client layer matching backend Pydantic models across all telemetry payloads and event contracts.
- **Reactive State & Polling**: Resilient polling routines (`useCallback`, `useEffect`) synchronized with backend metrics endpoints.
- **Vite Bundler & Reverse Proxy**: Sub-millisecond HMR (Hot Module Replacement) with automated reverse-proxying (`/api` -> `127.0.0.1:8000`) eliminating CORS overhead during local development.
- **Modular Component Design**: Clean atomic components (`Header`, `MetricCard`, `PulseActivity`, `QuickActions`) styled with Tailwind CSS utility classes and Lucide vector iconography.

### DevOps & Engineering Tooling
- **Unified CLI Supervisor (`dev.py`)**: A cross-platform runner managing Python virtual environment isolation, dependency trees, concurrent multi-process orchestration, and test execution.
- **Containerization**: Multi-container Docker orchestration (`docker-compose.yml`) separating backend (`python:3.12-slim`) and frontend (`node:20-alpine`) execution contexts.
- **Automated Test Harness**: Integration and unit testing suite powered by `pytest` and FastAPI `TestClient` / `httpx`.

---

## 🚀 Key Technical Specifications

| Component | Technical Implementation & Specifications |
|---|---|
| **Runtime & Language** | Python 3.12 (Asynchronous ASGI via `asyncio`), TypeScript 5.6 (ES2020 target) |
| **API Framework** | FastAPI 0.115+ with modular APIRouter versioning (`/api/v1`) and OpenAPI 3.1 schema auto-generation |
| **Data Validation** | Pydantic v2 schemas (`BaseModel`, `Field`, `@field_validator`) guaranteeing type parity with frontend |
| **Telemetry Engine** | Non-blocking OS-level resource sampling via `psutil` with simulated fallback metrics |
| **Client Layer** | React 18 SPA built with Vite, Tailwind CSS utility styling, and Lucide vector icons |
| **Data & Privacy Guarantee** | Strictly anonymous, local machine telemetry; zero PII collection, zero external tracking pixels |
| **Test Coverage** | `pytest` automated suite testing health checks, pulse endpoints, and event CRUD routes |

---

## 📁 Project Architecture

```
DevPulse/
├── dev.py                       # Unified developer CLI manager
├── docker-compose.yml           # Container orchestration
├── .gitignore                   # Multi-stack gitignore
├── README.md                    # Project documentation
│
├── backend/                     # Python FastAPI Application
│   ├── app/
│   │   ├── main.py              # FastAPI app instance, CORS, lifespan, root UI
│   │   ├── api/
│   │   │   ├── router.py        # Central API router aggregator
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   │           ├── health.py    # Health check (/api/v1/health)
│   │   │           └── metrics.py   # Pulse telemetry (/api/v1/metrics/*)
│   │   ├── core/
│   │   │   ├── config.py        # Pydantic BaseSettings (.env loader)
│   │   │   └── logger.py        # Structured logging setup
│   │   ├── schemas/             # Pydantic request/response models
│   │   │   ├── health.py
│   │   │   └── metrics.py
│   │   ├── services/            # Business logic & telemetry services
│   │   │   └── pulse_service.py
│   │   └── templates/
│   │       └── dashboard.html   # Zero-setup embedded dashboard
│   ├── tests/                   # Pytest test suite
│   │   ├── conftest.py
│   │   ├── test_health.py
│   │   └── test_metrics.py
│   ├── requirements.txt         # Backend Python dependencies
│   ├── pyproject.toml           # Packaging & linting configuration
│   └── .env.example             # Environment configuration template
│
└── frontend/                    # Vite + React + TypeScript SPA
    ├── src/
    │   ├── components/          # Modular UI components
    │   │   ├── Header.tsx       # App header with live status
    │   │   ├── MetricCard.tsx   # Visual KPI card with progress bars
    │   │   ├── PulseActivity.tsx# Live event feed
    │   │   └── QuickActions.tsx # Event dispatch form
    │   ├── services/
    │   │   └── api.ts           # Typed API client connected to backend
    │   ├── types/
    │   │   └── api.ts           # TypeScript models matching backend schemas
    │   ├── App.tsx              # Main dashboard view
    │   ├── main.tsx             # React DOM entrypoint
    │   └── index.css            # Tailwind directives
    ├── index.html               # Frontend HTML root
    ├── vite.config.ts           # Vite bundler & API reverse proxy config
    ├── tailwind.config.js       # Tailwind CSS theme configuration
    └── package.json             # Frontend dependencies and scripts
```

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python 3.10+** (Python 3.12 recommended)
- **Node.js 18+ & npm** (optional if running embedded backend dashboard only)

### 2. Automated Setup (Recommended)
Run the setup command to initialize the virtual environment and install all dependencies:

```bash
python dev.py setup
```

### 3. Running DevPulse

#### Option A: Full-Stack Mode (Both Backend & Frontend)
```bash
python dev.py dev
```
- **Backend API**: `http://127.0.0.1:8000`
- **Swagger Documentation**: `http://127.0.0.1:8000/docs`
- **Vite React SPA**: `http://localhost:5173`

#### Option B: Backend Only (with Embedded Dashboard)
```bash
python dev.py backend
```
Visit `http://127.0.0.1:8000` in your browser to immediately interact with the embedded dashboard and live metrics.

#### Option C: Frontend Only
```bash
python dev.py frontend
```

---

## 🔌 API Endpoints Reference

All endpoints are versioned under `/api/v1`:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | DevPulse embedded developer dashboard |
| `GET` | `/docs` | Interactive Swagger OpenAPI documentation |
| `GET` | `/redoc` | Interactive ReDoc API documentation |
| `GET` | `/api/v1/health` | Service health status, uptime, and runtime info |
| `GET` | `/api/v1/metrics/pulse` | Full telemetry snapshot (system metrics + events) |
| `GET` | `/api/v1/metrics/system` | Real-time hardware telemetry (CPU, RAM, Disk) |
| `GET` | `/api/v1/metrics/events` | List recorded activity pulse events |
| `POST`| `/api/v1/metrics/events` | Record a new pulse event |

### Sample Request & Response

#### 1. Service Health Check
```bash
curl http://127.0.0.1:8000/api/v1/health
```
```json
{
  "status": "ok",
  "app_name": "DevPulse",
  "version": "0.1.0",
  "environment": "development",
  "uptime_seconds": 42.15,
  "timestamp": "2026-11-02T08:00:00Z",
  "python_version": "3.12.10"
}
```

#### 2. Create Pulse Event
```bash
curl -X POST http://127.0.0.1:8000/api/v1/metrics/events \
  -H "Content-Type: application/json" \
  -d '{"title": "Deploy to Staging", "category": "deploy", "status": "success", "details": "Build #42 passed"}'
```

---

## 🧪 Testing

Run backend automated test suite:
```bash
python dev.py test
```
Or directly using pytest inside `backend/`:
```bash
cd backend
pytest
```

---

## 🐳 Docker Deployment

To launch the full stack with Docker Compose:

```bash
docker-compose up --build
```

---

## 🧩 How to Extend This Platform

### Adding a New Backend Endpoint
1. Define your Pydantic schemas in `backend/app/schemas/`.
2. Add your business logic in `backend/app/services/`.
3. Create endpoint handlers in `backend/app/api/v1/endpoints/`.
4. Register the router in `backend/app/api/router.py`.

### Adding a New Frontend Feature
1. Define the TypeScript interfaces in `frontend/src/types/api.ts`.
2. Add corresponding fetch functions to `frontend/src/services/api.ts`.
3. Create modular React components in `frontend/src/components/`.

---

## 📄 License
This project is dual-licensed under both the **MIT License** and the **Apache License (Version 2.0)**:

- [MIT License](LICENSE-MIT)
- [Apache License 2.0](LICENSE-APACHE)

You may choose to use this project under the terms of either license at your option. See [LICENSE](LICENSE) for details.
