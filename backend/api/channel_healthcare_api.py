from datetime import datetime
from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.db.session import get_db
from backend.schemas.channel_healthcare_schemas import CGMHistoryBase, CGMHistoryResponse, EXERCISEHistoryResponse, MEDICINEHistoryResponse, MEALHistoryResponse
from backend.models.channel_healthcare_model import CGMHistory as CGMHistoryModel
from backend.models.channel_healthcare_model import EXERCISE_History as EXERCISE_HistoryModel
from backend.models.channel_healthcare_model import MEALS_History as MEAL_HistoryModel
from backend.models.channel_healthcare_model import MEDICINE_History as MEDICINE_HistoryModel


router = APIRouter()

@router.get("/cgm", response_model=List[CGMHistoryResponse], tags=["ChannelHealthcare"])
def read_cgm(user_uid : int, start_date : datetime, end_date:datetime, db : Session = Depends(get_db)):
    '''
    CGM History 정보를 조회하는 엔드포인트
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

@router.get("/exercise", response_model=List[EXERCISEHistoryResponse], tags=["ChannelHealthcare"])
def read_exercise(user_uid : int, start_date : datetime, end_date:datetime, db : Session = Depends(get_db)):
    '''
    Exercise History 정보를 조회하는 엔드포인트
    Args:
       user_uid: 사용자 ID
       start_date: 조회 시작 날짜
       end_date: 조회 종료 날짜
    :return:
        특정 user_uid의 지정된 기간 동안의 운동 기록 데이터
    '''

    try :
        exercise_data = db.query(EXERCISE_HistoryModel).filter(
            EXERCISE_HistoryModel.user_uid == user_uid,
            EXERCISE_HistoryModel.start_time <= end_date,  # 운동 시작 시간이 조회 종료일 이전
            EXERCISE_HistoryModel.end_time >= start_date   # 운동 종료 시간이 조회 시작일 이후
        ).order_by(EXERCISE_HistoryModel.start_time).all()
        if not exercise_data:
            raise HTTPException(status_code=404, detail="No exercise data found for this user in the given time range")
        return exercise_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    return exercise_data

@router.get("/meal", response_model=List[MEALHistoryResponse], tags=["ChannelHealthcare"])
def read_meal(user_uid : int, start_date : datetime, end_date:datetime, db : Session = Depends(get_db)):
    '''
    Meal History 정보를 조회하는 엔드포인트
    Args:
       user_uid: 사용자 ID
       start_date: 조회 시작 날짜
       end_date: 조회 종료 날짜
    :return:
        특정 user_uid의 지정된 기간 동안의 식사 기록 데이터
    '''


    try :
        meal_data = db.query(MEAL_HistoryModel).filter(
            MEAL_HistoryModel.user_uid == user_uid,
            MEAL_HistoryModel.start_time <= end_date,  # 식사 시작 시간이 조회 종료일 이전
            MEAL_HistoryModel.end_time >= start_date   # 식사 종료 시간이 조회 시작일 이후
        ).order_by(MEAL_HistoryModel.start_time).all()
        if not meal_data:
            raise HTTPException(status_code=404, detail="No meal data found for this user in the given time range")
        return meal_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    return meal_data


@router.get("/medicine", response_model=List[MEDICINEHistoryResponse], tags=["ChannelHealthcare"])
def read_medicine(user_uid : int, regist_time : datetime, db : Session = Depends(get_db)):
    '''
    medicine History 정보를 조회하는 엔드포인트
    Args:
       user_uid: 사용자 ID
       start_date: 조회 시작 날짜
       end_date: 조회 종료 날짜
    :return:
        특정 user_uid의 지정된 기간 동안의 복약 기록 데이터
    '''

    try:
        # start_time의 날짜 범위 계산
        # start_of_day = datetime.combine(start_date.date(), datetime.min.time())  # 2023-11-01 00:00:00
        # end_of_day = datetime.combine(start_time.date(), datetime.max.time())  # 2023-11-01 23:59:59
        end_date = datetime.combine(regist_time.date(), datetime.max.time())  # 2023-11-01 23:59:59

        # 데이터 필터링
        # medicine_data = db.query(MEDICINE_HistoryModel).filter(
        #     MEDICINE_HistoryModel.user_uid == user_uid,
        #     MEDICINE_HistoryModel.regist_time.between(start_of_day, end_of_day)  # 날짜 범위 필터링
        # ).order_by(MEDICINE_HistoryModel.regist_time).all()

        medicine_data = db.query(MEDICINE_HistoryModel).filter(
            MEDICINE_HistoryModel.user_uid == user_uid
        ).order_by(MEDICINE_HistoryModel.regist_time).all()

        # medicine_data = db.query(MEDICINE_HistoryModel).filter(
        #     MEDICINE_HistoryModel.user_uid == user_uid,
        #     MEDICINE_HistoryModel.regist_time <= end_date,  # 식사 시작 시간이 조회 종료일 이전
        #     MEDICINE_HistoryModel.end_date >= regist_time   # 식사 종료 시간이 조회 시작일 이후
        # ).order_by(MEDICINE_HistoryModel.regist_time).all()

        if not medicine_data:
            raise HTTPException(status_code=404, detail="No medicine data found for this user on the given date")

        return medicine_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    return medicine_data