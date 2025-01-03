import pandas as pd

from app.utils.singleton import singleton
from app.utils.data_manager import DataManager, data_manager
from datetime import datetime, date
from app.utils.net_utils import net_util
import streamlit as st
from typing import Dict, Any, Optional

from app.utils.streamlit_utils import get_date_list, get_alltime_date
# from app.session.channel_healthcare_session_service import ChannelHealthcareSessionService, channel_healthcare_session_service

@singleton
class DataAgent:
    def __init__(self):
        pass

    # 원본
    def get_cgm(self, user_uid: int, sdate: date, edate: date) -> Optional[dict]:
        cgm_list = []
        cgm_info = data_manager.get_cgm(user_uid, sdate, edate)
        if cgm_info is not None:
            cgm_list.extend(cgm_info)
            st.session_state.data_call_session = '저장값 로드'
            # st.success('저장값 로드')


        elif cgm_info is None:
            cgm = self.update_cgm(user_uid, sdate, edate)
            st.session_state.data_call_session = '새롭게 업데이트'
            # st.success('새롭게 업데이트')
            if cgm is not None:
                cgm_list.extend(cgm)
        return cgm_list

    def update_cgm(self, user_uid:int, sdate:date, edate:date) -> Optional[dict]:
        response = net_util.get_cgm(user_uid, sdate, edate)
        if response is None:
            return None

        cgm_json_data = response.json()
        if cgm_json_data is None:
            return None
        data_manager.update_cgm(user_uid, sdate, cgm_json_data)
        return cgm_json_data

    def get_bollinger_band(self, user_uid, sdate, edate, bollinger_band_df):
        bollinger_band_info = data_manager.get_bollinger_band(user_uid, sdate, edate)
        if bollinger_band_info is None:
            self.update_bollinger_band(user_uid, sdate, edate, bollinger_band_df)
        return bollinger_band_info

    def update_bollinger_band(self, user_uid, sdate, edate, bollinger_band_df):
        from app.session.channel_healthcare_session_service import channel_healthcare_session_service
        bollinger_band_data = channel_healthcare_session_service.update_bollinger_band(user_uid, bollinger_band_df)
        if bollinger_band_data is None:
            return None
        data_manager.update_bollinger_band(user_uid, sdate, edate, bollinger_band_data)

        return bollinger_band_data


    def get_exercise(self, user_uid: int, sdate: date, edate: date) -> Optional[dict]:
        exercise_list = []
        exercise_info = data_manager.get_exercise(user_uid, sdate, edate)
        if exercise_info is not None:
            exercise_list.extend(exercise_info)

        elif exercise_info is None:
            exercise = self.update_exercise(user_uid, sdate, edate)

            if exercise is not None:
                exercise_list.extend(exercise)
            else:
                return None

        return exercise_list

    def update_exercise(self, user_uid: int, sdate: date, edate: date) -> Optional[dict]:
        response = net_util.get_exercise(user_uid, sdate, edate)
        if response is None:
            return None

        exercise_json_data = response.json()
        if exercise_json_data is None:
            return None
        data_manager.update_exercise(user_uid, sdate, exercise_json_data)
        return exercise_json_data


    def get_meal_food(self, meal_id:int):
        meal_food_list = []
        meal_food_info = data_manager.get_meal_food(meal_id)

        if meal_food_info is not None:
            meal_food_list.extend(meal_food_info)
        elif meal_food_info is None:
            meal_food = self.update_meal_food(meal_id)

            if meal_food is not None:
                meal_food_list.extend(meal_food)
        return meal_food_list

    def update_meal_food(self, meal_id:int) -> Optional[dict]:
        response = net_util.get_meal_food(meal_id)
        if response is None:
            return None

        meal_food_json_data = response.json()
        if meal_food_json_data is None:
            return None
        data_manager.update_meal_food(meal_id, meal_food_json_data)
        return meal_food_json_data


    def get_meal(self, user_uid, sdate, edate) -> Optional[dict]:
        meal_list = []
        meal_info = data_manager.get_meal(user_uid, sdate, edate)

        if meal_info is not None:
            meal_list.extend(meal_info)

        elif meal_info is None:
            meal = self.update_meal(user_uid, sdate, edate)

            if meal is not None:
                meal_list.extend(meal)

        return meal_list

    def update_meal(self, user_uid: int, sdate: date, edate: date) -> Optional[dict]:
        response = net_util.get_meal(user_uid, sdate, edate)
        if response is None:
            return None

        meal_json_data = response.json()
        if meal_json_data is None:
            return None
        data_manager.update_meal(user_uid, sdate, meal_json_data)
        return meal_json_data

    def get_medicine(self, user_uid: int, sdate: date) -> Optional[dict]:
        medicine_list = []
        medicine_info = data_manager.get_medicine(user_uid, sdate)
        if medicine_info is not None:
            medicine_list.extend(medicine_info)

        elif medicine_info is None:
            medicine = self.update_medicine(user_uid, sdate)

            if medicine is not None:
                medicine_list.extend(medicine)
            else:
                return None


        return medicine_list

    def update_medicine(self, user_uid: int, sdate: date) -> Optional[dict]:
        response = net_util.get_medicine(user_uid, sdate )
        if response is None:
            return None

        medicine_json_data = response.json()
        if medicine_json_data is None:
            return None
        data_manager.update_medicine(user_uid, sdate, medicine_json_data)
        return medicine_json_data




data_agent:DataAgent = DataAgent()