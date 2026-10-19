# 🚀 RookieRoute API Reference

RookieRoute provides a FastAPI backend for authentication, AI-assisted code
analysis, structured weakness persistence, and per-user analytics.

---

## 📌 Base Information

| Item | Description |
| :--- | :--- |
| **Base URL** | `http://localhost:8000` |
| **Swagger UI** | `http://localhost:8000/docs` |
| **ReDoc** | `http://localhost:8000/redoc` |
| **Authentication** | OAuth2 Password Bearer / JWT |
| **Data Format** | JSON |

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

---

# 🔐 Authentication

## `POST /auth/signup`

Creates a user account.

### Request

```json
{
  "email": "dev@example.com",
  "password": "StrongPassword123!",
  "username": "rookie_dev"
}
```

### Response

```text
201 Created
```

```json
{
  "email": "dev@example.com",
  "username": "rookie_dev"
}
```

Duplicate username or email:

```text
409 Conflict
```

---

## `POST /auth/login`

Authenticates a user and returns a JWT access token.

The endpoint accepts OAuth2 form data rather than JSON.

### Content-Type

```text
application/x-www-form-urlencoded
```

### Required Fields

```text
username
password
```

### Response

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

---

# 💻 Code Review

## `POST /review/analyze` 🔒

Submits source code for AI analysis.

### Request

```json
{
  "code": "def calculate_area(radius):\n    return 3 * radius * radius",
  "language": "python"
}
```

### Response

```json
{
  "submission_id": 105,
  "summary": "코드 분석 요약",
  "weaknesses": [
    {
      "type": "LogicError",
      "line": 2,
      "explanation": "분석된 문제에 대한 설명"
    }
  ]
}
```

The AI response must satisfy the backend's `AIAnalysisResult` and `AIWeakness`
schemas before it can be persisted.

Unsupported `ErrorType` values or malformed responses are rejected.

---

# 📊 Dashboard

## `GET /dashboard/stats/me` 🔒

Returns aggregated statistics for the authenticated user.

The backend derives the user from the validated JWT.

No `user_id` path or query parameter is accepted.

### Response

```json
{
  "stats": [
    {
      "count": 15,
      "weakness_type": "LogicError"
    },
    {
      "count": 8,
      "weakness_type": "SyntaxError"
    },
    {
      "count": 5,
      "weakness_type": "Security"
    }
  ],
  "total_submissions": 42
}
```

---

# ⚙️ System

## `GET /`

Health-check endpoint.

### Response

```json
{
  "message": "RookieRoute 서버가 정상적으로 실행 중입니다."
}
```

---

# 📦 Data Models

## UserCreate

| Field | Type |
| :--- | :--- |
| `username` | string |
| `email` | email string |
| `password` | string |

## UserResponse

| Field | Type |
| :--- | :--- |
| `username` | string |
| `email` | string |

## Token

| Field | Type |
| :--- | :--- |
| `access_token` | string |
| `token_type` | string |

## CodeRequest

| Field | Type |
| :--- | :--- |
| `code` | string |
| `language` | string |

## AIWeakness

| Field | Type |
| :--- | :--- |
| `type` | `ErrorType` |
| `line` | integer or null |
| `explanation` | string |

## AnalysisResponse

Extends `AIAnalysisResult` and adds:

```text
submission_id
```

## DashboardResponse

```text
total_submissions
stats[]
  ├─ weakness_type
  └─ count
```
