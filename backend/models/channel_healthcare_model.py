from sqlalchemy import Column, Integer, String, DateTime, Float
# from backend.db.session import Base
from sqlalchemy.sql import func
from backend.models.base import Base
from sqlalchemy.dialects.mysql import ENUM  # MySQL ENUM 타입 사용
from datetime import datetime

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


class MEALS_History(Base):
    __tablename__ = "ch_meals_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meal_id = Column(Integer, nullable=False)
    user_uid = Column(Integer, nullable=False)
    meal_div_code = Column(ENUM('BREAKFAST', 'LUNCH', 'DINNER', 'SNACK'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    meal_duration = Column(Integer, nullable=False)
    bg_point = Column(Integer, nullable=False)
    bg_point_percent = Column(Integer, nullable=False)
    top_bg = Column(Integer, nullable=False)
    top_bg_percent = Column(Integer, nullable=False)
    vary_bg = Column(Integer, nullable=False)
    vary_bg_percent = Column(Integer, nullable=False)
    tir = Column(Integer, nullable=False)
    tir_percent = Column(Integer, nullable=False)
    start_bg = Column(Integer, nullable=False)
    start_bg_percent = Column(Integer, nullable=False)
    food_info = Column(String(100), nullable=False)
    meal_desc = Column(String(100), nullable=False)
    memo = Column(String(100), nullable=False)
    append_count = Column(Integer, nullable=False)
    push_alarm = Column(Integer, nullable=False)
    regist_time = Column(DateTime, nullable=False)
    modifier_uid = Column(Integer)
    modify_time = Column(DateTime, nullable=False)
    # pegist_time = Column(String(100))

class MEDICINE_History(Base):
    __tablename__ = "ch_medicine_search_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_uid = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    regist_time = Column(DateTime, nullable=False)
    modify_time = Column(DateTime, nullable=False)
    company = Column(String(100), nullable=False)
    created_at = Column(DateTime)

class MEALFOOD_History(Base):
    __tablename__ ="ch_meal_food"
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_type = Column(String(100), nullable=False)
    meal_id = Column(Integer, nullable=False)
    food_id = Column(Integer, nullable=False)
    food_name = Column(String(100), nullable=False, default="Unknown")
    serving_unit = Column(String(100), nullable=False, default="N/A")
    intake_amount = Column(Float, nullable=False, default=0.0)
    dc_ratio = Column(Float, nullable=False, default=0.0)
    photo_seed = Column(String(100), nullable=False, default="")
    minx = Column(Integer, nullable=False, default=0)
    maxx = Column(Integer, nullable=False, default=0)
    miny = Column(Integer, nullable=False, default=0)
    maxy = Column(Integer, nullable=False, default=0)
    regist_time = Column(DateTime, default=datetime.utcnow)
    modify_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    modifier_uid = Column(Integer, default=0)
