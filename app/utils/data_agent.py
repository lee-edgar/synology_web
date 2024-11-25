import pandas as pd

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
        cgm_list = []
        cgm_info = data_manager.get_cgm(user_uid, sdate, edate)
        
        if cgm_info is not None:
            cgm_list.extend(cgm_info)
        elif cgm_info is None:
            cgm = self.update_cgm(user_uid, sdate, edate)
            if cgm is not None:
                cgm_list.extend(cgm)
        return cgm_list

    def update_cgm(self, user_uid:int, sdate:date, edate:date):
        response = net_util.get_cgm(user_uid, sdate, edate)
        if response is None:
            return None

        cgm_json_data = response.json()
        if cgm_json_data is None:
            return None
        data_manager.update_cgm(user_uid, sdate, cgm_json_data)
        return cgm_json_data

data_agent:DataAgent = DataAgent()