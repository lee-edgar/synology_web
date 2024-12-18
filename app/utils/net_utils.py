from http.client import responses

import requests
import json
from datetime import datetime
from app.common.common import GET_CGM, GET_EXERCISE, GET_MEAL, GET_MEDICINE, GET_MEAL_FOOD
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

        try:
            response = requests.get(url=url, params=params)

            if response.status_code == 200:
                try:
                    return response
                except ValueError as e:
                    st.error(f"Failed to parse JSON response: {e}")
                    return None
            elif response.status_code == 404:
                st.sidebar.warning(f"No exercise data found for user_uid {user_uid}")
                return None
            else:
                st.sidebar.error(f"Unexpected response: {response.status_code}, Response Text: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            st.sidebar.error(f"Request failed: {e}")
            return None

    def get_meal_food(self, meal_id:int) -> Optional[dict]:
        params = {
            "meal_id": meal_id
        }
        url = f'{GET_MEAL_FOOD}'
        response = requests.get(url=url, params=params)
        if response.status_code != 200:
            logger.error(f"Failed to get meal info with meal_id{meal_id}. status_code: {response.status_code}")
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


    def get_medicine(self, user_uid: int, regist_time: datetime) -> Optional[dict]:
        params = {
            "user_uid": user_uid,
            "regist_time": regist_time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        url = f'{GET_MEDICINE}'

        try:
            response = requests.get(url=url, params=params)  # GET 요청
            if response.status_code == 200:
                # JSON 파싱 시도
                try:
                    return response
                except Exception as e:
                    logger.error(f"Error parsing JSON response: {e}")
                    st.sidebar.error(f"데이터를 처리하는 중 문제가 발생했습니다. (JSON 오류)")
                    return None

            elif response.status_code == 404:
                # st.warning(f"복약 데이터가 존재하지 않습니다. (user_uid: {user_uid})")
                logger.info(f"No exercise data found for user_uid {user_uid}. URL: {url}")
                return None

            elif response.status_code == 500:
                st.sidebar.error(f"서버 내부 오류로 데이터를 가져올 수 없습니다. (user_uid: {user_uid})")
                logger.error(f"500 Error: Internal server issue for {user_uid}. URL: {url}")
                return None

            else:
                st.warning(f"예상치 못한 응답 코드: {response.status_code}")
                logger.warning(f"Unexpected response: {response.status_code} for {user_uid}. URL: {url}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP 요청 중 오류 발생: {e}")
            st.sidebar.error(f"데이터를 가져오는 중 네트워크 문제가 발생했습니다.")
            return None



net_util:NetUtil = NetUtil()
