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
        df = pd.DataFrame(data_agent.get_medicine(user_uid, sdate))

        # st.session_state에서 날짜 가져오기
        session_sdate, session_edate = pd.to_datetime(st.session_state.sdate), pd.to_datetime(st.session_state.edate)

        # regist_time 필터링
        df['regist_time'] = pd.to_datetime(df['regist_time'])  # datetime 형식으로 변환
        filtered_df = df[(df['regist_time'] >= session_sdate) & (df['regist_time'] <= session_edate)]

        return filtered_df

channel_healthcare_info_session: ChannelHealthcareInfo = ChannelHealthcareInfo()