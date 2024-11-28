from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class CGMHistoryBase(BaseModel):
    user_uid: int
    std_time: datetime
    cgm_type: str
    collector: str
    bg: int
    device_number: Optional[str] = None
    device_serial: Optional[str] = None
    regist_time: datetime
    modifier_uid: Optional[int] = None
    modifiy_time: datetime

class CGMHistoryResponse(CGMHistoryBase):
    id: int

    class Config:
        from_attributes = True

class EXERCISEHistoryBase(BaseModel):
    user_uid: int
    id : int
    type_id : int
    summary_id : str
    upload_type : str
    start_time : datetime
    end_time : datetime
    bmr_calories : float
    total_calories : float
    distance : int
    steps : int
    step_type : str
    heart_rate_min : int
    heart_rate_max : int
    heart_rate_avg : int
    speed_max : float
    speed_avg : float
    regist_time : datetime
    modifier_uid : Optional[int] = None
    modify_time : datetime
    consecutive_days : int

class EXERCISEHistoryResponse(EXERCISEHistoryBase):
    id: int

    class Config:
        from_attributes = True

class MEALHistoryBase(BaseModel):
    id : int
    meal_id : int
    user_uid : int
    meal_div_code: Literal['BREAKFAST', 'LUNCH', 'DINNER', 'SNACK']  # 제한된 값 사용
    start_time : datetime
    end_time : datetime
    meal_duration : int
    bg_point : int
    bg_point_percent : int
    top_bg : int
    top_bg_percent : int
    vary_bg : int
    vary_bg_percent : int
    tir  : int
    tir_percent : int
    start_bg : int
    start_bg_percent : int
    food_info : str
    meal_desc : str
    memo : str
    append_count : int
    push_alarm : int
    regist_time : datetime
    modifier_uid : Optional[str] = None
    modify_time : datetime
    # pegist_time : Optional[str] = None

class MEALHistoryResponse(MEALHistoryBase):
    id: int

    class Config:
        from_attributes = True


class MEDICINEHistoryBase(BaseModel):
    id : int
    user_uid : int
    name : str
    regist_time : datetime
    modify_time : datetime
    company : str
    created_at : Optional[datetime] = None

class MEDICINEHistoryResponse(MEDICINEHistoryBase):
    id: int

    class Config:
        from_attributes = True