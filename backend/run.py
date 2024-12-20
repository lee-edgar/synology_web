import uvicorn
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.common.common import BACKEND_HOST


if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # "파일명:앱인스턴스"
        host=BACKEND_HOST,  # 모든 인터페이스에서 접근 허용
        port=8000,  # 포트 설정
        log_level="info", # 로깅 레벨 설정
        reload=True  # 코드 변경 시 자동으로 서버를 재시작
    )