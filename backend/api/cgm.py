from datetime import datetime
from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.db.session import get_db
from backend.schemas.cgm import CGMHistoryBase, CGMHistoryResponse
from backend.models.cgm import CGMHistory as CGMHistoryModel

router = APIRouter()

@router.get("/cgm", response_model=List[CGMHistoryResponse], tags=["CGM"])
def read_cgm(user_uid : int, start_date : datetime, end_date:datetime, db : Session = Depends(get_db)):
    '''
    CGM History 정보를 조회하는 엔드포인트
    Args:
       user_uid: 사용자 ID
       start_date: 조회 시작 날짜
       end_date: 조회 종료 날짜
    :return:
        특정 user_uid의 지정된 기간 동안의 연속혈당 데이터
    '''
    try:
        cgm_data = db.query(CGMHistoryModel).filter(
            CGMHistoryModel.user_uid == user_uid,
            CGMHistoryModel.std_time.between(start_date, end_date)
        ).order_by(CGMHistoryModel.std_time).all()
        if not cgm_data:
            raise HTTPException(status_code=404, detail='no cgm data found for this user')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return cgm_data