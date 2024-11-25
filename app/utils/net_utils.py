from http.client import responses

import requests
import json
from datetime import datetime
from app.common.common import GET_CGM, GET_EXERCISE, GET_MEAL, GET_MEDICINE
from typing import Optional

from loguru import logger
import streamlit as st

class NetUtil:
    """
    NetUtil 클래스
    -------------
    현재 프로젝트에서 API 요청과 관련된 주요 기능을 담당하는 클래스입니다.

    참고:
    - `archive.py` 파일에 `NetUtil` 클래스와 관련된 미사용 코드가 보관되어 있습니다.
    - `archive.py`에 보관된 메서드(`_make_request`, `get_cgm` 등)는 현재 사용되지 않지만,
      추후 필요할 경우 이 클래스에 다시 통합할 수 있습니다.
    """

    def __init__(self):
        logger.info("NetUtil initialized")


    def get_cgm(self, user_uid: int, start_time: datetime, end_time: datetime) -> Optional[dict]:
        params = {
            "user_uid": user_uid,
            "start_date": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "end_date": end_time.strftime("%Y-%m-%dT%H:%M:%S")
        }
        url = f'{GET_CGM}'

        response = requests.get(url=url, params=params)  # GET 요청으로 변경

        if response.status_code != 200:
            logger.error(f"Failed to get cgm info with user uid:{user_uid}. status_code: {response.status_code}")
            return None

        return response

    def get_exercise(self, user_uid: int, start_time: datetime, end_time: datetime) -> Optional[dict]:
        params = {
            "user_uid": user_uid,
            "start_date": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "end_date": end_time.strftime("%Y-%m-%dT%H:%M:%S")
        }
        url = f'{GET_EXERCISE}'

        response = requests.get(url=url, params=params)  # GET 요청으로 변경

        if response.status_code != 200:
            logger.error(f"Failed to get exercise info with user uid:{user_uid}. status_code: {response.status_code}")
            return None

        return response

    def get_meal(self, user_uid: int, start_time: datetime, end_time: datetime) -> Optional[dict]:
        params = {
            "user_uid": user_uid,
            "start_date": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "end_date": end_time.strftime("%Y-%m-%dT%H:%M:%S")
        }
        url = f'{GET_MEAL}'
        response = requests.get(url=url, params=params)  # GET 요청으로 변경

        if response.status_code != 200:
            logger.error(f"Failed to get meal info with user uid:{user_uid}. status_code: {response.status_code}")
            return None

        return response

    # def get_meal(self, user_uid: int, start_time: datetime, end_time: datetime) -> Optional[dict]:
    #     """
    #     Fetch meal history for a given user and time range.
    #     """
    #     payload = {
    #         "fromTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #         "toTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #         "query_type": "user_uid",
    #         "key": f"{user_uid}"
    #     }
    #     return self._make_request(GET_MEAL, payload)
    #
    # def get_medicine(self, user_uid: int, start_time: datetime) -> Optional[dict]:
    #     """
    #     Fetch medicine history for a given user on a specific date.
    #     """
    #     start_of_day = datetime.combine(start_time.date(), datetime.min.time())  # 00:00:00
    #     end_of_day = datetime.combine(start_time.date(), datetime.max.time())   # 23:59:59
    #
    #     payload = {
    #         "fromTime": start_of_day.strftime("%Y-%m-%dT%H:%M:%S"),
    #         "toTime": end_of_day.strftime("%Y-%m-%dT%H:%M:%S"),
    #         "query_type": "user_uid",
    #         "key": f"{user_uid}"
    #     }
    #     return self._make_request(GET_MEDICINE, payload)


net_util:NetUtil = NetUtil()
