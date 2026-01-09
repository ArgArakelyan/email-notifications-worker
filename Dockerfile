FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# uv из официального образа
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --python 3.12

# Копируем код
COPY app/ ./app/
RUN uv sync --frozen --no-dev --python 3.12

# Runtime stage
FROM python:3.12-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:${PATH}"

RUN useradd -m -u 10001 appuser

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

USER appuser

# НЕТ порта для worker'а!
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import app.core.broker; print('healthy')" || exit 1

# ✅ broker.run() вместо faststream CLI
CMD ["python", "-m", "app.main"]
