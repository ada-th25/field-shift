FROM python:3.12-slim

WORKDIR /app

COPY backend/app/requirements.txt /app/backend/app/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/app/requirements.txt

COPY . /app

WORKDIR /app/backend

# Render sets $PORT; Hugging Face Spaces' Docker SDK defaults to 7860
# unless app_port is set in the Space's README frontmatter.
ENV PORT=7860
EXPOSE 7860

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
