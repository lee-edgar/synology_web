"""
archive.py
===========
이 파일은 프로젝트에서 현재 사용되지 않는 코드, 추후에 필요할 가능성이 있는 코드,
혹은 재사용 가능성을 염두에 둔 공통 코드의 보관소 역할을 합니다.

파일 목적:
1. 프로젝트 내 특정 모듈에 속하지 않는 범용적인 유틸리티 함수 및 클래스 보관.
2. 현재 사용되지 않는 코드 중 잠재적으로 다시 사용할 가능성이 있는 코드 보관.
3. 코드 가독성과 유지보수를 위해 아카이브된 코드를 한 곳에 통합 관리.

주의:
- 이 파일은 반드시 필요한 경우에만 참조하도록 설계되었습니다.
- 코드가 활성화되어 필요할 경우 적절한 모듈로 이동하세요.
"""

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
    front-end단 코드입니다.
    HTTP 요청을 처리하기 위한 유틸리티 클래스.
    현재 프로젝트에서 사용하지 않는 함수(_make_request, get_cgm)를 포함하고 있으며,
    필요 시 활성화하여 사용할 수 있습니다.
    """

    def __init__(self):
        logger.info("NetUtil initialized")

    def _make_request(self, method: str, url: str, params: dict = None, payload: dict = None) -> Optional[dict]:
        """
        HTTP 요청을 처리하는 공통 메서드.

        Args:
            method (str): HTTP 메서드 ('GET', 'POST' 등).
            url (str): 요청 대상 URL.
            params (dict, optional): GET 요청의 쿼리 파라미터.
            payload (dict, optional): POST 요청의 JSON 페이로드.

        Returns:
            Optional[dict]: 요청이 성공한 경우 JSON 응답 데이터, 실패 시 None.
        """
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, json=payload)
            else:
                logger.error(f"지원하지 않는 HTTP 메서드: {method}")
                return None

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"요청 실패 (상태 코드 {response.status_code}): {response.text}")
                return None
        except Exception as e:
            logger.error(f"요청 중 오류 발생 ({url}): {str(e)}")
            return None

    def get_cgm(self, user_uid: int, start_time: datetime, end_time: datetime) -> Optional[dict]:
        """
        특정 사용자와 시간 범위에 대한 CGM 데이터를 가져오는 메서드.

        Args:
            user_uid (int): 사용자 ID.
            start_time (datetime): 시작 날짜 및 시간.
            end_time (datetime): 종료 날짜 및 시간.

        Returns:
            Optional[dict]: 요청이 성공한 경우 JSON 응답 데이터, 실패 시 None.
        """
        params = {
            "user_uid": user_uid,
            "start_date": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "end_date": end_time.strftime("%Y-%m-%dT%H:%M:%S")
        }

        url = f"{GET_CGM}"
        return self._make_request("GET", url, params=params)
