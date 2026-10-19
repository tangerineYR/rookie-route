# 핵심 기능

Rookie Route는 반복되는 AI 코드 리뷰 결과를 구조화된 학습 데이터로 변환하고,
사용자별로 누적하여 반복적인 오류 패턴을 확인할 수 있도록 설계한 플랫폼입니다.

---

## 🤖 AI 기반 코드 분석

사용자는 Monaco Editor에서 코드를 작성하거나 붙여넣은 뒤 AI 분석을 요청할 수 있습니다.

Backend는 다음 정보를 구조화하여 반환합니다.

- 분석 요약
- 발견된 약점
- 제한된 오류 카테고리
- 가능한 경우 관련 코드 라인
- 각 약점에 대한 설명

AI 응답은 데이터베이스에 저장되기 전에 검증됩니다.

---

## 🧩 구조화된 오류 분류

Rookie Route는 AI Prompt, Pydantic Validation, Database Model,
Dashboard에서 동일한 `ErrorType` 분류 체계를 사용합니다.

현재 카테고리는 다음과 같습니다.

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

이를 통해 AI가 임의의 오류 유형을 생성하여 장기 통계에 섞이는 것을 방지합니다.

---

## 💾 학습 데이터 축적

분석에 성공한 코드는 `Submission`으로 저장되고,
분석된 문제들은 관련된 `Weakness` 레코드로 저장됩니다.

```text
User
  └─ Submission
       └─ Weakness[]
```

이를 통해 한 번의 AI 응답을 여러 제출에 걸쳐 집계할 수 있는
구조화된 학습 데이터로 변환합니다.

---

## 📊 개인 오류 패턴 분석

인증된 사용자의 누적 `Weakness` 데이터를 데이터베이스에서 집계하여
다음 정보를 제공합니다.

- 총 코드 분석 횟수
- 오류 카테고리별 발생 횟수
- 가장 자주 발생한 오류
- 오류 유형 분포

검증되지 않은 종합 점수를 부여하는 대신 실제 누적 오류 패턴을 보여줍니다.

---

## 🕘 최근 분석 기록

코드 분석 화면에서는 최근 최대 20개의 분석 결과를 browser `localStorage`에 저장합니다.

이를 통해 최근 분석한 코드를 빠르게 다시 불러올 수 있습니다.

이 기록은 서버에 저장되는 `Submission` / `Weakness` 학습 데이터와는 별개의
Client-side History입니다.

---

## 🔐 인증 기반 사용자 데이터

회원가입과 로그인은 FastAPI Backend에서 처리하며 JWT 인증을 사용합니다.

코드 분석 결과의 소유자는 Client가 전달하는 사용자 ID가 아니라
인증된 사용자 정보에서 결정합니다.

Dashboard 역시 현재 로그인한 사용자의 통계만 반환합니다.

---

## 🛠️ 기술 스택

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
