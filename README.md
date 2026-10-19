<div align="center">

<img src="assets/images/logo.png" width="170" alt="Rookie Route Logo" />

# Rookie Route

### AI-powered Code Coaching & Learning Analytics Platform

**단발성 코드 리뷰를 넘어, 반복되는 오류 패턴을 데이터로 축적하여  
초보 개발자의 코딩 습관과 성장 과정을 추적합니다.**

<br/>

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Recharts](https://img.shields.io/badge/Recharts-3.x-22B5BF?style=flat-square)](https://recharts.org/)
[![Alembic](https://img.shields.io/badge/Alembic-DB_Migration-6BA81E?style=flat-square)](https://alembic.sqlalchemy.org/)
[![Sphinx](https://img.shields.io/badge/Sphinx-Docs-000000?style=flat-square&logo=sphinx&logoColor=white)](https://www.sphinx-doc.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI-2088FF?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](LICENSE)

[![Application tests](https://github.com/tangerineYR/rookie-route/actions/workflows/test.yml/badge.svg)](https://github.com/tangerineYR/rookie-route/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/rookie-route-repository/badge/?version=latest)](https://rookie-route-repository.readthedocs.io/en/latest/)

<br/>

[📚 Technical Docs](docs/source/index.rst)
&nbsp;·&nbsp;
[🌐 Project Page](https://tangerineyr.github.io/rookie-route/)
&nbsp;·&nbsp;
[🤝 Contributing](CONTRIBUTING.md)
&nbsp;·&nbsp;
[📚 Original Team Documentation](https://rookie-route-repository.readthedocs.io/en/latest/)

</div>

---

## 📌 Overview

**Rookie Route**는 초보 개발자를 위한 **AI 기반 Code Coaching & Learning Analytics Platform**입니다.

기존의 정적 분석 도구나 일회성 AI 코드 리뷰가 현재 코드의 문제를 찾아내는 데 집중한다면, Rookie Route는 사용자가 반복적으로 발생시키는 오류를 **구조화된 `ErrorType` 데이터로 저장하고 누적 분석**하여 장기적인 개발 습관 개선을 지원하는 것을 목표로 합니다.

```text
단순 AI 답변
    ↓
구조화된 Code Analysis
    ↓
사용자별 Weakness Data 축적
    ↓
Error Pattern Aggregation
    ↓
개인화된 Learning Analytics
```

<table>
  <tr>
    <td><img src="assets/images/main.png" alt="Rookie Route Main" /></td>
    <td><img src="assets/images/analyze.png" alt="Rookie Route Analysis" /></td>
  </tr>
</table>

### Project Info

| 항목 | 내용 |
| --- | --- |
| **프로젝트 유형** | 3인 팀 프로젝트 / Open Source |
| **Repository Activity** | 2025.11.19 – 2025.12.11 |
| **주요 역할** | Backend · AI Integration · Docs as Code · OSS Environment |
| **협업 방식** | GitHub Issue / Branch / Pull Request 기반 협업 |
| **Team Repository** | 154 main-branch commits · 83 merged PRs |
| **My Git History** | 63 author-attributed main commits · 33 merged PRs authored |
| **Backend** | FastAPI · SQLAlchemy · MySQL · JWT |
| **AI** | OpenAI API · JSON Mode · Pydantic Validation |
| **Documentation** | Sphinx · MyST · Mermaid · Jekyll i18n |
| **CI/CD** | GitHub Actions |

> **Portfolio Refactoring**
>
> 본 저장소는 3인 팀 프로젝트의 원본 repository를 기반으로 한 개인 포트폴리오 fork입니다.
> 팀 프로젝트 종료 이후 Authentication/Authorization, Strict AI Response Validation,
> Atomic Transaction, Foreign Key & Cascade, Alembic Migration, Structured Logging,
> Regression Tests 및 GitHub Actions CI를 추가로 보강했습니다.
>
> 이후 실제 구현과 공개 문서 간의 정합성을 다시 검증하여 API Reference,
> Configuration, Technical Documentation, GitHub Pages 콘텐츠와 Repository Hygiene도
> 현재 코드 기준으로 정리했습니다.

---

## 🏗️ Architecture

### Runtime Architecture

```mermaid
flowchart LR
    U[User] --> FE[React + Monaco Editor]

    FE -->|JWT + Code| API[FastAPI]

    API --> AUTH[JWT Authentication]
    API --> REVIEW[Review API]
    API --> DASH[Dashboard API]

    REVIEW -->|async request| AI[OpenAI API]
    AI -->|Structured JSON| VALID[Pydantic Validation]

    VALID --> ORM[SQLAlchemy ORM]
    AUTH --> ORM
    DASH --> ORM

    ORM --> DB[(MySQL)]

    DB --> SUB[Submission]
    DB --> WEAK[Weakness]

    WEAK --> AGG[COUNT / GROUP BY]
    AGG --> DASH
    DASH --> FE
```

### AI Analysis Pipeline

```mermaid
flowchart LR
    A[Source Code] --> B[Input Validation]
    B --> C[AsyncOpenAI]
    C --> D[JSON Response]
    D --> E[AIAnalysisResult]
    E --> F{Schema Valid?}

    F -->|No| G[502 Bad Gateway]
    F -->|Yes| H[Submission + Weakness]

    H --> I[Single DB Transaction]
    I --> J[(MySQL)]
    J --> K[Learning Analytics]
```

AI가 생성한 자연어 응답을 그대로 저장하지 않고,

**`LLM → Strict JSON → Pydantic Domain Model → Relational Data → Analytics`**

흐름으로 변환하여 이후 사용자별 학습 데이터로 재사용할 수 있도록 설계했습니다.

### Documentation Delivery

```mermaid
flowchart LR
    SOURCE[Markdown / Python Source]
    SOURCE --> SPHINX[Sphinx + MyST + Mermaid]
    SPHINX --> RTD[ReadTheDocs]

    SOURCE --> JEKYLL[Jekyll + i18n]
    JEKYLL --> ACTIONS[GitHub Actions]
    ACTIONS --> PAGES[GitHub Pages]
```

---

## 🚀 Engineering Highlights

### 1. LLM의 비정형 응답을 신뢰하지 않는 Structured AI Pipeline

#### Problem

LLM 응답은 JSON 형식을 요청하더라도 필드 누락, 잘못된 타입, 정의되지 않은 Category 등 예상하지 못한 형태를 반환할 수 있습니다.

잘못된 AI 응답이 그대로 DB에 저장되면 Dashboard 통계와 사용자 학습 데이터의 신뢰성까지 훼손될 수 있습니다.

#### Engineering Decision

AI의 결과를 곧바로 persistence layer에 전달하지 않고 **Pydantic을 이용한 명시적인 validation boundary**를 추가했습니다.

```text
OpenAI
  ↓
JSON Object
  ↓
AIAnalysisResult
  ├─ summary: str
  └─ weaknesses: list[AIWeakness]
         ├─ type: ErrorType
         ├─ line: int | null
         └─ explanation: str
  ↓
Validated Domain Data
  ↓
Database
```

`extra='forbid'`, strict type validation, 최대 길이와 배열 개수 제한을 적용했으며, 정의되지 않은 `ErrorType`이나 malformed response는 DB에 도달하기 전에 차단합니다.

#### Impact

- Invalid AI response의 영속화 방지
- AI Prompt와 Backend Domain Model 간 계약 명확화
- Dashboard에서 사용하는 Error Category의 일관성 확보
- AI 결과를 장기적인 Learning Analytics 데이터로 안전하게 재사용

---

### 2. Error Taxonomy를 Single Source of Truth로 통합

#### Problem

AI Prompt, Backend Validation, Database, Dashboard에서 Error Category를 별도로 관리하면 Category가 추가되거나 변경될 때 서로 다른 값을 사용하게 되는 문제가 발생할 수 있습니다.

#### Engineering Decision

공통 `ErrorType Enum`을 정의하고 이를 다음 계층에서 공유하도록 구성했습니다.

```text
ErrorType Enum
   ├── OpenAI System Prompt
   ├── Pydantic Schema
   ├── SQLAlchemy Model
   ├── Database Constraint
   └── Dashboard Response
```

#### Impact

Application 전체가 동일한 Error Taxonomy를 사용하게 되어 **Prompt → Validation → Persistence → Analytics** 간 schema drift 가능성을 줄였습니다.

---

### 3. JWT Identity Binding으로 사용자 데이터 접근 제어

#### Problem

사용자 ID를 URL parameter로 직접 받아 Dashboard 데이터를 조회하면 인증된 사용자가 다른 사용자의 identifier를 전달하여 데이터를 조회할 수 있는 **IDOR(Insecure Direct Object Reference)** 위험이 있습니다.

#### Engineering Decision

기존 사용자 식별자 기반 API 대신 인증된 JWT의 identity를 기준으로 데이터를 조회하도록 변경했습니다.

```text
Before
GET /dashboard/stats/{user_id}

After
GET /dashboard/stats/me
        ↓
JWT Verification
        ↓
current_user
        ↓
Submission.owner_id
```

Review API에서도 request body의 user identifier를 신뢰하지 않고 `current_user.id`를 이용해 Submission ownership을 결정합니다.

JWT decoding 시 signature뿐 아니라 `exp`, `sub` claim을 요구하며 inactive user 역시 차단합니다.

#### Impact

- Client-provided identity에 대한 의존 제거
- Dashboard 데이터의 사용자 간 격리
- Authentication context와 Resource Ownership 연결
- Backend 전반의 authorization policy 일관성 향상

---

### 4. AI 분석 결과를 Atomic Transaction으로 저장

#### Problem

`Submission`을 먼저 commit하고 이후 `Weakness`를 저장하는 구조에서는 두 번째 저장 과정에서 장애가 발생할 경우 분석 기록만 존재하고 세부 결과가 없는 **Partial State**가 생성될 수 있습니다.

#### Engineering Decision

`flush()`로 Submission ID만 확보한 뒤 Weakness 데이터를 모두 추가하고 최종적으로 **한 번만 commit**하도록 변경했습니다.

```text
BEGIN

INSERT Submission
      ↓
    flush()
      ↓
Submission ID 확보
      ↓
INSERT Weakness[]
      ↓
    commit()

ERROR
  ↓
rollback()

END
```

#### Impact

Submission과 Weakness를 하나의 logical unit으로 다루어 **All-or-Nothing 데이터 정합성**을 확보했습니다.

---

### 5. Async LLM Integration + Failure Boundary 설계

FastAPI의 async endpoint에서 `AsyncOpenAI`를 사용하여 외부 LLM API 호출을 비동기 I/O로 처리했습니다.

또한 외부 서비스 장애가 내부 오류와 동일하게 처리되지 않도록 failure case를 분리했습니다.

| Failure | API Response |
| --- | --- |
| Rate Limit | `503 Service Unavailable` |
| Connection / Timeout | `503 Service Unavailable` |
| Upstream API Error | `502 / 503` |
| Invalid AI Response | `502 Bad Gateway` |
| Unexpected Failure | `500 Internal Server Error` |

`timeout`과 제한된 `max_retries`를 설정해 외부 API 호출이 무한정 요청을 점유하지 않도록 했습니다.

사용자의 Source Code와 API Key가 오류 로그를 통해 유출되지 않도록 exception body를 직접 출력하지 않고 allowlist 기반 **Structured Logging**을 적용했습니다.

```json
{
  "level": "WARNING",
  "logger": "services.analyzer",
  "event": "ai_api_failure",
  "status": 500
}
```

---

### 6. Relational Integrity를 ORM 관계에서 Database까지 확장

기존 identifier 중심의 관계를 실제 Foreign Key 기반 관계로 변경했습니다.

```text
User
  │ 1
  │
  ▼ N
Submission
  │ 1
  │
  ▼ N
Weakness
```

`ForeignKey`, `relationship`, `back_populates`, `delete-orphan`, `ON DELETE CASCADE`를 함께 적용하여 ORM을 우회한 SQL delete에서도 관계 무결성이 유지되도록 했습니다.

사용자 삭제 시 연결된 Submission과 Weakness가 남는 orphan data도 방지합니다.

---

### 7. Alembic으로 Schema Versioning 및 Legacy Data Migration

Application startup에서 `Base.metadata.create_all()`로 schema를 생성하는 방식 대신 **Alembic 기반 migration**으로 전환했습니다.

기존 데이터가 존재하는 환경도 고려해 migration 과정에서 legacy identifier를 새로운 `owner_id` Foreign Key 구조로 변환하도록 구성했습니다.

특히 유효하지 않은 legacy ownership 또는 지원하지 않는 Error Category가 발견될 경우 migration을 중단하여 데이터 손실을 방지하도록 regression test를 작성했습니다.

```text
Legacy Schema
     ↓
Preflight Validation
     ↓
Ownership Backfill
     ↓
Foreign Key Migration
     ↓
Current Schema
```

이를 통해 DB schema 변경을 코드와 함께 version control할 수 있도록 개선했습니다.

---

### 8. DB-side Aggregation으로 Learning Analytics 생성

사용자의 모든 Weakness row를 Application Memory로 가져와 Python에서 집계하지 않고 Database에서 직접 집계합니다.

```sql
SELECT weaknesses.type, COUNT(weaknesses.id)
FROM weaknesses
JOIN submissions
  ON weaknesses.submission_id = submissions.id
WHERE submissions.owner_id = :current_user_id
GROUP BY weaknesses.type
ORDER BY COUNT(weaknesses.id) DESC;
```

이를 통해 Dashboard API는 사용자별 총 분석 횟수와 Error Category 빈도를 제공하며, 반복적으로 발생하는 약점 패턴을 시각화할 수 있습니다.

---

### 9. SQLite + MySQL Regression Test를 GitHub Actions에 통합

리팩토링 과정에서 인증, 데이터 정합성, AI validation 등의 동작이 다시 깨지지 않도록 automated regression test를 추가했습니다.

주요 검증 대상은 다음과 같습니다.

```text
Authentication
├─ Signup / Login
├─ Duplicate username & email
├─ Input validation
├─ Expired / malformed JWT
└─ Inactive user

AI Pipeline
├─ Invalid JSON rejection
├─ Unknown ErrorType rejection
├─ Timeout / Rate Limit mapping
├─ API failure mapping
└─ Missing API configuration

Persistence
├─ Atomic rollback
├─ Foreign Key
├─ ON DELETE CASCADE
├─ Orphan removal
└─ Category constraint

Migration
├─ Fresh migration
├─ Upgrade / Downgrade
├─ Legacy data backfill
└─ Invalid legacy data protection
```

GitHub Actions에서는 push와 Pull Request마다 다음 Quality Gate를 자동 실행합니다.

```text
Backend
├─ Dependency validation
├─ SQLite regression tests
├─ MySQL regression tests
└─ Alembic migration tests

Frontend
├─ npm test
└─ npm run build
```

---

## 🛠️ Tech Stack

| Category | Technology | Usage |
| --- | --- | --- |
| **Backend** | FastAPI | REST API, Dependency Injection, async endpoint |
| **Language** | Python | Backend application |
| **ORM** | SQLAlchemy | Relational modeling, query, aggregation |
| **Database** | MySQL | User, Submission, Weakness persistence |
| **Migration** | Alembic | Schema versioning, legacy migration |
| **AI** | OpenAI API | Code analysis and structured feedback |
| **Validation** | Pydantic | API contract and AI response validation |
| **Authentication** | OAuth2, JWT, bcrypt | Authentication and identity binding |
| **Frontend** | React, Vite | SPA client |
| **Editor** | Monaco Editor | Source code input |
| **Visualization** | Recharts | Weakness statistics visualization |
| **Testing** | pytest, Node Test Runner | Backend / Frontend regression tests |
| **Documentation** | Sphinx, MyST, Mermaid | API and architecture Docs as Code |
| **Docs Hosting** | ReadTheDocs | Technical documentation deployment |
| **CI/CD** | GitHub Actions | Test, build, Jekyll deployment |
| **OSS** | Jekyll i18n | Korean / English project pages |

---

## 📂 Project Structure

```text
rookie-route/
│
├── app/
│   ├── backend/
│   │   ├── core/
│   │   │   ├── config.py          # Pydantic Settings
│   │   │   ├── logging.py         # Structured logging
│   │   │   └── security.py        # JWT / bcrypt
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py            # Signup / Login
│   │   │   ├── review.py          # AI analysis persistence
│   │   │   └── dashboard.py       # Learning analytics
│   │   │
│   │   ├── services/
│   │   │   └── analyzer.py        # AsyncOpenAI integration
│   │   │
│   │   ├── migrations/            # Alembic migrations
│   │   ├── tests/                 # Backend regression tests
│   │   ├── models.py              # SQLAlchemy ORM
│   │   ├── schemas.py             # Pydantic contracts
│   │   ├── error_types.py         # Error taxonomy
│   │   ├── database.py            # DB session lifecycle
│   │   └── back_main.py           # FastAPI entry point
│   │
│   └── frontend/
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   └── lib/
│       └── package.json
│
├── docs/
│   └── source/                     # Sphinx / MyST documentation
│
├── .github/
│   └── workflows/
│       ├── test.yml                # Backend / Frontend CI
│       └── jekyll.yml              # GitHub Pages deployment
│
├── _i18n/                          # Korean / English localization
├── CONTRIBUTING.md                 # Contribution workflow
├── CODE_OF_CONDUCT.md
└── README.md
```

---

## ⚡ Quick Start

### Prerequisites

- Python **3.11+**
- Node.js **24**
- MySQL **8.0+**
- OpenAI API Key

### 1. Clone

```bash
git clone https://github.com/tangerineYR/rookie-route.git
cd rookie-route
```

### 2. Backend

```bash
python -m venv venv
```

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

```bash
cd app/backend
pip install -r requirements.txt
```

`.env.example`을 복사하여 `.env`를 생성한 후 필요한 값을 설정합니다.

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/rookie_route

SECRET_KEY=your_secure_random_secret
```

`SECRET_KEY`는 다음과 같이 생성할 수 있습니다.

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

DB schema를 적용합니다.

```bash
python -m alembic upgrade head
```

Backend를 실행합니다.

```bash
uvicorn back_main:app --reload
```

API Documentation:

```text
http://localhost:8000/docs
```

### 3. Frontend

프로젝트 root에서 Node.js 버전을 맞춥니다.

```bash
nvm use
```

```bash
cd app/frontend
npm ci
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 📚 Documentation & OSS

Rookie Route는 코드뿐 아니라 프로젝트 운영 과정도 repository 안에서 관리하는 **Docs as Code** 방식을 적용했습니다.

- **Sphinx + MyST** — Technical Documentation
- **Mermaid** — Architecture Diagram
- **ReadTheDocs** — Documentation Hosting
- **GitHub Actions** — Automatic Build / Deployment
- **Jekyll + i18n** — Korean / English Project Page
- **CONTRIBUTING.md** — Branch / Commit / PR Contribution Workflow
- **CODE_OF_CONDUCT.md** — Open Source Community Guidelines

자세한 기술 문서는 [`docs/source/`](docs/source/)에서 확인할 수 있습니다.

---

## 🤝 Contribution

Contribution workflow와 개발 규칙은 [`CONTRIBUTING.md`](CONTRIBUTING.md)를 참고해 주세요.

이 프로젝트는 Pull Request 기반의 협업 방식을 사용하며 Issue → Branch → Commit → Pull Request → Review 흐름을 권장합니다.

---

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).

---

<div align="center">

### Rookie Route

**Fixing one bug is useful.  
Understanding why you keep making it is better.**

</div>
