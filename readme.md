# Competitive Intelligence Tracker

A full-stack web app that tracks changes on competitor websites (pricing, docs, changelogs), highlights diffs, and generates AI-powered summaries with citations.

## Features
- Add competitors (pricing/docs/changelog URLs)
- Fetch and store page snapshots
- Detect changes between checks
- AI-generated summaries with relevant context
- History of last 5 checks per competitor
- Health & status monitoring endpoints

## Tech Stack
- Backend: FastAPI, SQLAlchemy, SQLite
- Frontend: Next.js (App Router), TypeScript, Tailwind CSS
- AI: OpenAI API
- Hosting: (to be added)

## How to run locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

Frontend
cd frontend
npm install
npm run dev

Backend docs: http://localhost:8000/docs
Frontend: http://localhost:3000