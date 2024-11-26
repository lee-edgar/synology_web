import streamlit as st
import requests
import json
from app.common.common import BACKEND_URL
from app.utils.singleton import  singleton
from app.layout.const import *
from streamlit_pdf_viewer import pdf_viewer
from datetime import date, datetime, timedelta
from app.session.channel_healthcare_info import channel_healthcare_info_session
from app.utils.streamlit_utils import get_session_state, update_session_state, initialize_session_state, str2datetime


class Portfolio_Channel_Layout():
    def __init__(self):

        pass

    # def update_date(self):
    #     sdate = '2023-11-01'
    #     edate = '2023-11-03'
    #     self.update_ch_data(sdate, edate)
    #
    # def update_ch_data(self, start_date : date, end_date:date):
    #     self.update_cgm(start_date, end_date)

    def initialize_session_render(self):
        '''
        초기 세션 상태 설정:
        기본 세션 정보를 DEFAULT_SESSION_STATE 값으로 초기화함.
        세션 변경이 필요한 경우, 자식함수에서 변경할 수 있음.
        '''
        st.markdown(f"{CHANNEL_HEALTHCARE_MARKDOWN}")

        initialize_session_state(DEFAULT_SESSION_STATE)

        self.draw_graph()
        self.draw_table()

    def draw_graph(self):
        user_uid = st.session_state['user_uid']
        sdate = str2datetime(st.session_state['sdate'])
        edate = str2datetime(st.session_state['edate'])


        self.get_cgm(user_uid, sdate, edate)
        self.get_exercise(user_uid, sdate, edate)
        self.get_meal(user_uid, sdate, edate)
        self.get_medicine(user_uid, sdate)

    def draw_table(self):
        mode = st.radio('회원 정보 탭', [item.value for item in TableView],
                        horizontal=True, label_visibility='collapsed')
        st.info(st.session_state.data_call_session)
        if mode == TableView.cgm:
            st.dataframe(self.get_cgm(st.session_state['user_uid'],  str2datetime(st.session_state['sdate']), str2datetime(st.session_state['edate'])))

        elif mode == TableView.meal:
            st.dataframe(self.get_exercise(st.session_state['user_uid'], str2datetime(st.session_state['sdate']), str2datetime(st.session_state['edate'])))

        elif mode == TableView.exercise:
            st.dataframe(self.get_meal(st.session_state['user_uid'], str2datetime(st.session_state['sdate']),str2datetime(st.session_state['edate'])))

        elif mode == TableView.medicine:
            st.dataframe(self.get_medicine(st.session_state['user_uid'],  str2datetime(st.session_state['sdate'])))

    def get_cgm(self, user_uid: int, sdate: date, edate:date):
        return channel_healthcare_info_session.get_cgm_data(user_uid, sdate, edate)

    def get_exercise(self, user_uid: int, sdate: date, edate:date):
        return channel_healthcare_info_session.get_exercise_data(user_uid, sdate, edate)

    def get_meal(self, user_uid: int, sdate: date, edate:date):
        return channel_healthcare_info_session.get_meal_data(user_uid, sdate, edate)

    def get_medicine(self, user_uid: int, sdate: date):
        return channel_healthcare_info_session.get_medicine_data(user_uid, sdate)


