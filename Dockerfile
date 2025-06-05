FROM python:3.12-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app
# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Copy the application into the container.
COPY . /app

WORKDIR /app
# Install the application dependencies.
RUN uv sync --frozen --no-cache && \ 
    # Not Root
    adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser
# Expose
EXPOSE 8000
# Run the application.
CMD ["./.venv/bin/uvicorn", "app.main:app","--log-level","warning","--host", "0.0.0.0","--port", "8000","--workers","2"]
