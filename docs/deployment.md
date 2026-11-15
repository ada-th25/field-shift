# Deployment

**Live, currently deployed: https://field-shift-nnkf.onrender.com**
(Render free web service, connected to the `backend_tsuyu` branch — any
push to that branch auto-redeploys this URL.)

This project has a real Python backend (it calls NASA POWER and ISRIC
SoilGrids live), so it can't be hosted as static files — it needs
somewhere that actually runs a server. A `Dockerfile` is included at the
repo root for this; it builds the backend and serves the full frontend
from the same container (`GET /`), so there's nothing else to deploy.

## Render free web service (what's actually deployed)

Free, no card required, and officially supports Docker without
restriction. The one caveat: a free-tier service **sleeps after 15
minutes of inactivity** — the first visit after that has a ~30-60 second
cold start, which can look broken to a judge who doesn't wait. Opening
the link yourself a minute or two before a judging session avoids this.

1. Create a free account at [render.com](https://render.com).
2. **New** → **Web Service** → connect this GitHub repo, select the
   branch to deploy.
3. **Language: Docker** (the default dropdown may suggest something else,
   e.g. Ruby — change it; Render then auto-detects the root `Dockerfile`).
   Leave Build/Start Command blank — the Dockerfile handles both.
4. Pick the **Free** compute plan ($0/month, 0.1 CPU / 512 MB RAM).
5. Deploy. Render sets `$PORT` itself; the `Dockerfile` already reads it.
   The URL is `https://<your-service-name>.onrender.com`.

## Hugging Face Spaces — attempted, abandoned for this account

Hugging Face gates the **Docker** SDK behind a paid plan on some
accounts, and separately gates **CPU Basic** hardware behind a PRO
subscription for the **Gradio** SDK's free tier, leaving only **ZeroGPU**
hardware available for free. The root `app.py` and `requirements.txt` in
this repo are leftover from attempting that route (they launch the real
FastAPI backend via `uvicorn.run(...)`, mounting a dummy Gradio app
purely to satisfy ZeroGPU's `@spaces.GPU` detection) and got as far as
passing that check, but then hit a port-binding conflict between our
`uvicorn.run()` and ZeroGPU's own worker process, both claiming port
7860. Abandoned in favor of Render rather than continuing to debug
ZeroGPU-specific internals. If your Hugging Face account *does* have
Docker SDK access (no paid-plan gate), that would be the simpler and
no-cold-start route — see the git history of this file for the
step-by-step Docker-SDK instructions that were written before this
account's restriction was discovered.

## Testing the container locally first

```bash
docker build -t harvest-heroes .
docker run -p 8000:7860 harvest-heroes
```

Then open `http://localhost:8000/`.
