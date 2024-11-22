from app.utils.singleton import singleton
from app.utils.data_manager import DataManager, data_manager
from datetime import datetime, date
from app.utils.net_utils import net_util
import streamlit as st

@singleton
class DataAgent:
    def __init__(self):
        pass


    def get_cgm(self, user_uid, sdate, edate):
        cgm_info = data_manager.get_cgm(user_uid, sdate, edate)
        st.write('agent cgm', cgm_info)
        if cgm_info is None:
            self.update_cgm(user_uid, sdate, edate)

    def update_cgm(self, user_uid:int, sdate:date, edate:date):
        response = net_util.get_cgm(user_uid, sdate, edate)
        st.write('response', response)


data_agent:DataAgent = DataAgent()