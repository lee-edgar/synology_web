from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.content import router as content_router

app = FastAPI(title="Portfolio API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit 앱 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(content_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "API is running"}