from enum import Enum
import os
from datetime import datetime, date


class Menu(str, Enum):
    profile_group = 'ProfileGroup'
    study_group = 'StudyGroup'
    story_group = 'StoryGroup'
    # portfolio_group = 'PortfolioGroup'

class StudyGroup(str, Enum):
    kaggle = 'Kaggle'
    paper = 'Paper'
    ml = 'ML'
    cv = 'CV'
    streamlit = 'Streamlit'
    math = 'Math'
    coursera = 'Coursera'
    link_collection = 'LinkCollection'


class StoryGroup(str, Enum):
    retrospective = '회고'
    thoughts = '그때그때느끼는것들'
    synology_web = '현재시놀로지웹의구성'


class ProfileGroup(str, Enum):
    profile = '프로필'
    channel_healthcare ='채널헬스케어'

class PortfolioGroup(str, Enum):
    prediction_mushrooms_binaryclassification = '버섯의 독성 분류'
    channel_healthcare = '채널헬스케어'
    retinal_oct_disease_classification =  'OCT 기반 안구질환 분류'

class TableView(str, Enum):
    cgm = '연속기록'
    meal = '식사기록'
    exercise = '운동기록'
    medicine = '약물기록'

PROFILEGROUP_VIEW_MARKDOWN = ' # 프로필 '
STORYGROUP_VIEW_MARKDOWN = ' # 스토리 '
STUDYGROUP_VIEW_MARKDOWN = ' # 스터디 '
PORTFOLIO_VIEW_MARKDOWN = ' # 포트폴리오 '
CHANNEL_HEALTHCARE_MARKDOWN = '채널헬스케어'
COMMING_SOON = ' # COMMING SOON'

# session state 상수
SESSION_LOAD_START_DATE = 'load_start_date'
SESSION_LOAD_END_DATE = 'load_end_date'
SESSION_VIZ_START_DATE = 'viz_start_date'
SESSION_VIZ_END_DATE = 'viz_end_date'

SESSION_MEAL_ID = 'meal_id'
SESSION_USER_UID = 'user_id'
DEFAULT_START_DATE = '2023-11-01'
DEFAULT_END_DATE = '2023-11-02'
DEFAULT_USER_UID = 187
USER_GROUP = [
    350,
    187
]
SELECT_MODE = [
    "Select",
    "All"
]

SELECT_MODE = [
    "Select",
    "All"
]
USER_DATE_RANGES = {
    350: {
        "load_start_date": datetime.strptime('2023-07-21T00:00:00', '%Y-%m-%dT%H:%M:%S'),
        "load_end_date": datetime.strptime('2023-08-03T23:59:59', '%Y-%m-%dT%H:%M:%S'),
        "viz_start_date": datetime.strptime('2023-07-21T00:00:00', '%Y-%m-%dT%H:%M:%S'),
        "viz_end_date": datetime.strptime('2023-07-21T23:59:59', '%Y-%m-%dT%H:%M:%S'),

    },
    187: {
        "load_start_date": datetime.strptime('2023-11-01T00:00:00', '%Y-%m-%dT%H:%M:%S'),
        "load_end_date": datetime.strptime('2023-11-14T23:59:59', '%Y-%m-%dT%H:%M:%S'),
        "viz_start_date": datetime.strptime('2023-11-01T00:00:00', '%Y-%m-%dT%H:%M:%S'),
        "viz_end_date": datetime.strptime('2023-11-01T23:59:59', '%Y-%m-%dT%H:%M:%S'),
    }
}


MSG_NO_CGM_DATA = '연속혈당 정보가 없습니다. :sunglasses:'
MSG_NO_EXERCISE_DATA = '운동 정보가 없습니다. :sunglasses:'
MSG_NO_TAKE_MEDICINE_DATA = '약물 정보가 없습니다. :sunglasses:'
MSG_NO_MEDICATION_DATA = '복약 정보가 없습니다. :sunglasses:'
MSG_NO_SPLIT_BREAK_LINE_DATA = "No segments found in split_break_line."
X_AXIS_DTICK_VALUES = { 0: 3600 * 1000, 1: 7200 * 1000, 3: 14400 * 1000, 7: 43200 * 1000 }


DEFAULT_SESSION_STATE = {
    'user_uid': 350,
    'sdate': '2023-07-21T00:00:00',  # 시작 날짜: 자정
    'edate': '2023-08-03T23:59:59',   # 종료 날짜: 하루의 마지막 시간
    'data_call_session': None
}

FOOD_CALORIES_DUMMY = {
    "참외": 70,
    "사과": 70,
    "검은콩": 83,
    "파프리카": 17,
    "라면": 597,
    "선지해장국": 409,
    "밥": 334,
    "돈고츠라멘": 500,
    "돼지껍데기": 520,
    "바지락조개탕": 181,
    "깍두기": 15,
    "녹두전, 냉동": 329,
    "홍합탕": 20,
    "블루베리": 38,
    "짜장라면": 600,
    "생가득 메밀막국수": 475,
    "골뱅이무침": 320,
    "비빔냉면": 474,
    "묵사발": 135,
    "프라이드치킨": 668,
    "떡볶이": 304,
    "초밥": 462,
    "물냉면": 507,
    "잡채밥": 500,
    "3분 쇠고기카레": 175,
    "잡곡밥": 336,
    "흰밥": 334,
    "오징어숙회": 115,
    "어묵볶음": 70,
    "콩나물무침": 38,
    "김치찌개": 308,
    "짬뽕국": 149,
    "수제비": 126,
    "갈비탕": 449,
    "감자탕": 355,
    "된장찌개": 91,
    "부대찌개": 461,
    "육개장(소고기)": 230,
    "돼지고기탕수육": 234,
    "모듬콩조림": 131,
    "계란후라이": 86,
    "숙주나물": 18,
    "시래기나물, 된장": 42,
    "상추겉절이": 51,
    "채소샐러드": 60,
    "마늘장아찌": 17,
    "양파장아찌": 31,
    "오징어젓": 25,
    "땅콩조림": 170,
    "코카콜라제로": 0,
    "삼각김밥": 174,
    "필리 치즈 스테이크": 300,
    "빠다코코낫": 250,
    "참크래커": 87
}
