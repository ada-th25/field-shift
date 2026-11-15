# Deployment

This project has a real Python backend (it calls NASA POWER and ISRIC
SoilGrids live), so it can't be hosted as static files — it needs
somewhere that actually runs a server. A `Dockerfile` is included at the
repo root for this; it builds the backend and serves the full frontend
from the same container (`GET /`), so there's nothing else to deploy.

Both options below are free and don't require a payment card.

## Hugging Face Spaces, Gradio SDK (recommended — no cold-start sleep)

Hugging Face gates the **Docker** SDK behind a paid plan on some
accounts (the Space-creation page shows "Docker 🔒 Paid" if so). The
**Gradio** SDK stays free and just runs `python app.py` in a Python
environment — it doesn't require an actual Gradio UI, so the root
`app.py` in this repo uses that slot to launch the real FastAPI backend
directly via `uvicorn.run(...)`, the same server `uvicorn app.main:app`
runs locally. This has been tested end-to-end (static assets, `/api/crops`,
and a live `/rotations` NASA call all confirmed working through this
entry point).

1. Create a new Space: **New Space** → pick a name → **SDK: Gradio** →
   **Visibility: Public**.
2. Push this repo to the Space's git remote (shown on the Space's page
   after creation), e.g.:
   ```bash
   git remote add space https://huggingface.co/spaces/<your-username>/<space-name>
   git push space main
   ```
3. Hugging Face auto-installs the root `requirements.txt` and runs the
   root `app.py` — no extra configuration needed. The Space builds and
   starts automatically; the URL is
   `https://huggingface.co/spaces/<your-username>/<space-name>`.

## Render free web service (fallback, has cold-start sleep)

Free, no card required, and officially supports Docker without
restriction. The one caveat: a free-tier service **sleeps after 15
minutes of inactivity** — the first visit after that has a ~30-60 second
cold start, which can look broken to a judge who doesn't wait. Opening
the link yourself a minute or two before a judging session avoids this.

1. Create a free account at [render.com](https://render.com).
2. **New** → **Web Service** → connect this GitHub repo.
3. Environment: **Docker** (Render will detect the root `Dockerfile`
   automatically). Leave build/start commands blank — the Dockerfile
   handles both.
4. Deploy. Render sets `$PORT` itself; the `Dockerfile` already reads it.
5. The URL is `https://<your-service-name>.onrender.com`.

## Testing the container locally first

```bash
docker build -t harvest-heroes .
docker run -p 8000:7860 harvest-heroes
```

Then open `http://localhost:8000/`.
