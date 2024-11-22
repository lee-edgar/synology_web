from enum import Enum
import os

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

PROFILEGROUP_VIEW_MARKDOWN = ' # 프로필 '
STORYGROUP_VIEW_MARKDOWN = ' # 스토리 '
STUDYGROUP_VIEW_MARKDOWN = ' # 스터디 '
PORTFOLIO_VIEW_MARKDOWN = ' # 포트폴리오 '
CHANNEL_HEALTHCARE_MARKDOWN = '채널헬스케어'
COMMING_SOON = ' # COMMING SOON'

# session state 상수
SESSION_START_DATE = 'start_date'
SESSION_END_DATE = 'end_date'
SESSION_USER_UID = 'user_id'
DEFAULT_START_DATE = '2023-11-01'
DEFAULT_END_DATE = '2023-11-02'
DEFAULT_USER_UID = 187

DEFAULT_SESSION_STATE = {
    'user_uid': 187,
    'sdate': '2023-11-01T00:00:00',  # 시작 날짜: 자정
    'edate': '2023-11-02T23:59:59'   # 종료 날짜: 하루의 마지막 시간
}