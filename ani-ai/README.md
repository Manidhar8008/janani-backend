# Ani.ai — Behavior Intelligence

Mobile-first prototype for **Write → Compare → Score → Grow**.

## What this prototype does
- Capture typed writing directly from a phone.
- Capture handwritten pages with the phone camera.
- Store captures locally first so the app works without a backend.
- Export the personal archive as JSON.
- Calculate a transparent prototype Discipline Score from cadence, clarity, completion signals, and progress signals.
- Keep the data model ready for Supabase and the future smart pen.

## Source of truth
The current product concept is based on the 10-page Ani.ai deck:
- Smart Writing Pen: biomotion + stroke capture.
- Personal Intelligence Dashboard: timelines, comparisons, habit insights.
- Behavioral Analysis Engine: comparison, scoring, action suggestions.
- Longitudinal writing comparison.
- Discipline Score: consistency, clarity, completion, progress.
- Capture → Sync → Analyze → Compare.
- React/TypeScript/FastAPI, PostgreSQL/pgvector, local models/Ollama.
- Long-term vision: private, continuous, actionable Personal Cognitive Operating System.

## Run locally
```bash
cd ani-ai
python3 -m http.server 8080
```
Open `http://localhost:8080` on the phone or computer.

## Architecture
`Phone/Pen → Capture Adapter → Writing Event → Local Archive → Supabase → Behavior Engine → Timeline/Score/Actions`

The current GitHub connector cannot create a brand-new repository, so this prototype is staged under `Manidhar8008/janani-backend/ani-ai` on branch `ani-ai-bootstrap`. Move this directory into a dedicated `Manidhar8008/ani-ai` repository when repository creation is available.
