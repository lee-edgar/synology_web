import streamlit as st
from typing import Any,List

from requests.packages import target


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
