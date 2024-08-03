import uvicorn
from fastapi import FastAPI
from typing import Union


# 임시 FastAPI 앱 생성
app = FastAPI()

# 간단한 라우트 정의
@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    # Uvicorn 서버 실행
    uvicorn.run(
        "uvicorn_test:app",  # "파일명:앱인스턴스"
        host="127.0.0.1",
        port=8000,
        reload=True  # 코드 변경 시 자동으로 서버를 재시작
    )

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}