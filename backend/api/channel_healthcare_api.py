from datetime import datetime
from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.db.session import get_db
from backend.schemas.channel_healthcare_schemas import CGMHistoryBase, CGMHistoryResponse, EXERCISEHistoryResponse, MEDICINEHistoryResponse, MEALHistoryResponse, MEALFOODHistoryResponse
from backend.models.channel_healthcare_model import CGMHistory as CGMHistoryModel, MEALFOOD_History
from backend.models.channel_healthcare_model import EXERCISE_History as EXERCISE_HistoryModel
from backend.models.channel_healthcare_model import MEALS_History as MEAL_HistoryModel
from backend.models.channel_healthcare_model import MEDICINE_History as MEDICINE_HistoryModel
from backend.models.channel_healthcare_model import MEALFOOD_History as MEALFOOD_HistoryModel
from loguru import logger


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

    try:
        # 로그: 매개변수 확인
        logger.info(f"Fetching exercise data for user_uid: {user_uid}, start_date: {start_date}, end_date: {end_date}")

        # 데이터베이스 쿼리
        exercise_data = db.query(EXERCISE_HistoryModel).filter(
            EXERCISE_HistoryModel.user_uid == user_uid,
            EXERCISE_HistoryModel.start_time <= end_date,  # 운동 시작 시간이 조회 종료일 이전
            EXERCISE_HistoryModel.end_time >= start_date  # 운동 종료 시간이 조회 시작일 이후
        ).order_by(EXERCISE_HistoryModel.start_time).all()

        # 데이터가 없을 경우 404 반환
        if not exercise_data:
            logger.warning(f"No exercise data found for user_uid {user_uid} between {start_date} and {end_date}")
            raise HTTPException(
                status_code=404,
                detail=f"No exercise data found for user_uid {user_uid} between {start_date} and {end_date}"
            )

        # 데이터가 있는 경우 반환
        logger.info(f"Fetched {len(exercise_data)} exercise records for user_uid {user_uid}.")
        return exercise_data

    except HTTPException as e:
        # HTTPException은 그대로 반환
        raise e

    except Exception as e:
        # 예상치 못한 오류: 500 반환
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

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
    try:
        # 로그: 매개변수 확인
        logger.info(f"Fetching exercise data for user_uid: {user_uid}, regist_time: {regist_time}")
        end_date = datetime.combine(regist_time.date(), datetime.max.time())  # 2023-11-01 23:59:59

        medicine_data = db.query(MEDICINE_HistoryModel).filter(
            MEDICINE_HistoryModel.user_uid == user_uid
        ).order_by(MEDICINE_HistoryModel.regist_time).all()

        # 데이터가 없을 경우 404 반환
        if not medicine_data:
            logger.warning(f"No exercise data found for user_uid {user_uid} {regist_time}")
            raise HTTPException(
                status_code=404,
                detail=f"No exercise data found for user_uid {user_uid} {regist_time}"
            )

        # 데이터가 있는 경우 반환
        logger.info(f"Fetched {len(medicine_data)} exercise records for user_uid {user_uid}.")
        return medicine_data

    except HTTPException as e:
        # HTTPException은 그대로 반환
        raise e

    except Exception as e:
        # 예상치 못한 오류: 500 반환
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

    return medicine_data

@router.get("/meal_food", response_model=List[MEALFOODHistoryResponse], tags=["ChannelHealthcare"])
def read_meal_food(meal_id : int, db : Session = Depends(get_db)):
    try:
        mealfood_data = db.query(MEALFOOD_HistoryModel).filter(
            MEALFOOD_History.meal_id == meal_id
        ).order_by(MEALFOOD_History.meal_id).all()

        # 데이터가 없을 경우 404 반환
        if not mealfood_data:
            logger.warning(f"No meal_food data found for meal_id {meal_id}")
            raise HTTPException(
                status_code=404,
                detail=f"No meal_food data found for meal_id {meal_id}"
            )

        # 데이터가 있는 경우 반환
        logger.info(f"Fetched {len(mealfood_data)} meal_food records for meal_id {meal_id}.")
        return mealfood_data

    except HTTPException as e:
        # HTTPException은 그대로 반환
        raise e

    except Exception as e:
        # 예상치 못한 오류: 500 반환
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    return mealfood_data

