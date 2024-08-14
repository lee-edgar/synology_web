import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from sqlalchemy import insert
import logging

# FastAPI 앱 생성
app = FastAPI()

# SQLAlchemy 설정
DATABASE_URL = "mysql+mysqlconnector://forkwntkd:Gksdud9392!!@218.235.38.85:3307/test"

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# players 테이블 매핑
class Player(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))  # 테이블의 실제 컬럼에 맞춤

class PlayerInput(BaseModel):
    player_id: int
    name: str
    position : str
    nationality : str
    club : str

from sqlalchemy import Table, Column, Integer, String, MetaData
metadata = MetaData()
Player = Table(
    'players', metadata,
    Column('player_id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('position', String(50)),
    Column('nationality', String(50)),
    Column('club', String(100))
)


# 플레이어 이름 조회
@app.get("/players/{player_id}")
async def get_player_name(player_id: int) -> Optional[dict]:
    try:
        with engine.connect() as connection:
            # player_id에 해당하는 이름을 선택
            query = select(Player.c.name).where(Player.c.player_id == player_id)
            result = connection.execute(query).first()
            if result:
                return {"name": result[0]}
            else:
                raise HTTPException(status_code=404, detail="Player not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/players/")
async def add_player(player: PlayerInput):
    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                query = insert(Player).values(
                    player_id=player.player_id,
                    name=player.name,
                    position=player.position,
                    nationality=player.nationality,
                    club=player.club
                )
                connection.execute(query)
                transaction.commit()  # 트랜잭션 커밋
                return {"message": "Player added successfully"}
            except SQLAlchemyError as e:
                transaction.rollback()  # 오류 발생 시 롤백
                logging.error(f"Error occurred: {str(e)}")
                raise HTTPException(status_code=500, detail="Database error")
    except SQLAlchemyError as e:
        logging.error(f"Connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



# 기본 라우트
@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(
        "uvicorn_test:app",  # "파일명:앱인스턴스"
        host="127.0.0.1",      # 모든 인터페이스에서 접근 허용
        port=8000,           # 포트 설정
        reload=True          # 코드 변경 시 자동으로 서버를 재시작
    )
