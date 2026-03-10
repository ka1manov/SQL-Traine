# CLAUDE.md

## Analysis Rules
- Analyze ONLY what is explicitly present in provided data
- Do NOT infer, assume, or extrapolate beyond what is stated
- If something is unclear or missing — say "insufficient data"
- Every claim must be traceable to the provided input
- Prohibited phrases: "likely", "probably", "typically" (unless sourced from input)
- Format findings as: CONFIRMED / UNCERTAIN / ABSENT

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SQL Trainer — an interactive SQL learning platform for interview preparation. FastAPI + PostgreSQL backend, React + TypeScript + Vite frontend, all orchestrated with Docker Compose.

## Commands

### Full Stack (Docker Compose)
```bash
docker compose up                    # Start all services (db, backend, frontend)
docker compose restart backend       # Restart backend after Python changes
docker compose restart frontend      # Restart frontend after React changes
docker compose down                  # Stop everything
```

### Frontend Only
```bash
cd frontend
npm install
npm run dev                          # Dev server on http://localhost:5173
npm run build                        # Production build
npx tsc --noEmit                     # Type-check without emitting
```

### Backend Only
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Verify Changes
```bash
# TypeScript check
cd frontend && npx tsc --noEmit
# Production build
cd frontend && npx vite build
# API smoke test
curl -s http://localhost:8000/api/health
curl -s http://localhost:8000/api/learning-paths | python3 -m json.tool | head -20
```

No test suite exists; verify manually via type checks, builds, and API calls.

## Architecture

### Backend (FastAPI, Python 3.12)
```
backend/
├── main.py              # App init, lifespan (sandbox cleanup), CORS, router registration
├── routers/             # One file per domain: tasks.py, execute.py, progress.py, mock.py, auth.py, etc.
├── models/schemas.py    # Pydantic request/response models
├── services/
│   ├── sandbox.py       # SQL execution engine: per-session schema isolation, keyword validation, 5s timeout
│   ├── auth.py          # JWT (HS256) token creation/decode, user CRUD in app_users table
│   └── diff.py          # Row-by-row result comparison (match_pct, missing/extra rows, order check)
├── data/                # Hard-coded content as Python dataclasses (not in DB)
│   ├── tasks.py         # 35+ practice tasks with solutions
│   ├── learning_paths.py # 6 paths, 16 steps with theory/examples/quiz/tips
│   ├── flashcards.py    # Spaced-repetition flashcards
│   └── assignments.py   # Multi-step take-home projects
└── db/
    ├── connection.py    # asyncpg pool singleton
    └── init.sql         # 11 public tables + app tables + seed data
```

**Sandbox system**: Each user session gets a PostgreSQL schema (`sandbox_<session_id>`) with cloned tables for safe read/write isolation. Destructive keywords (DROP, TRUNCATE, etc.) are blocked before execution. Schemas older than 24h are cleaned up on startup.

**Data layer**: Tasks, flashcards, learning paths, and assignments are Python dataclasses in `backend/data/`, serialized with `dataclasses.asdict()`. User progress, history, and auth are in PostgreSQL app tables.

### Frontend (React 18, TypeScript, Vite)
```
frontend/src/
├── App.tsx              # React Router with lazy-loaded pages
├── contexts/            # AuthContext, ProgressContext, ThemeContext (React Context API)
├── hooks/               # useProgress, useLocalStorage
├── utils/api.ts         # Axios client with auth interceptor, all API fetch functions
├── types/index.ts       # TypeScript interfaces mirroring backend Pydantic models
├── components/          # Reusable: SQLEditor (Monaco), ResultTable, DiffView, Layout, Charts, etc.
└── pages/               # 11 page components: Sandbox, Tasks, Learn, Flashcards, MockInterview, etc.
```

**State**: Auth + progress + theme via React Context. Pages are lazy-loaded with Suspense. Axios interceptor auto-attaches JWT Bearer token.

**Styling**: Tailwind CSS with class-based dark mode. Custom palette: `dark-bg`, `dark-card`, `dark-surface`, `dark-border`, `accent-blue/green/yellow/red/purple`. Components use `dark:bg-dark-card bg-gray-50` pattern for dual-theme support.

### API Proxy
Vite dev server proxies `/api` → `http://backend:8000` (Docker) or `http://localhost:8000` (local).

## Key Conventions

- **Backend routers** are async, registered in `main.py`, prefixed with `/api`
- **Frontend types** in `types/index.ts` must stay in sync with backend Pydantic models and dataclasses
- **Data content** (tasks, learning paths) lives in `backend/data/` as dataclasses — use `dataclasses.asdict()` for API serialization
- **Dark/light theme**: every component needs both `dark:` and light Tailwind classes
- **Backend runs in Docker** with volume mount — code changes are live but require `docker compose restart backend` (no hot-reload without `--reload` flag in Dockerfile's uvicorn)
- **Frontend in Docker** uses Vite dev server with HMR via volume mount
- **Database**: PostgreSQL 16, credentials `postgres:postgres`, database `sql_trainer`
- **Environment**: `backend/.env` has `DATABASE_URL` and `JWT_SECRET`

## Database

11 public tables (employees, departments, customers, products, orders, invoices, salaries_log, subscriptions, streams, bookings, ab_tests/clickstream) plus app tables (app_users, user_progress, query_history, bookmarks, flashcard_progress, streaks). Schema defined in `backend/db/init.sql`.
