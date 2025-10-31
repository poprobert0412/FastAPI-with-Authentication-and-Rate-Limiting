# 📄 FastAPI with Authentication and Rate Limiting

A minimal **FastAPI** project showcasing API Key Authentication and simple Rate Limiting using dependency injection. The app manages job entries with basic in-memory storage.

---

## 🚀 Getting Started

### Prerequisites
You’ll need:
- **Python 3.8+**
- **fastapi**
- **uvicorn**
- **pydantic**
- **requests** (for testing)

Install dependencies:
```bash
pip install fastapi uvicorn pydantic requests
```

### Run the Application
Start the development server:
```bash
uvicorn main:app --reload
```
Server runs at **http://127.0.0.1:8000**

To test authentication and rate limiting, run:
```bash
python testing.py
```

---

## 💻 Code Overview

### `main.py`
Core FastAPI application, using an in-memory `fake_db` to store job entries.

| Feature | Description |
|----------|--------------|
| **Authentication** | Implemented via `verify_api_key` dependency. Validates `X-API-Key` header against `SECRET_KEY_123`. Returns **401 Unauthorized** if invalid. |
| **Rate Limiting** | Controlled by `rate_limit_per_key`. Limits `/jobs/` GET requests to **5 per API key**. Exceeding this returns **429 Too Many Requests**. |

#### Endpoints
- **`GET /jobs/`** — List all jobs. Requires **API Key + Rate Limiting**.  
- **`POST /jobs/`** — Add a new job. Requires **API Key** only.  
- **`GET /jobs/{job_id}`** — Retrieve a specific job. Requires **API Key**. Returns **404** if not found.

---

### `testing.py`
Demonstrates how the API behaves under various authentication and rate limit scenarios.

**Test Flow:**
1. Missing API key → **401 Unauthorized**  
2. Invalid key → **401 Unauthorized**  
3. Valid key → **200 OK**  
4. Exceeding rate limit → **429 Too Many Requests**

Includes `add_new_job()` for manual testing of the POST endpoint.

---

## 🔑 Security Details

- **Valid API Key:** `SECRET_KEY_123`  
- **Rate Limit:** `5` requests per key for `/jobs/` endpoint (in-memory, per app instance).

> ⚠️ Note: This rate limiter resets only when the app restarts.  
For production, use Redis-backed libraries like **fastapi-limiter** or **slowapi** for distributed rate limiting.

**Author:** Pop Robert 
**Tech Stack:** FastAPI • Python • Uvicorn • Pydantic • Requests
