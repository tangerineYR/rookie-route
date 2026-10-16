@echo off
echo Starting Rookie Route Servers...

:: 백엔드 실행 (새 창에서 열림)
start "Backend Server" cmd /k "call venv\Scripts\activate && cd app\backend && alembic upgrade head && uvicorn back_main:app --reload"

:: 프론트엔드 실행 (새 창에서 열림)
start "Frontend Server" cmd /k "cd app\frontend && npm run dev"

echo All servers are starting...
echo You can close this window now, or keep it open.