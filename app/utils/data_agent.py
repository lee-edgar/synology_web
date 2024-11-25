import pandas as pd

from app.utils.singleton import singleton
from app.utils.data_manager import DataManager, data_manager
from datetime import datetime, date
from app.utils.net_utils import net_util
import streamlit as st
from typing import Dict, Any, Optional


@singleton
class DataAgent:
    def __init__(self):
        pass


    def get_cgm(self, user_uid: int, sdate: date, edate: date) -> Optional[dict]:
        cgm_list = []
        cgm_info = data_manager.get_cgm(user_uid, sdate, edate)
        
        if cgm_info is not None:
            cgm_list.extend(cgm_info)
            st.success('업데이트 된 세션에서 로드')

        elif cgm_info is None:
            cgm = self.update_cgm(user_uid, sdate, edate)
            st.success('세션 업데이트 후 로드')

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

    def get_exercise(self, user_uid: int, sdate: date, edate: date) -> Optional[dict]:
        exercise_list = []
        exercise_info = data_manager.get_exercise(user_uid, sdate, edate)

        if exercise_info is not None:
            exercise_list.extend(exercise_info)
            st.success('업데이트 된 세션에서 로드')

        elif exercise_info is None:
            exercise = self.update_exercise(user_uid, sdate, edate)
            st.success('세션 업데이트 후 로드')

            if exercise is not None:
                exercise_list.extend(exercise)

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


    def get_meal(self, user_uid, sdate, edate) -> Optional[dict]:
        meal_list = []
        meal_info = data_manager.get_meal(user_uid, sdate, edate)

        if meal_info is not None:
            meal_list.extend(meal_info)
            st.success('업데이트 된 세션에서 로드')

        elif meal_info is None:
            meal = self.update_meal(user_uid, sdate, edate)
            st.success('세션 업데이트 후 로드')

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



data_agent:DataAgent = DataAgent()