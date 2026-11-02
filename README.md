# ⚡ DevPulse

> **Decoupled full-stack developer telemetry and system observability platform engineered with Python (FastAPI) and React (TypeScript + Tailwind CSS).**

DevPulse is an open-source, high-performance developer observability platform designed for real-time local environment monitoring and workflow event instrumentation. It provides a lightweight, asynchronous architectural foundation for tracking hardware utilization and developer lifecycle events with zero personal data collection, zero AI/ML training infrastructure, or external cloud dependencies.

---

## 🔬 Technical Overview & Architecture

### Backend Architecture (FastAPI & Python 3.12)
- **Asynchronous ASGI Runtime**: Built on FastAPI and Uvicorn running an asynchronous event loop (`asyncio`) with `@asynccontextmanager` application lifespan management.
- **Strict Data Contracts**: Request and response serializations are enforced strictly via **Pydantic v2** schemas (`BaseModel`, `Field`) with centralized 12-factor configuration through **pydantic-settings**.
- **OS-Level Telemetry Engine**: Interfaces with kernel performance counters via `psutil` to sample hardware resource utilization (CPU multi-core percentage, memory footprint in MB, disk saturation) with graceful fallback simulation.
- **Prometheus Observability (`/metrics`)**: Exposes native Prometheus text exposition metrics (Gauges and Counters) for ingestion by Prometheus server and Grafana dashboards.
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
- **Cloud-Native Deployment**: Production Kubernetes manifests (`deploy/k8s/`) with auto-discovery annotations and Terraform IaC (`deploy/terraform/`) for AWS ECS & CloudWatch monitoring.
- **Automated CI/CD Pipeline**: GitHub Actions workflow (`.github/workflows/ci.yml`) automating backend testing, frontend builds, and Docker validation.

---

## 🚀 Key Technical Specifications

| Component | Technical Implementation & Specifications |
|---|---|
| **Runtime & Language** | Python 3.12 (Asynchronous ASGI via `asyncio`), TypeScript 5.6 (ES2020 target) |
| **API Framework** | FastAPI 0.115+ with modular APIRouter versioning (`/api/v1`) and OpenAPI 3.1 schema auto-generation |
| **Data Validation** | Pydantic v2 schemas (`BaseModel`, `Field`, `@field_validator`) guaranteeing type parity with frontend |
| **Observability & Metrics** | Native `/metrics` endpoint formatted for Prometheus & Grafana scrapers (RFC 0.0.4) |
| **Infrastructure as Code** | Terraform (`deploy/terraform/main.tf`) provisioning AWS ECS & CloudWatch alarms |
| **Container Orchestration**| Kubernetes Deployment & Service manifests (`deploy/k8s/`) with Liveness/Readiness probes |
| **CI/CD Automation** | GitHub Actions multi-job workflow (`.github/workflows/ci.yml`) |
| **Data & Privacy Guarantee** | Strictly anonymous, local machine telemetry; zero PII collection, zero external tracking pixels |
| **Test Coverage** | `pytest` automated suite testing health checks, pulse endpoints, and Prometheus metrics |

---

## 📁 Project Architecture

```
DevPulse/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD pipeline
├── deploy/                      # Cloud Engineering & Deployment
│   ├── k8s/
│   │   └── deployment.yaml      # Kubernetes Deployment & Service manifests
│   └── terraform/
│       └── main.tf              # AWS ECS & CloudWatch Terraform IaC
├── dev.py                       # Unified developer CLI manager
├── docker-compose.yml           # Container orchestration
├── .gitignore                   # Multi-stack gitignore
├── README.md                    # Project documentation
│
├── backend/                     # Python FastAPI Application
│   ├── app/
│   │   ├── main.py              # FastAPI app instance, CORS, lifespan, /metrics
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
- **Prometheus Metrics**: `http://127.0.0.1:8000/metrics`
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

All endpoints are versioned under `/api/v1` (with `/metrics` exposed at root for scraper standard compatibility):

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | DevPulse embedded developer dashboard |
| `GET` | `/metrics` | Standard Prometheus exposition format for Prometheus & Grafana |
| `GET` | `/docs` | Interactive Swagger OpenAPI documentation |
| `GET` | `/redoc` | Interactive ReDoc API documentation |
| `GET` | `/api/v1/health` | Service health status, uptime, and runtime info |
| `GET` | `/api/v1/metrics/pulse` | Full telemetry snapshot (system metrics + events) |
| `GET` | `/api/v1/metrics/system` | Real-time hardware telemetry (CPU, RAM, Disk) |
| `GET` | `/api/v1/metrics/events` | List recorded activity pulse events |
| `POST`| `/api/v1/metrics/events` | Record a new pulse event |

### Sample Request & Response

#### 1. Prometheus Metrics Scrape
```bash
curl http://127.0.0.1:8000/metrics
```
```
# HELP devpulse_cpu_percent Current CPU utilization percentage
# TYPE devpulse_cpu_percent gauge
devpulse_cpu_percent 14.2
# HELP devpulse_memory_percent Current RAM utilization percentage
# TYPE devpulse_memory_percent gauge
devpulse_memory_percent 42.1
# HELP devpulse_uptime_seconds Application uptime in seconds
# TYPE devpulse_uptime_seconds counter
devpulse_uptime_seconds 42.15
# HELP devpulse_events_total Total developer pulse events recorded
# TYPE devpulse_events_total counter
devpulse_events_total 3
```

#### 2. Service Health Check
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

---

## ☁️ Cloud Engineering & DevOps Architecture

DevPulse is architected with enterprise-grade cloud-native patterns matching modern Site Reliability Engineering (SRE) and DevOps practices:

### 1. Prometheus & Grafana Native Observability (`GET /metrics`)
- Exposes real-time system metrics directly in standard **Prometheus exposition format** (RFC 0.0.4) at `http://localhost:8000/metrics`.
- Gauges: `devpulse_cpu_percent`, `devpulse_memory_percent`, `devpulse_memory_used_mb`, `devpulse_disk_percent`.
- Counters: `devpulse_uptime_seconds`, `devpulse_events_total`.
- Scrapeable directly by Prometheus servers and visualizable via pre-configured Grafana dashboards.

### 2. Kubernetes Deployment & Pod Autoscaling (`deploy/k8s/`)
- Production-ready `deployment.yaml` and `service.yaml` manifests.
- Standard cloud-native annotations for Prometheus auto-discovery:
  ```yaml
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8000"
    prometheus.io/path: "/metrics"
  ```
- Dual health probes configured:
  - **Liveness Probe**: `GET /api/v1/health` (container self-healing)
  - **Readiness Probe**: `GET /api/v1/health` (traffic ingress routing)

### 3. Infrastructure as Code (Terraform) (`deploy/terraform/`)
- Modular **Terraform (`main.tf`)** targeting AWS ECS and CloudWatch infrastructure.
- Automated CloudWatch Metric Alarm for CPU saturation breaches (>80%).
- Declarative infrastructure management compliant with HashiCorp best practices.

### 4. Automated CI/CD Pipeline (`.github/workflows/ci.yml`)
- Multi-job GitHub Actions workflow triggering on push and pull requests:
  - **Backend Job**: Sets up Python 3.12, caches dependencies, runs `pytest` suite.
  - **Frontend Job**: Sets up Node.js 20, runs TypeScript compiler checks (`tsc`), and bundles Vite SPA.
  - **Docker Validation**: Multi-stage build check ensuring zero image regressions.

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

## 🗺️ Roadmap & Future Implementation Scope

The following **5 features** are scheduled for future implementation, each designed to strictly adhere to our core engineering principles (**Zero AI/ML model training, zero security exploit tooling, and zero personal data collection**):

1. **Real-Time WebSocket Telemetry Streaming (`/api/v1/ws/pulse`)**
   - Direct bidirectional WebSocket connection between FastAPI and React, providing sub-millisecond hardware metric streams without HTTP polling overhead.
   - *Strict Rule Verification*: Pure network transport protocol; transmits only anonymous hardware counters (`cpu_percent`, `memory_mb`).

2. **Local Git Workspace Health Inspector (`/api/v1/git/status`)**
   - Real-time local repository hygiene monitor displaying current branch, head commit SHA, unstaged file counters, and stash queue depth.
   - *Strict Rule Verification*: Local read-only workspace inspection; completely strips author identities, emails, and commit signatures.

3. **Configurable Saturation Threshold Alerts & Outbound Webhook Dispatcher (`/api/v1/alerts`)**
   - Developer-defined resource saturation thresholds (e.g. `CPU > 85% for 10s`) that trigger in-app visual warnings and optional local JSON webhook events.
   - *Strict Rule Verification*: Deterministic numerical threshold comparisons; zero attack or exploit logic.

4. **Process Tree Resource Monitor (`/api/v1/system/processes`)**
   - Non-privileged OS process table inspector tracking top resource-consuming binary processes (e.g. `node.exe`, `python.exe`, `docker.exe`).
   - *Strict Rule Verification*: Standard OS task enumeration; captures only executable binary names and CPU/RAM percentages with zero access to user keystrokes or account data.

5. **Local Service Latency & Microservice Health Prober (`/api/v1/benchmarks/probe`)**
   - Developer diagnostic prober measuring HTTP response latency percentiles (P50, P95, P99) across internal development microservices.
   - *Strict Rule Verification*: Strictly localhost-whitelisted diagnostic probe; zero external vulnerability scanning, brute-forcing, or penetration testing.

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
