# ⚡ DevPulse

> **Production-ready, modular developer telemetry & dashboard starter template built with Python (FastAPI) and React (TypeScript + Tailwind CSS).**

DevPulse provides a clean, extensible architectural foundation for building developer tools, system health monitors, engineering telemetry dashboards, or modern full-stack web applications.

---

## 🚀 Key Features

- **⚡ FastAPI Backend**: Clean architecture with lifespan events, centralized configuration via `pydantic-settings`, structured logging, and automated OpenAPI (Swagger / ReDoc) documentation.
- **🎨 Modern React Dashboard**: Built with Vite, React 18, TypeScript, Tailwind CSS, and Lucide icons.
- **🖥️ Zero-Setup Embedded UI**: FastAPI serves a dark-themed responsive dashboard at `http://localhost:8000` out of the box, even before compiling the frontend SPA.
- **🔄 Real-time Pulse Telemetry**: System telemetry (CPU, RAM, Disk) and live activity stream polling via clean REST endpoints.
- **🛠️ Unified CLI Runner (`dev.py`)**: One-command dependency setup, isolated running, concurrent dev execution, and testing.
- **🐳 Docker Ready**: Full multi-container `docker-compose.yml` for isolated containerized environments.
- **🧪 Automated Tests**: Preconfigured `pytest` suite with `httpx` / FastAPI `TestClient`.

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

## 🧩 How to Extend This Starter

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
