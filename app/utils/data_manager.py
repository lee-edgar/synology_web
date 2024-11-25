# from app.utils.data_agent import data_agent
from datetime import datetime, date
import streamlit as st
import json

class DataManager:
    def __init__(self):
        self.cgm_dict = {}
        self.exercise_dict = {}


    def get_cgm(self, user_uid: int, sdate: date, edate: date):
        cgm_info: dict = self.cgm_dict.get(user_uid)
        if cgm_info is None:
            return None
        # st.success('업데이트 된 세션에서 로드')
        return cgm_info

    def update_cgm(self, user_uid, useful_data, cgm_json_data):
        cgm_info = self.cgm_dict.get(user_uid)
        if cgm_info is not None:
            cgm_info[user_uid] = cgm_json_data
        else:
            self.cgm_dict[user_uid] = cgm_json_data
            # st.success('세션 업데이트 후 로드')

    def get_exercise(self, user_uid: int, sdate: date, edate: date):
        exercise_info: dict = self.exercise_dict.get(user_uid)
        if exercise_info is None:
            return None
        return exercise_info

    def update_exercise(self, user_uid, useful_data, exercise_json_data):
        exercise_info = self.exercise_dict.get(user_uid)
        if exercise_info is not None:
            exercise_info[user_uid] = exercise_json_data
        else:
            self.exercise_dict[user_uid] = exercise_json_data


data_manager:DataManager = DataManager()