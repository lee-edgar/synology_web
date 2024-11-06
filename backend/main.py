from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.content import router as content_router

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.common.common import BACKEND_HOST
from db.session import engine
from models.base import Base
from api.career import router as carrer_router
from contextlib import asynccontextmanager


# 1. FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(title="Portfolio API")

# 2. Middleware 설정 streamlit(8501)에서 오는 요청을 허용하는 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{BACKEND_HOST}:8501"],  # Streamlit 앱 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 라우터 등록
app.include_router(content_router, prefix="/api")
app.include_router(carrer_router, prefix="/api") # career 관련 모든 엔드포인트 설정



@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    등록된 모든 라우트를 콘솔에 출력 (디버깅에 유용)
    Base.metadata.create_all(bind=engine)로 DB 테이블 자동 생성
    없어도 되지만, 개발할 때 도움이 되는 정보를 제공합니다.

    '''
    # 시작 시 실행
    print("Registered routes:")
    for route in app.routes:
        print(f"  {route.path} [{route.methods}]")
    Base.metadata.create_all(bind=engine)
    yield


@app.get("/server_sync")
async def root():
    """
    API 서버 상태를 체크하는 헬스체크 엔드포인트

    Returns:
        dict: 서버 상태 메시지
    """
    return {"message": "API is running"}