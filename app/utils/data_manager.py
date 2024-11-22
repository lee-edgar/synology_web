# from app.utils.data_agent import data_agent
from datetime import datetime, date

class DataManager:
    def __init__(self):
        self.cgm_dict = {}

    def get_cgm(self, user_uid:int, sdate:date, edate:date):
        cgm_info:dict = self.cgm_dict.get(user_uid)
        if cgm_info is None:
            return None


data_manager:DataManager = DataManager()