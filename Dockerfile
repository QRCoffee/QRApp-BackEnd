# ─────────────── BUILD STAGE ───────────────
FROM python:3.12-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Cài các thư viện hệ thống cần thiết
RUN apk add --no-cache build-base curl libffi-dev openssl-dev

# Cài `uv`
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Tạo thư mục app
WORKDIR /app

# Sao chép file phụ thuộc trước (tận dụng cache tốt hơn)
COPY pyproject.toml poetry.lock* ./

# Nếu chưa có uv.lock thì tạo mới (có thể thay đổi tùy môi trường)
RUN uv lock

# Tạo môi trường ảo và cài dependencies
RUN uv venv && \
    uv pip install --upgrade pip && \
    uv sync --frozen --no-cache && \
    find .venv -name '*.pyc' -delete && \
    find .venv -name '__pycache__' -type d -exec rm -rf {} +

# Sao chép mã nguồn
COPY app ./app

# ─────────────── RUNTIME STAGE ───────────────
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Tạo user không phải root
RUN adduser -D appuser

WORKDIR /app

# Chỉ copy những gì cần thiết từ builder
COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/app ./app

# Đặt quyền
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Chạy FastAPI với Uvicorn
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--log-level=warning", "--host=0.0.0.0", "--port=8000", "--workers=2"]
