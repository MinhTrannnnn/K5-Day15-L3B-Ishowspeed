FROM node:22-slim AS frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=frontend /frontend/dist ./frontend/dist
COPY run.py TEAMS.md ./
COPY codebase/ ./codebase/
COPY data/demo_*.json ./data/
COPY eval/ ./eval/
COPY cost/ ./cost/
RUN mkdir -p traces data/runtime
CMD ["python", "-m", "uvicorn", "api:app", "--app-dir", "codebase", "--host", "0.0.0.0", "--port", "8080"]
