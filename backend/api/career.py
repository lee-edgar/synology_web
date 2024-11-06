"""
경력 정보에 대한 CRUD(Create, Read, Update, Delete) 작업을 처리하는 라우터입니다.
backend/main.py의 app.include_router(career_router, prefix="/api")를 통해 등록되며,
데이터베이스와 직접 상호작용하여 경력 정보를 관리합니다.

각 엔드포인트는 다음과 같은 프로세스를 따릅니다:
1. API 요청 수신
2. DB 세션 생성 (get_db 의존성)
3. CareerModel을 통한 DB 작업
4. Pydantic 모델(Career)을 통한 응답 데이터 검증
5. 결과 반환

Routes:
    POST   /api/careers/          : 새로운 경력 정보 생성
    GET    /api/careers/          : 모든 경력 정보 조회
    GET    /api/careers/{id}      : 특정 경력 정보 조회
    PUT    /api/careers/{id}      : 경력 정보 수정
    DELETE /api/careers/{id}      : 경력 정보 삭제
"""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.db.session import get_db
from backend.schemas.carrer import CareerBase, CareerCreate, Career
from backend.models.carrer import Career  as CareerModel
import json

router = APIRouter()


@router.post("/create_careers/", response_model=Career)
def create_career(career: CareerCreate, db: Session = Depends(get_db)):
    '''
    1. title: 경력의 타이틀입니다.
    2. company: 회사명입니다.
    3. company_type: 회사의 유형입니다. 예시로는 스타트업, 법인 등이 있습니다.
    4. start_date: 고용 시작일입니다.
    5. end_date: 고용 종료일입니다. 현재 근무 중인 경우 선택 사항입니다.
    6. location: 고용 지역입니다.
    7. description: 업무에 대한 상세 설명입니다.
    8. tags: 경력과 관련된 태그 목록을 쉼표(`,`)로 구분하여 입력합니다.
    9. files: 경력과 관련된 파일 목록을 쉼표(`,`)로 구분하여 입력합니다. 각 파일은 쉼표로 구분된 세 가지 정보로 구성됩니다:
        - 첫 번째 값: 파일 이름
        - 두 번째 값: 파일 유형 (예: `image` 또는 `pdf`)
        - 세 번째 값: 파일에 대한 간단한 설명

    1. **DB 세션 생성**: `Depends(get_db)`를 통해 `db/session.py`의 `SessionLocal()` 실행
    2. **쿼리 실행**: `CareerModel` (`models/career.py`)을 기반으로 DB에서 경력 정보를 조회
    3. **결과 반환**: 경력 정보를 `start_date` 기준으로 내림차순 정렬하여 반환

    Returns:
        List[CareerResponse]: 경력 정보의 목록을 반환
    '''
    db_career = CareerModel(**career.model_dump())
    db.add(db_career)
    db.commit()
    db.refresh(db_career)
    return db_career





@router.get("/careers/", response_model=List[Career])
def read_careers(db: Session = Depends(get_db)):
    '''
    모든 경력 정보를 조회하는 엔드포인트
    1. DB 세션 생성: Depends(get_db)를 통해 db/session.py의 SessionLocal() 실행
    2. 쿼리 실행: CareerModel(models/career.py)을 기반으로 DB 조회
    3. 결과 반환: 경력 정보를 start_date 기준 내림차순으로 정렬하여 반환

    :return:
        List[Carrer] : 경력 정보 목록
    '''
    careers = db.query(CareerModel).order_by(CareerModel.start_date.desc()).all()
    return careers


@router.get("/careers/{career_id}", response_model=Career)
def read_career(career_id: int, db: Session = Depends(get_db)):
    """특정 경력 정보 조회"""
    career = db.query(CareerModel).filter(CareerModel.id == career_id).first()
    if career is None:
        raise HTTPException(status_code=404, detail="Career not found")
    return career


@router.put("/careers/{career_id}", response_model=Career)
def update_career(career_id: int, career: CareerCreate, db: Session = Depends(get_db)):
    """경력 정보 수정"""
    db_career = db.query(CareerModel).filter(CareerModel.id == career_id).first()
    if db_career is None:
        raise HTTPException(status_code=404, detail="Career not found")

    for key, value in career.model_dump().items():
        setattr(db_career, key, value)

    db.commit()
    db.refresh(db_career)
    return db_career


@router.delete("/careers/{career_id}")
def delete_career(career_id: int, db: Session = Depends(get_db)):
    """경력 정보 삭제"""
    career = db.query(CareerModel).filter(CareerModel.id == career_id).first()
    if career is None:
        raise HTTPException(status_code=404, detail="Career not found")

    db.delete(career)
    db.commit()
    return {"message": "Career deleted successfully"}