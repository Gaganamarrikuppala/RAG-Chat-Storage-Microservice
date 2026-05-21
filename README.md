# RAG Chat Storage Service

Production-ready backend microservice for storing RAG chatbot sessions, chat messages, and optional retrieved context.

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Docker Compose
- SlowAPI rate limiting
- API key authentication
- Swagger/OpenAPI documentation
- Adminer database browser
- Pytest tests

## Features

- Create and maintain chat sessions per user
- Rename chat sessions
- Mark/unmark sessions as favorite
- Delete sessions with cascading message deletion
- Store user/assistant/system messages
- Store optional RAG retrieved context as JSON
- Retrieve paginated message history
- API key authentication using environment variables
- Rate limiting
- Centralized JSON logging
- Global exception handling
- CORS configuration
- Health check endpoint
- Dockerized API, PostgreSQL, and Adminer

## Project Structure

```text
app/
  api/v1/endpoints/     API routes
  core/                 config, db, security, logging, limiter
  models/               SQLAlchemy ORM models
  schemas/              Pydantic request/response DTOs
  services/             business logic
tests/                  basic API tests
```

## Local Setup with Docker

### 1. Create `.env`

```bash
cp .env.example .env
```

Update `API_KEY` in `.env` before running in a real environment.

### 2. Start services

```bash
docker compose up --build
```

API will be available at:

```text
http://localhost:8000
```

Swagger docs:

```text
http://localhost:8000/docs
```

Adminer:

```text
http://localhost:8080
```

Adminer login:

```text
System: PostgreSQL
Server: postgres
Username: rag_user
Password: rag_password
Database: rag_chat
```

## Run Without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

For non-Docker local execution, set `DATABASE_URL` to your local PostgreSQL connection string.

## Authentication

All session APIs require this header:

```http
X-API-Key: replace-with-strong-api-key
```

The expected key is read from the `API_KEY` environment variable.

## API Endpoints

### Health Check

```http
GET /api/v1/health
```

### Create Session

```http
POST /api/v1/sessions
X-API-Key: replace-with-strong-api-key
Content-Type: application/json

{
  "user_id": "user_123",
  "title": "Loan eligibility conversation"
}
```

### List Sessions

```http
GET /api/v1/sessions?user_id=user_123&favorite_only=false&limit=20&offset=0
X-API-Key: replace-with-strong-api-key
```

### Get Session

```http
GET /api/v1/sessions/{session_id}
X-API-Key: replace-with-strong-api-key
```

### Rename Session

```http
PATCH /api/v1/sessions/{session_id}/rename
X-API-Key: replace-with-strong-api-key
Content-Type: application/json

{
  "title": "Updated conversation title"
}
```

### Mark/Unmark Favorite

```http
PATCH /api/v1/sessions/{session_id}/favorite
X-API-Key: replace-with-strong-api-key
Content-Type: application/json

{
  "is_favorite": true
}
```

### Delete Session

```http
DELETE /api/v1/sessions/{session_id}
X-API-Key: replace-with-strong-api-key
```

### Add Message

```http
POST /api/v1/sessions/{session_id}/messages
X-API-Key: replace-with-strong-api-key
Content-Type: application/json

{
  "sender": "USER",
  "content": "What is my credit card limit?",
  "retrieved_context": {
    "documents": [
      {
        "source": "faq-credit-card-limits",
        "chunk": "Credit card limits depend on eligibility and bank policy."
      }
    ]
  }
}
```

Allowed sender values:

```text
USER, ASSISTANT, SYSTEM
```

### Get Paginated Messages

```http
GET /api/v1/sessions/{session_id}/messages?limit=20&offset=0
X-API-Key: replace-with-strong-api-key
```

## Run Tests

```bash
pytest
```

## Example cURL Flow

```bash
export API_KEY="replace-with-strong-api-key"

curl -X POST http://localhost:8000/api/v1/sessions \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user_123","title":"First RAG chat"}'
```

## Notes for Reviewers

This project intentionally uses a clean layered architecture:

- Routers handle HTTP concerns.
- Schemas validate request and response contracts.
- Services contain business logic.
- Models define persistence structure.
- Core modules centralize cross-cutting concerns like config, security, logging, rate limiting, and error handling.

The service is designed to be easy to extend with migrations, user identity integration, message encryption, background jobs, or observability tooling.
