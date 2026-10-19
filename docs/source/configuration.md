# ⚙️ Configuration Guide

This document describes the environment variables currently read by the
Rookie Route application.

---

# 🐍 Backend Configuration

Create:

```text
app/backend/.env
```

The backend loads this file through `pydantic-settings`.

## Variables

| Variable | Required | Description | Default |
| :--- | :---: | :--- | :--- |
| `DATABASE_URL` | Yes | SQLAlchemy database URL | — |
| `SECRET_KEY` | Yes | JWT signing secret, minimum 32 characters | — |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | JWT expiration in minutes | `30` |
| `OPENAI_API_KEY` | For AI analysis | OpenAI API credential | — |
| `OPENAI_MODEL` | No | OpenAI model used for analysis | `gpt-4o-mini` |
| `OPENAI_TIMEOUT_SECONDS` | No | OpenAI request timeout | `30` |
| `OPENAI_MAX_RETRIES` | No | OpenAI SDK retry count | `2` |

## Example

```ini
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
OPENAI_TIMEOUT_SECONDS=30
OPENAI_MAX_RETRIES=2

DATABASE_URL=mysql+mysqlconnector://root:your_password@localhost:3306/rookie_route

SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a strong `SECRET_KEY` locally:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Do not commit the resulting value.

## SQLite Development Example

For development or isolated tests:

```ini
DATABASE_URL=sqlite:///./rookie_route.db
```

---

# ⚛️ Frontend Configuration

Create:

```text
app/frontend/.env
```

## Variable

| Variable | Description | Example |
| :--- | :--- | :--- |
| `VITE_API_URL` | Base URL used by the frontend API client | `http://localhost:8000` |

## Example

```ini
VITE_API_URL=http://localhost:8000
```

The current frontend reads only `VITE_API_URL`.

Vite exposes client-side environment variables only when their names begin
with `VITE_`.