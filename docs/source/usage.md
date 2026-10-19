# 💡 How to Use Rookie Route

Rookie Route is an AI-powered code analysis and learning analytics tool for
beginner developers.

## 🧠 AI-Powered Code Analysis

![AI Code Analysis - Error Patterns](images/analyze1.png)

### Submit Code for Analysis

1. Sign up or log in.
2. Open the code-analysis screen.
3. Paste or write source code in the editor.
4. Select the language.
5. Click **Analyze My Code**.
6. Review the returned summary and weaknesses.

The analysis response contains:

- a summary
- a controlled `ErrorType`
- the related line number when available
- an explanation for each weakness

The backend validates the AI response before storing it.

## 🕘 Recent Analysis History

The analysis screen keeps up to 20 recent analyses in browser `localStorage`.

The History panel can be used to reopen recently analyzed code.

This browser history is separate from server-side learning analytics.

## 📊 Personal Error Pattern Analytics

![Error Visualization](images/analyze2.png)

The authenticated report page retrieves:

```text
GET /dashboard/stats/me
```

The backend derives the user identity from the JWT and aggregates the user's
stored `Weakness` records.

The report currently shows:

- total number of completed analyses
- weakness count by `ErrorType`
- the most frequently occurring weakness
- error-category distribution

```text
Authenticated User
       ↓
Submission[]
       ↓
Weakness[]
       ↓
COUNT / GROUP BY ErrorType
       ↓
Dashboard
```

No client-provided user ID is used to retrieve another user's statistics.
