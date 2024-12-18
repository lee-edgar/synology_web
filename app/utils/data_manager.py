# from app.utils.data_agent import data_agent
from datetime import datetime, date, timedelta
# from idlelib.debugger_r import wrap_info

import streamlit as st
import json
from typing import Dict, Any, Optional, Tuple, List
from app.utils.streamlit_utils import get_date_list


class DataManager:
    def __init__(self):
        self.cgm_dict = {}
        self.exercise_dict = {}
        self.meal_dict = {}
        self.medicine_dict = {}
        self.bollinger_band_dict = {}
        self.meal_food_dict = {}

    def get_cgm(self, user_uid: int, sdate: date, edate: date) -> Optional[Dict[str, Any]]:
        cgm_info: dict = self.cgm_dict.get(user_uid)
        if cgm_info is None:
            return None
        return cgm_info


    def update_cgm(self, user_uid: int, useful_data: date, cgm_json_data: Dict[str, Any]) -> None:
        cgm_info = self.cgm_dict.get(user_uid)
        if cgm_info is not None:
            cgm_info[user_uid] = cgm_json_data
        else:
            self.cgm_dict[user_uid] = cgm_json_data
            # self.cgm_dict[user_uid] = {useful_data: cgm_json_data}

    def get_bollinger_band(self, user_uid:int, sdate :date, edate:date):
        bollinger_band_info = self.bollinger_band_dict.get(user_uid)
        if bollinger_band_info is None:
            return None
        return bollinger_band_info

    def update_bollinger_band(self, user_uid, sdate, edate, bollinger_band_data):
        bollinger_band_info = self.bollinger_band_dict.get(user_uid)
        if bollinger_band_info is not None:
            bollinger_band_info[user_uid] = bollinger_band_data
        else:
            self.bollinger_band_dict[user_uid] = bollinger_band_data



    def get_exercise(self, user_uid: int, sdate: date, edate: date) -> Optional[Dict[str, Any]]:

        exercise_info: dict = self.exercise_dict.get(user_uid)
        if exercise_info is None:
            return None
        return exercise_info

    def update_exercise(self, user_uid: int, useful_data: date, exercise_json_data: Dict[str, Any]) -> None:

        exercise_info = self.exercise_dict.get(user_uid)
        if exercise_info is not None:
            exercise_info[user_uid] = exercise_json_data
        else:
            self.exercise_dict[user_uid] = exercise_json_data

    def get_meal_food(self, meal_id:int) -> Optional[Dict[str, Any]]:
        meal_food_info : dict = self.meal_food_dict.get(meal_id)
        if meal_food_info is None:
            return None
        return meal_food_info

    def update_meal_food(self, meal_id:int, meal_food_json_data:Dict[str, Any]) -> None:
        meal_food_info = self.meal_food_dict.get(meal_id)
        if meal_food_info is not None:
            meal_food_info[meal_id] = meal_food_info
        else:
            self.meal_food_dict[meal_id] = meal_food_info



    def get_meal(self, user_uid: int, sdate: date, edate: date) -> Optional[Dict[str, Any]]:
        meal_info: dict = self.meal_dict.get(user_uid)
        if meal_info is None:
            return None
        return meal_info

    def update_meal(self, user_uid: int, useful_data: date, meal_json_data: Dict[str, Any]) -> None:
        meal_info = self.meal_dict.get(user_uid)
        if meal_info is not None:
            meal_info[user_uid] = meal_json_data
        else:
            self.meal_dict[user_uid] = meal_json_data

    def get_medicine(self, user_uid: int, sdate: date) -> Optional[Dict[str, Any]]:
        medicine_info: dict = self.medicine_dict.get(user_uid)
        if medicine_info is None:
            return None
        return medicine_info

    def update_medicine(self, user_uid: int, useful_data: date, medicine_json_data: Dict[str, Any]) -> None:
        medicine_info = self.medicine_dict.get(user_uid)
        if medicine_info is not None:
            medicine_info[user_uid] = medicine_json_data
        else:
            self.medicine_dict[user_uid] = medicine_json_data


data_manager:DataManager = DataManager()