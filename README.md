# CodeDojo

A platform for coding challenges.

## Prerequisites

- [uv](https://github.com/astral-sh/uv)
- Docker & Docker Compose

## Quick Start

1. **Initialize the project** (if running locally without Docker for dev):
   ```bash
   uv run reflex init
   ```

2. **Run with Docker Compose** (Recommended):
   The application is containerized and managed via Docker Compose.
   
   ```bash
   docker compose up --build
   ```
   
   This will start:
   - **App**: http://localhost:3000
   - **Database**: Postgres 15 on port 5432

## Development commands

- Check logs: `docker compose logs -f`
- Stop: `docker compose down`
