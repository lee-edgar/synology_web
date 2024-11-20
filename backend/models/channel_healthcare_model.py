from sqlalchemy import Column, Integer, String, DateTime, Enum, Float
# from backend.db.session import Base
from sqlalchemy.sql import func
from backend.models.base import Base

class CGMHistory(Base):
    __tablename__ = "ch_cgm_history"

    user_uid = Column(Integer, nullable=False)
    std_time = Column(DateTime, nullable=False)
    cgm_type = Column(String(50), nullable=False)
    bg = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    collector = Column(String(50), nullable=False)
    device_number = Column(String(100))
    device_serial = Column(String(100))
    regist_time = Column(DateTime, nullable=False)
    modifier_uid = Column(Integer)
    modifiy_time = Column(DateTime, nullable=False)

    # def __repr__(self):
    #     return f"<CGMHistory(id={self.id}, user_uid={self.user_uid}, std_time={self.std_time})>"

class EXERCISE_History(Base):
    __tablename__ = "ch_exercise_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_uid = Column(Integer, nullable=False)
    type_id = Column(Integer, nullable=False)
    summary_id = Column(String(100), nullable=False)
    upload_type = Column(String(20), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    bmr_calories = Column(Float, nullable=False)
    total_calories = Column(Float, nullable=False)
    distance = Column(Integer, nullable=False)
    steps = Column(Integer, nullable=False)
    step_type = Column(String(20), nullable=False)
    heart_rate_min = Column(Integer, nullable=False)
    heart_rate_max = Column(Integer, nullable=False)
    heart_rate_avg = Column(Integer, nullable=False)
    speed_max = Column(Float, nullable=False)
    speed_avg = Column(Float, nullable=False)
    regist_time = Column(DateTime, nullable=False)
    modifier_uid = Column(Integer)
    modify_time = Column(DateTime, nullable=False)
    consecutive_days = Column(Integer, nullable=False)




