# 💭 About Rookie Route

## ✨ What is Rookie Route?

![Rookie Route Main Screen](images/main.png)

**Rookie Route** is an AI-powered code coaching and learning analytics platform
for beginner developers.

Instead of treating each AI code review as a one-off response, Rookie Route
converts analysis results into structured weakness data and accumulates them
per user so repeated error patterns can be identified across submissions.

```text
Source Code
    ↓
AI Analysis
    ↓
Structured ErrorType
    ↓
Submission / Weakness Storage
    ↓
Per-user Aggregation
    ↓
Learning Analytics
```

## 🎯 Project Goal

The goal of Rookie Route is to help beginner developers move beyond fixing a
single error and understand **which types of mistakes they repeatedly make**.

The backend therefore treats AI output as structured application data rather
than storing an unrestricted natural-language response.

## 🚀 Core Features

### AI Code Analysis

Users submit source code and receive a structured analysis consisting of:

- analysis summary
- controlled error category (`ErrorType`)
- related line number when available
- explanation for each weakness

### Structured Weakness Data

AI output is validated with Pydantic before persistence.

Unsupported categories, malformed JSON, invalid types, and oversized responses
are rejected before reaching the database.

### Persistent Learning Data

Each successful analysis is stored as a `Submission`, and its structured issues
are stored as related `Weakness` records.

```text
User
  └─ Submission
       └─ Weakness[]
```

### Per-user Learning Analytics

The authenticated dashboard aggregates:

- total code submissions
- weakness frequency by category
- most frequently occurring error patterns

### Authentication & Ownership

JWT authentication binds analysis and dashboard data to the authenticated user.

Client-supplied user IDs are not trusted when determining ownership.

## 💻 Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS
- Monaco Editor
- Recharts

### Backend

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Alembic
- OpenAI API
- Pydantic
- JWT / bcrypt

## 🤝 Project Resources

- [Getting Started](getting_started.md)
- [Technical Overview](technical.md)
- [API Reference](api.md)
- [Contribution Guide](contribution.md)
