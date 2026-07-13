# Ports & Adapters Exercise

This project contains the starting point for the **Ports & Adapters** exercise from *Software Design Mastery*.

The application is a small FastAPI service for managing equipment rentals. The current implementation intentionally mixes HTTP handling, business logic, database access, and notifications. Your goal is to refactor it into a Ports & Adapters architecture.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)

## Install Dependencies

```bash
uv sync
```

## Run the Application

Start the development server:

```bash
uv run uvicorn app:app --reload
```

The API will be available at:

- http://127.0.0.1:8000

Interactive API documentation:

- http://127.0.0.1:8000/docs

## Try the API

### Register Equipment

```bash
curl -X POST http://127.0.0.1:8000/equipment \
  -H "Content-Type: application/json" \
  -d '{
    "id": "eq-001",
    "name": "Projector"
  }'
```

Expected response:

```json
{
  "status": "registered"
}
```

---

### Rent Equipment

```bash
curl -X POST http://127.0.0.1:8000/rentals \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_id": "eq-001",
    "renter_email": "alice@example.com"
  }'
```

Expected response:

```json
{
  "status": "rented"
}
```

You should also see a notification printed in the terminal.

## Exercise

Refactor the application so that:

- business logic lives in application use cases
- SQLite access is moved to a repository adapter
- notifications are moved to a notifier adapter
- FastAPI only translates HTTP requests and responses
- application-specific errors replace `HTTPException` inside the core

The goal is to keep the application logic independent from frameworks and infrastructure.