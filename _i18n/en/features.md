# Core Features

Rookie Route turns repeated AI code reviews into structured learning data
that can be accumulated and analyzed per user.

---

## 🤖 AI-Powered Code Analysis

Users can write or paste source code in the Monaco-based editor and request
an AI analysis.

The backend returns:

- a concise analysis summary
- detected weaknesses
- controlled error categories
- related line numbers when available
- explanations for each weakness

AI output is validated before it is stored.

---

## 🧩 Structured Error Classification

Rookie Route uses a shared `ErrorType` taxonomy across the AI prompt,
Pydantic validation, database model, and dashboard.

Current categories are:

- SyntaxError
- IndentationError
- TypeError
- ImportError
- NameError
- LogicError
- InfiniteLoop
- BoundaryError
- NullSafety
- DataStructureMisuse
- Efficiency
- RedundantCode
- NamingConvention
- Security
- Documentation
- Other

This prevents arbitrary AI-generated category names from polluting
long-term analytics.

---

## 💾 Persistent Learning Data

Each successful analysis is stored as a `Submission`, while detected issues
are stored as related `Weakness` records.

```text
User
  └─ Submission
       └─ Weakness[]
```

This converts a one-time AI response into structured data that can be
aggregated across multiple submissions.

---

## 📊 Personal Error Pattern Analytics

The authenticated dashboard aggregates stored weaknesses directly in the
database.

It provides:

- total number of analyses
- count per weakness category
- the most frequently occurring weakness
- error-category distribution

The dashboard identifies repeated error patterns rather than assigning
an unverified overall programming score.

---

## 🕘 Recent Analysis History

The code-analysis screen also keeps up to 20 recent analyses in browser
`localStorage`.

This local history is used for quickly reopening recently analyzed code.

It is separate from the server-side `Submission` and `Weakness` data used
for learning analytics.

---

## 🔐 Authenticated User Data

Signup and login are handled by the FastAPI backend using JWT authentication.

Analysis ownership is derived from the authenticated user rather than from
a user identifier supplied by the client.

The dashboard likewise returns only the current user's statistics.

---

## 🛠️ Technology

**Frontend**

- React
- Vite
- Tailwind CSS
- Monaco Editor
- Recharts

**Backend**

- FastAPI
- SQLAlchemy
- MySQL
- Alembic
- OpenAI API
- Pydantic
- JWT / bcrypt
