# from app.utils.data_agent import data_agent
from datetime import datetime, date
import streamlit as st
import json

class DataManager:
    def __init__(self):
        self.cgm_dict = {}

    def get_cgm(self, user_uid: int, sdate: date, edate: date):
        cgm_info: dict = self.cgm_dict.get(user_uid)
        if cgm_info is None:
            return None

        # JSON 직렬화(datetime -> str)
        serialized_info = self.json_serialize(cgm_info)
        return serialized_info


    def update_cgm(self, user_uid, useful_data, cgm_json_data):

        cgm_info = self.cgm_dict.get(user_uid)
        if cgm_info is not None:
            cgm_info[useful_data] = cgm_json_data
        else:
            self.cgm_dict[user_uid] = {useful_data: cgm_json_data}

    def json_serialize(data: dict) -> str:
        """
        JSON 직렬화는 기본적으로 문자열, 정수, 부동 소수점, 불리언, None만 처리할 수 있습니다.
        이 함수는 datetime 객체를 ISO 8601 형식의 문자열로 변환하여 직렬화를 지원합니다.
        Returns: str: JSON 형식의 문자열.
        """
        return json.dumps(data, default=lambda x: x.strftime("%Y-%m-%dT%H:%M:%S") if isinstance(x, datetime) else x)

data_manager:DataManager = DataManager()