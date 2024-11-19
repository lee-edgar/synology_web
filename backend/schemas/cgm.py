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

