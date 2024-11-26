import pandas as pd

from app.utils.singleton import singleton
import streamlit as st
from app.utils.data_agent import DataAgent, data_agent
from datetime import datetime, date


@singleton
class ChannelHealthcareInfo:
    def __init__(self):
        pass

    def get_cgm_data(self, user_uid: int, sdate: date, edate:date):
        cgm_info = data_agent.get_cgm(user_uid, sdate, edate)
        return pd.DataFrame(cgm_info)

    def get_exercise_data(self, user_uid: int, sdate: date, edate:date):
        exercise_info = data_agent.get_exercise(user_uid, sdate, edate)
        return pd.DataFrame(exercise_info)

    def get_meal_data(self, user_uid: int, sdate: date, edate: date):
        meal_info = data_agent.get_meal(user_uid, sdate, edate)
        return pd.DataFrame(meal_info)

    def get_medicine_data(self, user_uid: int, sdate: date):
        medicine_info = data_agent.get_medicine(user_uid, sdate)
        return pd.DataFrame(medicine_info)


channel_healthcare_info_session: ChannelHealthcareInfo = ChannelHealthcareInfo()