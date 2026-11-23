# 🏠 Homingo — Master Project Plan & Blueprint

> **Purpose:** This document is the single source of truth for the entire project. If work is interrupted at any point, any developer or AI agent can pick up from here and continue.

> [!IMPORTANT]
> A workflow with 8 parallel agents is currently scaffolding the project in `/home/pushpendra/homingo`. This plan describes **every file, every module, every decision** so work can resume from any point.

---

## 📋 What We're Building

**Homingo** is a production-grade AI SaaS application that lets users:

1. **Upload documents** (PDFs) for processing
2. **Chat with AI** using those documents as context (RAG)
3. **Run intelligent workflows** via an AI agent (LangGraph)
4. **Manage their account**, documents, conversations, and settings

It's designed for 3 developers working simultaneously with feature branches, PR-based workflow, CI/CD, and auto-deployment.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Vue 3)                     │
│   Cloudflare Pages  │  Vite  │  Tailwind  │ TypeScript  │
└──────────────────────────┬──────────────────────────────┘
                           │ HTTPS / API calls
┌──────────────────────────▼──────────────────────────────┐
│                   BACKEND (FastAPI)                      │
│                      Render.com                          │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐             │
│  │ API Layer│→ │ Service  │→ │Repository │→ PostgreSQL  │
│  │ (Routes) │  │ (Logic)  │  │ (Data)    │  (Neon)      │
│  └──────────┘  └──────────┘  └───────────┘             │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐             │
│  │   Auth   │  │  AI/RAG  │  │  Workers  │→ Redis      │
│  │  (JWT)   │  │(LangChain│  │ (Celery)  │  (Upstash)  │
│  └──────────┘  └──────────┘  └───────────┘             │
│                     │                                    │
│            ┌────────▼────────┐                          │
│            │  Vector Store   │                          │
│            │  (Qdrant Cloud) │                          │
│            └─────────────────┘                          │
└─────────────────────────────────────────────────────────┘
```

**Clean Architecture Layers:**
- **API Layer** → HTTP endpoints, request validation, response formatting
- **Service Layer** → Business logic, orchestration, no DB knowledge
- **Repository Layer** → Data access, SQL queries, no business logic
- **AI Layer** → LLM providers, RAG, agents — isolated from web layer

---

## 📁 Complete File Manifest

Every file that should exist in the project. Check (✅) means generated, (❌) means missing/needs creation.

### Root Files

| File | Purpose |
|------|---------|
| `.gitignore` | Python, Node, Docker, IDE, env exclusions |
| `LICENSE` | MIT License, 2024, Homingo Team |
| `README.md` | Professional project README (detailed below) |
| `CONTRIBUTING.md` | Git workflow, PR process, dev setup |
| `CODE_OF_CONDUCT.md` | Contributor Covenant v2.1 |
| `SECURITY.md` | Security policy, responsible disclosure |
| `docker-compose.yml` | All 6 services orchestrated |
| `render.yaml` | Render deployment blueprint |

### Docker (`docker/`)

| File | Purpose |
|------|---------|
| `docker/Dockerfile.frontend` | Multi-stage: node:20-alpine build → nginx:alpine serve |
| `docker/Dockerfile.backend` | python:3.12-slim, gunicorn+uvicorn |
| `docker/nginx.conf` | SPA routing, /api proxy, gzip, security headers |

### GitHub (`.github/`)

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | PR checks: ruff, black, pytest, npm lint, test, build |
| `.github/workflows/deploy.yml` | Auto-deploy on main merge: Cloudflare Pages + Render |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR description, type, checklist |

### Scripts (`scripts/`)

| File | Purpose |
|------|---------|
| `scripts/setup.sh` | One-command project setup (docker compose) |
| `scripts/reset-db.sh` | Drop/recreate DB, run migrations |

### Docs (`docs/`)

| File | Purpose |
|------|---------|
| `docs/architecture.md` | System architecture, diagrams, data flow |
| `docs/api.md` | API endpoint reference |
| `docs/deployment.md` | Deployment guide for all services |
| `docs/developer-onboarding.md` | New developer setup guide |

---

### Backend (`backend/`)

#### Config & Entry

| File | Purpose |
|------|---------|
| `backend/requirements.txt` | All Python dependencies |
| `backend/.env.example` | All env vars with descriptions |
| `backend/pyproject.toml` | black, ruff, isort, mypy, pytest config |
| `backend/alembic.ini` | Alembic config |
| `backend/alembic/env.py` | Async Alembic environment |
| `backend/alembic/versions/.gitkeep` | Migration versions directory |
| `backend/app/__init__.py` | Package init |
| `backend/app/main.py` | FastAPI app factory (CORS, rate limit, Sentry, routers, lifespan) |

#### Config (`backend/app/config/`)

| File | Purpose |
|------|---------|
| `config/__init__.py` | — |
| `config/settings.py` | Pydantic BaseSettings — all env vars, validators |

#### Database (`backend/app/db/`)

| File | Purpose |
|------|---------|
| `db/__init__.py` | — |
| `db/base.py` | AsyncEngine, async_sessionmaker, Base model |
| `db/session.py` | `get_db` FastAPI dependency |

#### Models (`backend/app/models/`)

| File | Fields |
|------|--------|
| `models/__init__.py` | Import all |
| `models/user.py` | id(UUID), email, hashed_password, full_name, avatar_url, role(admin/user), is_active, is_verified, google_id, created_at, updated_at |
| `models/document.py` | id(UUID), user_id(FK), filename, original_filename, file_url, file_size, mime_type, page_count, status(pending/processing/completed/failed), error_message, timestamps |
| `models/conversation.py` | id(UUID), user_id(FK), title, model_used, timestamps |
| `models/message.py` | id(UUID), conversation_id(FK), role(user/assistant/system), content, citations(JSON), tokens_used, created_at |
| `models/document_chunk.py` | id(UUID), document_id(FK), chunk_index, content, metadata_(JSON), embedding_id, created_at |
| `models/notification.py` | id(UUID), user_id(FK), title, message, type(enum), is_read, created_at |

#### Schemas (`backend/app/schemas/`)

| File | Schemas |
|------|---------|
| `schemas/__init__.py` | — |
| `schemas/user.py` | UserCreate, UserUpdate, UserResponse, UserInDB |
| `schemas/auth.py` | Token, TokenPayload, LoginRequest, GoogleAuthRequest, RegisterRequest |
| `schemas/document.py` | DocumentCreate, DocumentResponse, DocumentListResponse |
| `schemas/conversation.py` | ConversationCreate, ConversationResponse, MessageCreate, MessageResponse, ChatRequest, ChatResponse |
| `schemas/common.py` | PaginatedResponse, HealthResponse, ErrorResponse, SuccessResponse |

#### Auth (`backend/app/auth/`)

| File | Purpose |
|------|---------|
| `auth/__init__.py` | — |
| `auth/jwt.py` | create_access_token, create_refresh_token, verify_token (python-jose) |
| `auth/password.py` | hash_password, verify_password (passlib bcrypt) |
| `auth/dependencies.py` | get_current_user, get_current_active_user, require_admin |
| `auth/google.py` | verify_google_token, get_google_user_info (httpx) |

#### Middleware (`backend/app/middleware/`)

| File | Purpose |
|------|---------|
| `middleware/__init__.py` | — |
| `middleware/logging.py` | Structured logging (structlog) — method, path, status, duration |
| `middleware/rate_limit.py` | slowapi — 100/min general, 20/min auth |

#### Repositories (`backend/app/repositories/`)

| File | Methods |
|------|---------|
| `repositories/__init__.py` | — |
| `repositories/base.py` | BaseRepository[T]: get_by_id, get_all(paginated), create, update, delete |
| `repositories/user_repository.py` | + get_by_email, get_by_google_id |
| `repositories/document_repository.py` | + get_by_user, get_with_chunks |
| `repositories/conversation_repository.py` | + get_by_user, get_with_messages |
| `repositories/notification_repository.py` | + get_unread_by_user, mark_as_read, mark_all_read |

#### Services (`backend/app/services/`)

| File | Methods |
|------|---------|
| `services/__init__.py` | — |
| `services/auth_service.py` | register, login, refresh_token, google_login, change_password |
| `services/user_service.py` | get_profile, update_profile, list_users(admin), deactivate_user(admin) |
| `services/document_service.py` | upload_document, get_documents, get_document, delete_document |
| `services/conversation_service.py` | create/get/delete conversation, add_message |
| `services/notification_service.py` | create/get/mark_read notifications |
| `services/chat_service.py` | process_chat_message (RAG → LLM → citations) |
| `services/admin_service.py` | get_dashboard_stats, get_all_users, get_system_health |

#### LLM Provider Abstraction (`backend/app/services/llm/`)

| File | Purpose |
|------|---------|
| `services/llm/__init__.py` | — |
| `services/llm/base.py` | Abstract LLMProvider: generate(), stream_generate(). LLMResponse model |
| `services/llm/openai_provider.py` | OpenAI via langchain-openai (gpt-4o, gpt-4o-mini) |
| `services/llm/gemini_provider.py` | Google Gemini via langchain-google-genai |
| `services/llm/factory.py` | LLMProviderFactory.get_provider(name) — config-driven switching |

#### API Routes (`backend/app/api/`)

| File | Endpoints |
|------|-----------|
| `api/__init__.py` | — |
| `api/router.py` | Main router including all v1 sub-routers |
| `api/deps.py` | Shared dependencies (get_settings, services) |
| `api/v1/__init__.py` | — |
| `api/v1/auth.py` | POST /register, /login, /refresh, /google-auth |
| `api/v1/users.py` | GET/PUT /me, GET /me/notifications |
| `api/v1/documents.py` | POST /upload, GET /, GET /{id}, DELETE /{id} |
| `api/v1/conversations.py` | POST /, GET /, GET /{id}, DELETE /{id} |
| `api/v1/chat.py` | POST /{conversation_id}/messages |
| `api/v1/admin.py` | GET /dashboard, GET /users, PUT /users/{id}/role |
| `api/v1/health.py` | GET /health |

#### Embeddings (`backend/app/embeddings/`)

| File | Purpose |
|------|---------|
| `embeddings/__init__.py` | — |
| `embeddings/embedding_service.py` | EmbeddingService: generate_embeddings() using sentence-transformers (BAAI/bge-small-en-v1.5, all-MiniLM-L6-v2 fallback) |

#### Vector Store (`backend/app/vectorstore/`)

| File | Purpose |
|------|---------|
| `vectorstore/__init__.py` | — |
| `vectorstore/base.py` | Abstract VectorStoreProvider: add_vectors, search, delete_by_document_id |
| `vectorstore/qdrant_store.py` | Qdrant Cloud implementation |
| `vectorstore/chroma_store.py` | ChromaDB for local dev |
| `vectorstore/factory.py` | Auto-select Qdrant (prod) or ChromaDB (dev) |

#### RAG Pipeline (`backend/app/rag/`)

| File | Purpose |
|------|---------|
| `rag/__init__.py` | — |
| `rag/document_processor.py` | extract_text (PyMuPDF→pypdf fallback), clean_text, chunk_text (RecursiveCharacterTextSplitter) |
| `rag/retriever.py` | RAGRetriever: embed query → vector search → return ranked chunks |
| `rag/chain.py` | RAGChain: build LangChain chain, generate_answer with citations |

#### Prompts (`backend/app/prompts/`)

| File | Contents |
|------|----------|
| `prompts/__init__.py` | — |
| `prompts/templates.py` | RAG_SYSTEM_PROMPT, CHAT_SYSTEM_PROMPT, AGENT_SYSTEM_PROMPT, SUMMARIZE_PROMPT |

#### LangGraph Agents (`backend/app/agents/`)

| File | Purpose |
|------|---------|
| `agents/__init__.py` | — |
| `agents/state.py` | AgentState TypedDict (messages, context, tools_output, plan, final_answer, metadata) |
| `agents/tools.py` | @tool functions: search_documents, summarize_document, web_search |
| `agents/nodes.py` | Graph nodes: reasoning, retrieval, tool, generation, planning |
| `agents/graph.py` | StateGraph: START→reasoning→(retrieval\|tool\|direct)→generation→END. MemorySaver. run_agent() |

#### Celery Workers (`backend/app/workers/` + `backend/app/tasks/`)

| File | Purpose |
|------|---------|
| `workers/__init__.py` | — |
| `workers/celery_app.py` | Celery config: Redis broker, task routes, beat schedule, autodiscover |
| `tasks/__init__.py` | — |
| `tasks/document_tasks.py` | process_document (full pipeline), generate_embeddings, delete_document_vectors |
| `tasks/notification_tasks.py` | send_email_notification, send_in_app_notification |
| `tasks/scheduled_tasks.py` | cleanup_expired_tokens, generate_daily_stats |

#### Utils (`backend/app/utils/`)

| File | Purpose |
|------|---------|
| `utils/__init__.py` | — |
| `utils/exceptions.py` | AppException, NotFoundException, UnauthorizedException, etc. + global handler |
| `utils/helpers.py` | generate_uuid, utc_now, paginate |
| `utils/logging.py` | structlog config (JSON in prod, pretty in dev) |

#### Tests (`backend/app/tests/`)

| File | Coverage |
|------|----------|
| `tests/__init__.py` | — |
| `tests/conftest.py` | Fixtures: async_client, test_db, test_user, auth_headers, admin_headers |
| `tests/test_auth.py` | 9 tests: register, login, refresh, protected routes |
| `tests/test_users.py` | 4 tests: get user, update profile, notifications |
| `tests/test_documents.py` | 8 tests: upload, list, get, delete, validation |
| `tests/test_conversations.py` | 5 tests: CRUD conversations |
| `tests/test_admin.py` | 4 tests: dashboard, users, role change, auth |
| `tests/test_health.py` | 2 tests: health check |
| `tests/test_rag.py` | 5 tests: processor, embeddings, retriever (mocked) |
| `tests/test_services/test_auth_service.py` | Unit tests with mocked repos |
| `tests/test_services/test_user_service.py` | Unit tests |
| `tests/test_services/test_chat_service.py` | Unit tests with mocked LLM/RAG |

---

### Frontend (`frontend/`)

#### Config Files

| File | Purpose |
|------|---------|
| `frontend/package.json` | Deps, scripts (dev, build, test, lint) |
| `frontend/vite.config.ts` | Vue plugin, @ alias, /api proxy, test config |
| `frontend/tsconfig.json` | Strict TS, paths |
| `frontend/tsconfig.node.json` | Node TS for vite config |
| `frontend/tailwind.config.js` | Custom colors (indigo/purple), plugins |
| `frontend/postcss.config.js` | tailwindcss + autoprefixer |
| `frontend/.eslintrc.cjs` | Vue 3 + TS rules |
| `frontend/.prettierrc` | No semi, single quotes |
| `frontend/.env.example` | VITE_API_URL, VITE_APP_NAME, etc. |
| `frontend/index.html` | Entry HTML with #app |

#### Entry (`frontend/src/`)

| File | Purpose |
|------|---------|
| `src/main.ts` | Create app, install Pinia, Router, VueQuery |
| `src/App.vue` | Root with RouterView + Suspense |
| `src/env.d.ts` | Vite/Vue type declarations |
| `src/styles/main.css` | Tailwind directives + global styles |

#### Router (`frontend/src/router/`)

| File | Routes |
|------|--------|
| `router/index.ts` | / (Landing), /about, /login, /register, /dashboard, /chat, /chat/:id, /documents, /profile, /settings, /admin, /admin/users, 404 catch-all. Auth guards. |

#### Stores (`frontend/src/stores/`)

| File | State |
|------|-------|
| `stores/auth.ts` | user, token, isAuthenticated. Actions: login, register, logout, googleLogin |
| `stores/chat.ts` | conversations, messages, isLoading. Actions: fetch, create, send, delete |
| `stores/document.ts` | documents, uploadProgress. Actions: fetch, upload, delete |
| `stores/notification.ts` | notifications, unreadCount. Actions: fetch, markRead |
| `stores/ui.ts` | sidebarOpen, theme, loading. Toast notifications |

#### Services (`frontend/src/services/`)

| File | API Calls |
|------|-----------|
| `services/api.ts` | Axios instance with JWT interceptors, 401 refresh |
| `services/auth.service.ts` | login, register, refreshToken, googleAuth |
| `services/user.service.ts` | getProfile, updateProfile |
| `services/document.service.ts` | upload(multipart), list, get, delete |
| `services/chat.service.ts` | conversations CRUD, sendMessage |
| `services/admin.service.ts` | dashboardStats, users, updateRole |

#### Types (`frontend/src/types/`)

| File | Interfaces |
|------|------------|
| `types/index.ts` | User, Document, Conversation, Message, Citation, Notification, PaginatedResponse, ApiError, LoginPayload, RegisterPayload |

#### Composables (`frontend/src/composables/`)

| File | Purpose |
|------|---------|
| `composables/useAuth.ts` | Auth wrapper |
| `composables/useToast.ts` | Toast with auto-dismiss |
| `composables/useDocuments.ts` | TanStack Query for documents |

#### Layouts (`frontend/src/layouts/`)

| File | Purpose |
|------|---------|
| `layouts/DefaultLayout.vue` | Navbar + Footer (public pages) |
| `layouts/DashboardLayout.vue` | Sidebar + TopBar + content (auth pages) |
| `layouts/AuthLayout.vue` | Centered card (login/register) |

#### Reusable Components (`frontend/src/components/`)

| File | Purpose |
|------|---------|
| `components/common/BaseButton.vue` | Variants, sizes, loading, disabled |
| `components/common/BaseInput.vue` | Label, error, icon, v-model |
| `components/common/BaseModal.vue` | Overlay, transitions, slots |
| `components/common/BaseCard.vue` | Header/body/footer slots |
| `components/common/LoadingSpinner.vue` | Animated spinner |
| `components/common/EmptyState.vue` | Icon, title, description, action |
| `components/common/Avatar.vue` | Image or initials fallback |
| `components/common/Badge.vue` | Color variants |
| `components/common/Toast.vue` | Success/error/warning/info, auto-dismiss |
| `components/layout/Navbar.vue` | Logo, links, auth buttons, mobile menu |
| `components/layout/Footer.vue` | Multi-column links, social, copyright |
| `components/layout/Sidebar.vue` | Dashboard nav, active state, collapse |
| `components/layout/TopBar.vue` | Breadcrumb, search, notifications, avatar |

#### Pages (`frontend/src/pages/`)

| File | Sections |
|------|----------|
| `pages/LandingPage.vue` | Hero, features, how-it-works, CTA |
| `pages/AboutPage.vue` | Hero, company, mission, vision, tech stack, open source, team, values |
| `pages/auth/LoginPage.vue` | Email/password, Google OAuth, links |
| `pages/auth/RegisterPage.vue` | Full form, password strength, Google OAuth |
| `pages/dashboard/DashboardPage.vue` | Stats cards, recent items, quick actions |
| `pages/chat/ChatPage.vue` | Conversation sidebar, message list, input bar, citations |
| `pages/documents/DocumentsPage.vue` | Drag-drop upload, grid/list, status badges |
| `pages/profile/ProfilePage.vue` | Avatar, edit name, activity |
| `pages/settings/SettingsPage.vue` | Account, notifications, AI prefs, security |
| `pages/admin/AdminDashboardPage.vue` | System stats, user growth, alerts |
| `pages/admin/AdminUsersPage.vue` | Users table, search, filter, role change |
| `pages/NotFoundPage.vue` | 404 with go-home button |

#### Frontend Tests (`frontend/src/__tests__/`)

| File | Tests |
|------|-------|
| `__tests__/setup.ts` | Test environment setup |
| `__tests__/components/BaseButton.test.ts` | 5 tests |
| `__tests__/components/BaseInput.test.ts` | 4 tests |
| `__tests__/components/BaseModal.test.ts` | 4 tests |
| `__tests__/components/Navbar.test.ts` | 3 tests |
| `__tests__/pages/LandingPage.test.ts` | 3 tests |
| `__tests__/pages/AboutPage.test.ts` | 4 tests |
| `__tests__/pages/LoginPage.test.ts` | 3 tests |
| `__tests__/stores/auth.test.ts` | 4 tests |

---

## 🔧 Environment Variables

### Backend (`backend/.env.example`)

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/homingo
ASYNC_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/homingo

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Auth
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback

# AI Providers
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
DEFAULT_LLM_PROVIDER=openai
DEFAULT_LLM_MODEL=gpt-4o-mini

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud
CLOUDINARY_API_KEY=your-key
CLOUDINARY_API_SECRET=your-secret

# Vector Store
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key
QDRANT_COLLECTION_NAME=homingo_docs

# Embeddings
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

# Monitoring
SENTRY_DSN=https://...@sentry.io/...

# App
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend (`frontend/.env.example`)

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=Homingo
VITE_GOOGLE_CLIENT_ID=your-google-client-id
VITE_SENTRY_DSN=https://...@sentry.io/...
VITE_CLOUDINARY_CLOUD_NAME=your-cloud
```

---

## 🐳 Docker Compose Services

| Service | Image | Port | Depends On |
|---------|-------|------|------------|
| `frontend` | docker/Dockerfile.frontend | 3000:80 | backend |
| `backend` | docker/Dockerfile.backend | 8000:8000 | postgres, redis |
| `postgres` | postgres:16-alpine | 5432:5432 | — |
| `redis` | redis:7-alpine | 6379:6379 | — |
| `celery_worker` | (same as backend) | — | backend, redis |
| `celery_beat` | (same as backend) | — | backend, redis |

**Run:** `docker compose up`

---

## 🔄 CI/CD Pipeline

### On Pull Request (`.github/workflows/ci.yml`)

```
PR opened/updated → triggers CI
  ├── backend-ci (Python 3.12)
  │   ├── pip install -r requirements.txt
  │   ├── ruff check .
  │   ├── black --check .
  │   └── pytest --cov --cov-fail-under=80
  └── frontend-ci (Node 20)
      ├── npm ci
      ├── npm run lint
      ├── npm run test
      └── npm run build
Both must pass → PR is mergeable
```

### On Merge to Main (`.github/workflows/deploy.yml`)

```
Push to main → triggers deploy
  ├── deploy-frontend
  │   ├── npm ci && npm run build
  │   └── Cloudflare Pages deploy (cloudflare/pages-action@v1)
  └── deploy-backend
      └── POST to Render deploy hook URL
```

---

## 🌿 Git Workflow

### Branches

```
main (protected — no direct pushes)
├── feature/about-page
├── feature/auth
├── feature/frontend
├── feature/backend
├── feature/chat
├── feature/rag
├── feature/dashboard
├── feature/profile
└── feature/admin
```

### Process

1. Create branch from `main`: `git checkout -b feature/my-feature main`
2. Develop and commit
3. Push: `git push origin feature/my-feature`
4. Open Pull Request → CI runs automatically
5. If CI passes → code review → merge to main
6. Merge to main → auto-deploy

---

## 👥 Team Responsibilities

### Developer 1 — Backend & Infrastructure
- FastAPI backend (`backend/app/api/`, `services/`, `repositories/`)
- Authentication (JWT, Google OAuth)
- Database models, Alembic migrations
- Docker & Docker Compose
- CI/CD pipelines
- **Branches:** `feature/auth`, `feature/backend`

### Developer 2 — Frontend & UI
- Vue 3 application (`frontend/src/`)
- Landing page, About page, Dashboard
- Reusable component library
- Responsive design, Tailwind CSS
- Frontend testing (Vitest)
- **Branches:** `feature/frontend`, `feature/about-page`, `feature/dashboard`, `feature/profile`

### Developer 3 — AI & RAG
- LangChain integration, LLM provider abstraction
- LangGraph agent workflows
- RAG pipeline (extract → chunk → embed → store → retrieve)
- Embedding service (sentence-transformers)
- Vector store (Qdrant, ChromaDB)
- Celery background tasks for document processing
- **Branches:** `feature/rag`, `feature/chat`

---

## 🔀 RAG Pipeline Flow

```
User uploads PDF
       │
       ▼
  Celery Task: process_document
       │
       ├── 1. Download file from Cloudinary
       ├── 2. Extract text (PyMuPDF → pypdf fallback)
       ├── 3. Clean text (whitespace, encoding, normalize)
       ├── 4. Chunk text (RecursiveCharacterTextSplitter, 1000 chars, 200 overlap)
       ├── 5. Generate embeddings (BAAI/bge-small-en-v1.5)
       ├── 6. Store vectors in Qdrant
       ├── 7. Store chunk metadata in PostgreSQL
       └── 8. Update document status → "completed"
       
User asks question
       │
       ├── 1. Embed query (same model)
       ├── 2. Similarity search in Qdrant (top 5)
       ├── 3. Retrieve chunk content + metadata
       ├── 4. Build prompt with context
       ├── 5. Send to LLM (OpenAI/Gemini)
       ├── 6. Generate grounded answer
       └── 7. Return answer + citations (source, page, score)
```

---

## 🤖 LangGraph Agent Architecture

```
         START
           │
           ▼
     ┌─────────────┐
     │  Reasoning   │ ← Analyze query, decide action
     └──────┬───────┘
            │
     ┌──────┴──────┐
     ▼              ▼
┌──────────┐  ┌──────────┐
│ Retrieval│  │Tool Call │
│  (RAG)   │  │          │
└────┬─────┘  └────┬─────┘
     │              │
     └──────┬───────┘
            ▼
     ┌─────────────┐
     │ Generation   │ ← Generate final response
     └──────┬───────┘
            │
            ▼
           END
```

**Capabilities:** Reasoning, Tool Calling, Retrieval, Planning, Memory

---

## 🚀 Deployment Map

| Component | Platform | URL |
|-----------|----------|-----|
| Frontend | Cloudflare Pages | https://homingo.pages.dev |
| Backend API | Render | https://homingo-api.onrender.com |
| Database | Neon PostgreSQL | (connection string in env) |
| Redis | Upstash Redis | (connection string in env) |
| Vector Store | Qdrant Cloud | (URL + API key in env) |
| File Storage | Cloudinary | (credentials in env) |
| Monitoring | Sentry | (DSN in env) |

---

## 🎯 First Feature: About Page

The first feature to implement and deploy end-to-end is the **About Page**.

1. Create `feature/about-page` branch
2. Implement `AboutPage.vue` with:
   - Responsive, modern UI
   - Hero section with gradient text
   - Company, Mission, Vision sections
   - Technology Stack display
   - Open Source section
   - Contributors/Team section
3. Write tests in `__tests__/pages/AboutPage.test.ts`
4. Push and open PR
5. CI runs (lint, test, build)
6. If pass → merge → auto-deploy

---

## 🛡️ Security Checklist

- [x] CORS configured (allowlist in env)
- [x] Rate limiting (slowapi: 100/min general, 20/min auth)
- [x] JWT with expiry + refresh tokens
- [x] Password hashing (bcrypt via passlib)
- [x] Input validation (Pydantic v2)
- [x] File upload validation (PDF only, 20MB max)
- [x] Environment variables (never hardcoded)
- [x] Structured logging (no PII in logs)
- [x] Global exception handler (no stack traces to client)
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] RBAC (admin/user roles)

---

## 📦 Key Dependencies

### Backend (Python 3.12)

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | latest | Web framework |
| uvicorn | latest | ASGI server |
| gunicorn | latest | Process manager |
| sqlalchemy | 2.0+ | ORM (async) |
| alembic | latest | Migrations |
| pydantic | 2.0+ | Validation |
| pydantic-settings | latest | Settings management |
| python-jose | latest | JWT |
| passlib | latest | Password hashing |
| celery | latest | Background tasks |
| redis | latest | Cache/broker |
| langchain | latest | LLM framework |
| langgraph | latest | Agent workflows |
| langchain-openai | latest | OpenAI provider |
| langchain-google-genai | latest | Gemini provider |
| qdrant-client | latest | Vector store |
| sentence-transformers | latest | Embeddings |
| pymupdf | latest | PDF processing |
| cloudinary | latest | File storage |
| sentry-sdk | latest | Monitoring |
| structlog | latest | Logging |
| slowapi | latest | Rate limiting |

### Frontend (Node 20)

| Package | Version | Purpose |
|---------|---------|---------|
| vue | 3.x | UI framework |
| vue-router | 4.x | Routing |
| pinia | latest | State management |
| @tanstack/vue-query | latest | Server state |
| axios | latest | HTTP client |
| @vueuse/core | latest | Vue utilities |
| tailwindcss | 3.x | CSS framework |
| typescript | 5.x | Type safety |
| vitest | latest | Testing |
| @vue/test-utils | latest | Vue testing |

---

> [!TIP]
> **Resuming work:** If generation was interrupted, check which files exist with `find /home/pushpendra/homingo -type f | sort`, compare against this manifest, and generate any missing files. Each file's purpose and content is fully described above.
