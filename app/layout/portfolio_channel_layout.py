import streamlit as st
import requests
import json
from app.common.common import BACKEND_URL
from app.utils.singleton import  singleton
from app.layout.const import *
from streamlit_pdf_viewer import pdf_viewer
from datetime import date, datetime, timedelta
from app.session.channel_healthcare_info import channel_healthcare_info_session
from app.utils.streamlit_utils import get_session_state, update_session_state


class Portfolio_Channel_Layout():
    def __init__(self):

        # 채널헬스케어 portfolio의 초기 셋팅 단계임(sdate, edate, user_uid 값 세팅)
        if get_session_state(SESSION_START_DATE) is None:
            update_session_state(SESSION_START_DATE, DEFAULT_START_DATE)
        if get_session_state(SESSION_END_DATE) is None:
            update_session_state(SESSION_END_DATE, DEFAULT_END_DATE)
        if get_session_state(SESSION_USER_UID) is None:
            update_session_state(SESSION_USER_UID, DEFAULT_USER_UID)


    def update_date(self):
        sdate = '2023-11-01'
        edate = '2023-11-03'
        self.update_ch_data(sdate, edate)

    def update_ch_data(self, start_date : date, end_date:date):
        self.update_cgm(start_date, end_date)

    def update_cgm(self, start_date, end_date):
        pass

    def draw(self):
        '''
        session out 발생시 새롭게 session 업데이트
        :return:
        '''
        st.markdown(f"{CHANNEL_HEALTHCARE_MARKDOWN}")

        # 기본값 설정
        defaults = {
            SESSION_START_DATE: '2023-11-01',
            SESSION_END_DATE: '2022-11-02',
            SESSION_USER_UID: 187
        }

        # None인 세션 상태를 기본값으로 업데이트
        for key, default_value in defaults.items():
            if get_session_state(key) is None:
                update_session_state(key, default_value)

        # 세션 값 가져오기
        sdate = get_session_state(SESSION_START_DATE)
        edate = get_session_state(SESSION_END_DATE)
        user_uid = get_session_state(SESSION_USER_UID)


        st.write("Session Values:", [sdate, edate, user_uid])

