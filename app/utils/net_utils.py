import requests
import json
from datetime import datetime
from app.common.common import GET_CGM, GET_EXERCISE, GET_MEAL, GET_MEDICINE
from typing import Optional
from loguru import logger

class NetUtil:
    def __init__(self):
        logger.info("NetUtil initialized")

    def _make_request(self, url: str, payload: dict) -> Optional[dict]:
        """
        Common request handler for POST requests.
        """
        try:
            response = requests.post(url, data=json.dumps(payload))
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Request failed with status code {response.status_code}: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error during request to {url}: {str(e)}")
            return None

    # def get_cgm(self, user_uid: int, start_time: datetime, end_time: datetime) -> Optional[dict]:
    #     """
    #     Fetch CGM history for a given user and time range.
    #     """
    #     payload = {
    #         "fromTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #         "toTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #         "query_type": "user_uid",
    #         "key": f"{user_uid}"
    #     }
    #     return self._make_request(GET_CGM, payload)
    def get_cgm(self, user_uid: int, start_time: datetime, end_time: datetime) -> Optional[dict]:
        """
        Fetch CGM history for a given user and time range.
        """
        payload = {
            "fromTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "toTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "query_type": "user_uid",
            "key": f"{user_uid}"
        }
        return self._make_request(GET_CGM, payload)

    def get_exercise(self, user_uid: int, start_time: datetime, end_time: datetime) -> Optional[dict]:
        """
        Fetch exercise history for a given user and time range.
        """
        payload = {
            "fromTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "toTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "query_type": "user_uid",
            "key": f"{user_uid}"
        }
        return self._make_request(GET_EXERCISE, payload)

    def get_meal(self, user_uid: int, start_time: datetime, end_time: datetime) -> Optional[dict]:
        """
        Fetch meal history for a given user and time range.
        """
        payload = {
            "fromTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "toTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "query_type": "user_uid",
            "key": f"{user_uid}"
        }
        return self._make_request(GET_MEAL, payload)

    def get_medicine(self, user_uid: int, start_time: datetime) -> Optional[dict]:
        """
        Fetch medicine history for a given user on a specific date.
        """
        start_of_day = datetime.combine(start_time.date(), datetime.min.time())  # 00:00:00
        end_of_day = datetime.combine(start_time.date(), datetime.max.time())   # 23:59:59

        payload = {
            "fromTime": start_of_day.strftime("%Y-%m-%dT%H:%M:%S"),
            "toTime": end_of_day.strftime("%Y-%m-%dT%H:%M:%S"),
            "query_type": "user_uid",
            "key": f"{user_uid}"
        }
        return self._make_request(GET_MEDICINE, payload)
