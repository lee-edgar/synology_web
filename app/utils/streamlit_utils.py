import streamlit as st
from typing import Any,List
from datetime import datetime, date, timedelta
from requests.packages import target

from datetime import time as dttime
from typing import Tuple, List, Union, Optional


def update_session_state(key: str, value: Any):
    """
    Streamlit 세션 상태에 값을 저장하거나 업데이트하는 함수.
    Args:
        key (str): 세션 상태에서 식별자로 사용할 키.
        value (Any): 해당 키에 저장할 값.
    """
    # st.session_state 딕셔너리에 키와 값을 저장합니다.
    st.session_state[key] = value

def get_session_state(key: str) -> Any:
    """
    Streamlit 세션 상태에서 값을 가져오는 함수.
    Args:
        key (str): 세션 상태에서 가져올 값을 식별하는 키.

    Returns:
        Any: 해당 키에 연결된 값. 만약 키가 존재하지 않으면 None을 반환.
    """
    # 세션 상태에 해당 키가 없으면 None 반환
    if key not in st.session_state:
        return None

    # 세션 상태에서 키에 연결된 값 반환
    return st.session_state[key]

def reset_session_state(*targets):
    for target in targets:
        update_session_state(target, None)

def initialize_session_state(defaults: dict):
    # 항상 디폴트 옵션을 주어, 새로고침 시 session out됨을 방지함.
    initialized_state = {}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
            initialized_state[key] = value
        else:
            initialized_state[key] = st.session_state[key]
    return initialized_state



def str2datetime(date:str) -> datetime:
    '''
    문자열 또는 datetime 객체를 받아 datetime 객체를 반환하는 함수.
    Returns:
        datetime: 입력 값이 문자열일 경우 datetime 객체로 변환된 값,
                  datetime 객체일 경우 그대로 반환.
    '''
    if isinstance(date, datetime):
        return date
    return datetime.fromisoformat(date)


def str2datetime_strptim(date, fmt="%Y-%m-%d %H:%M:%S") -> datetime:
    """
    문자열 또는 datetime 객체를 받아 datetime 객체를 반환하는 함수.
    문자열일 경우 지정된 포맷에 따라 datetime 객체로 변환합니다.

    Returns:
        datetime: 입력 값이 datetime 객체라면 그대로 반환,
                  문자열이라면 포맷에 따라 변환된 datetime 객체.

    Raises:
        ValueError: 문자열이 포맷에 맞지 않을 경우 예외 발생.
    """
    if isinstance(date, datetime):
        return date  # 이미 datetime 객체라면 그대로 반환
    try:
        return datetime.strptime(date, fmt)  # 문자열을 지정된 포맷으로 변환
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date}. Expected format: {fmt}") from e

def get_date_list(start_date:date, end_date:date) -> List[datetime]:
    date_range = []
    current_date = start_date

    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)

    return date_range

def get_alltime_date( when: date) -> Tuple[datetime, datetime]:
    fromT = dttime(0, 0, 0)
    toT = dttime(23, 59, 59)
    return datetime.combine(when, fromT), datetime.combine(when, toT)