from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB 연결 URL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://forkwntkd:Gksdud9392!!@218.235.38.85:3307/test"

# 엔진 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 세션 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 세션 의존성
def get_db():
    db = SessionLocal() #db session 생성
    try:
        yield db
    finally:
        db.close()