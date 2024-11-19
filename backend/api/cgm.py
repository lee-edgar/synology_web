from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.db.session import get_db
from backend.schemas.cgm import CGMHistoryBase, CGMHistoryResponse
from backend.models.cgm import CGMHistory as CGMHistoryModel

router = APIRouter()

@router.get("/cgm", response_model=List[CGMHistoryResponse], tags=["CGM"])
def read_cgm(user_uid : int, db : Session = Depends(get_db)):
    '''
    CGM History 정보를 조회하는 엔드포인트
    :return:
        특정 user_uid에 맞는 연속혈당 데이터 리턴
    '''
    try:
        cgm_data = db.query(CGMHistoryModel).filter(CGMHistoryModel.user_uid == user_uid).all()
        if not cgm_data:
            raise HTTPException(status_code=404, detail='no cgm data found for this user')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return db.query(CGMHistoryModel).all()
