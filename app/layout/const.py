from enum import Enum
import os

class Menu(str, Enum):
    study_group = 'StudyGroup'
    story_group = 'StoryGroup'
    profile_group = 'ProfileGroup'
    portfolio_group = 'PortfolioGroup'

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

class PortfolioGroup(str, Enum):
    Portfolio = '포트폴리오'

PROFILEGROUP_VIEW_MARKDOWN = ' # 프로필 '
STORYGROUP_VIEW_MARKDOWN = ' # 스토리 '
STUDYGROUP_VIEW_MARKDOWN = ' # 스터디 '
PORTFOLIO_VIEW_MARKDOWN = ' # 포트폴리오 '
COMMING_SOON = ' # COMMING SOON'