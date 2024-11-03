from enum import Enum
import os

#
# class Menu(str, Enum):
#     study_group = 'Study Group'
#     story_group = 'Stroy Group'
#     profile_group = 'Profile Group'
#
#
# class StudyGroup(str, Enum):
#     kaggle = 'Kaggle'
#     paper = 'Paper'
#     ml = 'ML'
#     cv = 'CV'
#     streamlit = 'Streamlit'
#     math = 'Math'
#     coursera = 'Coursera'
#     link_collection = 'Link Collection'
#
#
# class StoryGroup(str, Enum):
#     retrospective = '회고'
#     thoughts = '그때그때 느끼는 것들'
#     synology_web = '현재 시놀로지 웹의 구성'
#
# class ProfileGroup(str, Enum):
#     profile = '프로필'
#

class Menu(str, Enum):
    study_group = 'Study Group'
    story_group = 'Story Group'
    profile_group = 'Profile Group'
    portfolio_group = 'Portfolio Group'

class StudyGroup(str, Enum):
    kaggle = 'Kaggle'
    paper = 'Paper'
    ml = 'ML'
    cv = 'CV'
    streamlit = 'Streamlit'
    math = 'Math'
    coursera = 'Coursera'
    link_collection = 'Link Collection'


class StoryGroup(str, Enum):
    retrospective = '회고'
    thoughts = '그때그때 느끼는 것들'
    synology_web = '현재 시놀로지 웹의 구성'


class ProfileGroup(str, Enum):
    profile = '프로필'

class PortfolioGroup(str, Enum):
    Portfolio = '포트폴리오'

PROFILEGROUP_VIEW_MARKDOWN = ' # 프로필 '
STORYGROUP_VIEW_MARKDOWN = ' # 스토리 '
STUDYGROUP_VIEW_MARKDOWN = ' # 스터디 '
PORTFOLIO_VIEW_MARKDOWN = ' # 포트폴리오 '