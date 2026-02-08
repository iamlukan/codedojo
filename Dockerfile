# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency definition
COPY pyproject.toml .

# Install dependencies into a virtual environment
RUN uv venv .venv && \
    uv pip install --system -r pyproject.toml

# Stage 2: Runner
FROM python:3.11-slim

WORKDIR /app

# Copy env from builder (if we used venv, but here we installed system-wide in builder?)
# Actually, let's just use uv to install system-wide in the final image or copy site-packages.
# Simpler approach for now: Single stage with uv for speed, or copy from builder.
# Re-reading: "use uv inside container to install dependencies quickly".

# Let's do a single efficient stage for simplicity and speed as requested
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install system dependencies if needed (reflex might need unzip, etc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

# Install dependencies
RUN uv pip install --system -r pyproject.toml

COPY . .

# Initialize reflex (optional, but good for baking in assets if needed)
# RUN reflex init

EXPOSE 3000 8000

CMD ["reflex", "run", "--env", "dev", "--backend-host", "0.0.0.0"]
