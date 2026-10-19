# ❓ FAQ

## 🌐 General Questions

### Q1: What is the goal of Rookie Route?

Rookie Route helps beginner developers turn repeated AI code reviews into
structured learning data.

Instead of only fixing the current submission, the system stores validated
weakness categories per user and aggregates repeated error patterns across
multiple submissions.

### Q2: Is Rookie Route open source?

Yes. The project repository is distributed under the Apache License 2.0.

---

## ⚙️ Usage and Setup

### Q1: What environment is required to run the project locally?

The current repository uses:

- Python 3.11+
- Node.js 24
- MySQL 8.0+

See `README.md` and `getting_started.md` for the current setup procedure.

### Q2: How does the code review feature work?

The authenticated user submits source code to the FastAPI backend.

The backend sends the code to the configured OpenAI model and requires a
structured JSON response.

Pydantic validates the returned summary and weaknesses against the
application's `ErrorType` taxonomy before the result is stored as
`Submission` and `Weakness` records.

### Q3: How can I confirm that the backend is running?

Open:

```text
http://localhost:8000/docs
```

or request:

```text
GET /
```

The root endpoint returns:

```json
{
  "message": "RookieRoute 서버가 정상적으로 실행 중입니다."
}
```

---

## 🤝 Contribution

### Q1: I found a bug. How should I report it?

Use the repository's issue tracker and include:

- a clear description
- reproduction steps
- expected behavior
- actual behavior
- environment information

See `CONTRIBUTING.md` for the collaboration workflow.

### Q2: Can I contribute without changing application code?

Yes.

Documentation, translation, tests, bug reports, and improvement proposals
can also be useful contributions.