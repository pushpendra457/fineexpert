# FineExpert

Production-grade AI SaaS platform for intelligent document analysis, Retrieval-Augmented Generation (RAG), and agentic workflows.

## Architecture

- **Frontend:** Vue 3, Vite, TypeScript, Pinia, Tailwind CSS, TanStack Query
- **Backend:** FastAPI, Python 3.12, SQLAlchemy 2.0 (async), Alembic, Pydantic v2
- **AI & RAG:** LangChain, LangGraph, Qdrant, sentence-transformers
- **Workers & Cache:** Celery, Redis
- **Database:** PostgreSQL (Neon)
- **Deployment:** Cloudflare Pages (Frontend), Render (Backend)

For full architectural blueprint and implementation plan, see [phase1.md](phase1.md).

## Quick Start with Docker

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
docker compose up --build
```

## Team Workflow

This repository is built for multi-developer collaboration:
- Developer 1: Backend, Database, Auth, Docker, CI/CD
- Developer 2: Frontend, UI/UX, Reusable Components, Pages
- Developer 3: AI, LangChain, LangGraph, RAG Pipeline, Embeddings

Direct pushes to \`main\` are blocked. All changes must go through feature branches and pull requests.
