from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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