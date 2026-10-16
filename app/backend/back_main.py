from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from core.logging import configure_logging
from routers import review, dashboard, auth

# Validate required configuration at startup; schema changes use Alembic.
get_settings()
configure_logging()

app = FastAPI(
    title="RookieRoute",
    description="OpenAI와 FastAPI, MySQL을 활용한 코드 리뷰 및 약점 분석 프로젝트",
    version="1.0.0"
)

# CORS 설정 - 프론트엔드와 통신 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Vite 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(review.router)
app.include_router(dashboard.router)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "RookieRoute 서버가 정상적으로 실행 중입니다."}