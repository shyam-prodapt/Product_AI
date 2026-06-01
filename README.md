# AI Product Strategy Assistant

A production-grade, multi-agent AI system that transforms business documents into actionable product strategy insights. Upload a CSV, PDF, or DOCX — seven AI agents analyze the data in parallel and return a full strategy report with SWOT analysis, feature prioritization, opportunity scoring, product roadmap, and an executive summary. Ask follow-up questions via a grounded RAG chat interface and download a professional PDF report.

**Live Demo:** https://product-strategy-frontend-j8cb.onrender.com  
**Backend API:** https://product-strategy-backend.onrender.com/docs

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (Vite)                   │
│  Upload → AgentProgress → Dashboard → Chat → PDF Download   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
┌────────────────────────▼────────────────────────────────────┐
│                    FastAPI Backend                           │
│                                                             │
│  POST /api/upload/      → parse + embed + Pinecone index    │
│  POST /api/analysis/run → 7-agent orchestrator              │
│  POST /api/chat/        → RAG Q&A via Pinecone              │
│  POST /api/report/download → ReportLab PDF                  │
└──────┬────────────────────────────┬───────────────────────┘
       │                            │
┌──────▼──────┐            ┌────────▼─────────┐
│  OpenAI     │            │   Pinecone        │
│  Gateway    │            │   Serverless      │
│  gpt-4o-mini│            │   Vector DB       │
│  embeddings │            │   (1536-dim)      │
└─────────────┘            └──────────────────┘
```

### 7-Agent Pipeline

All agents run via `asyncio.gather` — phases 1 and 2 are parallelized:

**Phase 1 — Run in parallel:**
| Agent | Role |
|---|---|
| Customer Feedback Agent | Sentiment, pain points, NPS from review data |
| Market Research Agent | Trends, segments, regional growth opportunities |
| Competitor Analysis Agent | Product/category competitive positioning |
| Feature Prioritization Agent | RICE scoring, 4-feature ranked list, 2-phase roadmap |
| Opportunity Agent | Opportunity scoring (1–10), 3 top opportunities |

**Phase 2 — Consume Phase 1 outputs, run in parallel:**
| Agent | Role |
|---|---|
| SWOT Analysis Agent | Synthesizes all 5 outputs into a SWOT matrix |
| Executive Report Agent | C-suite summary + 3 strategic recommendations |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, uvicorn |
| Frontend | React 18, Vite, TailwindCSS |
| AI Model | gpt-4o-mini via custom OpenAI-compatible gateway |
| Embeddings | text-embedding-3-small (dim=1536) |
| Vector DB | Pinecone serverless |
| PDF | ReportLab |
| File Parsing | PyPDF2, python-docx, pandas |

---

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- Pinecone account (free tier works)

### 1. Clone and configure

```bash
git clone <your-repo-url>
cd product-strategy-ai
cp .env.example .env
```

Edit `.env` and fill in your Pinecone API key:
```env
OPENAI_API_KEY=learner025
OPENAI_BASE_URL=https://keygateway.arshnivlabs.com/v1
PINECONE_API_KEY=<your-pinecone-api-key>
PINECONE_INDEX_NAME=product-strategy-index
PINECONE_ENVIRONMENT=us-east-1
CORS_ORIGINS=["http://localhost:5173"]
MAX_FILE_SIZE_MB=50
UPLOAD_DIR=./uploads
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8001
```

API available at `http://localhost:8001`  
Swagger UI at `http://localhost:8001/docs`

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`

### 4. Test with sample data

Upload `Sample Sales Data.csv` (included in repo) — 120 rows of product sales across 10 products, 5 regions, with customer reviews. The full 7-agent pipeline runs in under 60 seconds.

---

## Deployment on Render

### Step 1 — Push to GitHub

```bash
cd product-strategy-ai
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### Step 2 — Deploy the Backend first

1. Go to [render.com](https://render.com) → **New** → **Web Service**
2. Connect your GitHub repo
3. Configure:
   - **Name:** `product-strategy-backend`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Under **Environment Variables**, add:

| Key | Value | Secret? |
|---|---|---|
| `OPENAI_API_KEY` | `learner025` | No |
| `OPENAI_BASE_URL` | `https://keygateway.arshnivlabs.com/v1` | No |
| `PINECONE_API_KEY` | `pcsk_...your key...` | **Yes** |
| `PINECONE_INDEX_NAME` | `product-strategy-index` | No |
| `PINECONE_ENVIRONMENT` | `us-east-1` | No |
| `CORS_ORIGINS` | `["https://product-strategy-frontend.onrender.com"]` | No |
| `UPLOAD_DIR` | `/tmp/uploads` | No |
| `MAX_FILE_SIZE_MB` | `50` | No |

5. Click **Create Web Service**
6. Wait for deploy to complete — copy the URL e.g. `https://product-strategy-backend.onrender.com`

### Step 3 — Deploy the Frontend

1. Go to Render → **New** → **Static Site**
2. Connect the same GitHub repo
3. Configure:
   - **Name:** `product-strategy-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Under **Environment Variables**, add:

| Key | Value |
|---|---|
| `VITE_API_URL` | `https://product-strategy-backend.onrender.com` |

5. Click **Create Static Site**

### Step 4 — Update CORS on the Backend

Once the frontend is deployed and you have its URL (e.g. `https://product-strategy-frontend.onrender.com`):

1. Go to your **backend** service on Render → **Environment**
2. Update `CORS_ORIGINS` to `["https://product-strategy-frontend.onrender.com"]`
3. Click **Save Changes** — the service redeploys automatically

### Step 5 — Verify

- Backend health: `https://product-strategy-backend.onrender.com/health` → `{"status":"ok"}`
- Frontend: `https://product-strategy-frontend.onrender.com` → upload `Sample Sales Data.csv`

> **Note on Render Free Tier:** Services spin down after 15 minutes of inactivity. The first request after sleep takes ~30 seconds to cold-start.

---

## Alternative: Deploy via render.yaml (Blueprint)

The repo includes `render.yaml` at the root. In the Render dashboard:

1. **New** → **Blueprint**
2. Connect your repo — Render reads `render.yaml` automatically
3. Set the one secret manually: `PINECONE_API_KEY`
4. After both services deploy, update `CORS_ORIGINS` on the backend with the actual frontend URL

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Swagger UI |
| `POST` | `/api/upload/` | Upload and index documents (multipart/form-data) |
| `POST` | `/api/analysis/run` | Run 7-agent analysis pipeline |
| `POST` | `/api/chat/` | RAG-based Q&A grounded in uploaded docs |
| `POST` | `/api/report/download` | Generate and download executive PDF report |

### Upload request

```bash
curl -X POST https://product-strategy-backend.onrender.com/api/upload/ \
  -F "files=@Sample Sales Data.csv"
# Returns: { "session_id": "uuid", "files_processed": 1, "chunks_indexed": 3 }
```

### Analysis request

```bash
curl -X POST https://product-strategy-backend.onrender.com/api/analysis/run \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<session_id from upload>"}'
```

---

## Environment Variables Reference

| Variable | Description | Default |
|---|---|---|
| `OPENAI_API_KEY` | API key for the OpenAI-compatible gateway | `learner025` |
| `OPENAI_BASE_URL` | Gateway base URL | `https://keygateway.arshnivlabs.com/v1` |
| `PINECONE_API_KEY` | Pinecone API key — **required** | — |
| `PINECONE_INDEX_NAME` | Pinecone index name | `product-strategy-index` |
| `PINECONE_ENVIRONMENT` | Pinecone region | `us-east-1` |
| `CORS_ORIGINS` | JSON array of allowed frontend origins | `["http://localhost:5173"]` |
| `UPLOAD_DIR` | File upload directory | `./uploads` |
| `MAX_FILE_SIZE_MB` | Max upload file size | `50` |
| `VITE_API_URL` | Backend URL (frontend build-time env var) | `""` (uses Vite proxy in dev) |

---

## Project Structure

```
product-strategy-ai/
├── render.yaml                   # Render Infrastructure-as-Code
├── .env.example                  # Environment variable template
├── .gitignore
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── main.py                   # FastAPI app entry point
│   ├── config.py                 # Pydantic settings
│   ├── requirements.txt
│   ├── agents/
│   │   ├── base_agent.py         # Abstract base with OpenAI client
│   │   ├── orchestrator.py       # asyncio.gather coordinator
│   │   ├── customer_feedback_agent.py
│   │   ├── market_research_agent.py
│   │   ├── competitor_analysis_agent.py
│   │   ├── feature_prioritization_agent.py
│   │   ├── opportunity_agent.py
│   │   ├── swot_agent.py
│   │   └── executive_report_agent.py
│   ├── services/
│   │   ├── embedding_service.py  # OpenAI text-embedding-3-small
│   │   ├── pinecone_service.py   # Vector DB (lazy singleton)
│   │   ├── file_parser.py        # PDF/DOCX/CSV/TXT → chunks
│   │   └── pdf_generator.py      # ReportLab PDF export
│   ├── models/
│   │   └── schemas.py            # Pydantic request/response models
│   └── routers/
│       ├── upload.py
│       ├── analysis.py
│       ├── chat.py
│       └── report.py
└── frontend/
    ├── public/
    │   └── _redirects            # SPA routing for Render static sites
    └── src/
        ├── App.jsx               # Phase state machine: upload→analyzing→results
        ├── api/client.js         # Axios client (VITE_API_URL aware)
        ├── hooks/                # useFileUpload, useAnalysis, useChat
        └── components/
            ├── Layout/           # Header, Sidebar
            ├── Upload/           # Drag-and-drop FileUploadZone
            ├── Analysis/         # AgentProgressTracker, AnalysisDashboard
            ├── Chat/             # RAG chat interface with markdown
            └── Report/           # PDF download button
```
