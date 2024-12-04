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


        # self.cgm_dict: Dict[int, List[Dict[str, Any]]] = {}


    def get_cgm(self, user_uid: int, sdate: date, edate: date) -> Optional[Dict[str, Any]]:
        cgm_info: dict = self.cgm_dict.get(user_uid)
        if cgm_info is None:
            return None
        # st.success('업데이트 된 세션에서 로드')
        return cgm_info

    # def get_cgm(self, user_uid: int, sdate: date, edate) -> List[Dict[str, Any]]:
    #     cgm_info = self.cgm_dict.get(user_uid, [])
    #     st.write('self.cgm_dict', self.cgm_dict)
    #     if cgm_info is None:
    #         return None

        # std_time이 sdate와 동일한 데이터 필터링
        # filtered_data = [
        #     item for item in cgm_info
        #     if datetime.strptime(item["std_time"], "%Y-%m-%dT%H:%M:%S").date() == sdate
        # ]
        #
        # # 동일한 데이터가 있으면 반환
        # if filtered_data:
        #     return filtered_data
        #
        # # 데이터가 없으면 업데이트 실행
        # updated_data = self.update_cgm(user_uid, sdate)
        # return updated_data


    # def get_cgm(self, user_uid: int, start_date: date, end_date: date) -> Optional[Tuple[List[Any], List[date]]]:
    #     cgm_info = self.cgm_dict.get(user_uid)
    #     st.write('datamanager cgminfo', self.cgm_dict.get(user_uid))
    #     if cgm_info is None:
    #         return None
    #
    #     # 날짜 리스트 생성
    #     date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    #
    #     cgm_list = []  # 데이터가 있는 날짜의 값
    #     noinfo_date_list = []  # 데이터가 없는 날짜 리스트
    #
    #     # 날짜별 데이터 확인
    #     for adate in date_list:
    #         useful_data = cgm_info.get(adate)
    #         if useful_data is not None:
    #             cgm_list.append(useful_data)
    #         else:
    #             # noinfo_date_list.append(adate)
    #             noinfo_date_list.append(adate.strftime("%Y-%m-%d"))  # 날짜를 문자열로 변환
    #
    #     return cgm_list, noinfo_date_list



    def update_cgm(self, user_uid: int, useful_data: date, cgm_json_data: Dict[str, Any]) -> None:
        cgm_info = self.cgm_dict.get(user_uid)
        if cgm_info is not None:
            cgm_info[user_uid] = cgm_json_data
        else:
            self.cgm_dict[user_uid] = cgm_json_data
            # self.cgm_dict[user_uid] = {useful_data: cgm_json_data}

    # def update_cgm(self, user_uid: int, useful_data: date, cgm_json_data: Dict[str, Any]) -> None:
    #     # 사용자 데이터 가져오기
    #     cgm_info = self.cgm_dict.get(user_uid, {})
    #
    #     # 날짜별 데이터 추가 또는 갱신
    #     if useful_data in cgm_info:
    #         # 기존 데이터가 있는 경우, 데이터 리스트로 추가
    #         cgm_info[useful_data].append(cgm_json_data)
    #     else:
    #         # 새로운 날짜의 데이터를 추가
    #         cgm_info[useful_data] = [cgm_json_data]
    #
    #     # 업데이트된 사용자 데이터 저장
    #     self.cgm_dict[user_uid] = cgm_info


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