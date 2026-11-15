"""Entry point for Hugging Face Spaces' Gradio SDK.

Spaces just run `python app.py` in a Python environment — this doesn't
build a Gradio UI, it launches the real FastAPI app (backend/app/main.py)
directly via uvicorn, the same server `uvicorn app.main:app` runs locally.
"""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
# Running `python app.py` puts REPO_ROOT on sys.path, which collides with
# importing the `app` package from backend/ (this very script is also named
# app.py) — drop it so only backend/'s `app` package resolves.
sys.path = [p for p in sys.path if p not in ("", str(REPO_ROOT))]
sys.path.insert(0, str(REPO_ROOT / "backend"))

import uvicorn

from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
