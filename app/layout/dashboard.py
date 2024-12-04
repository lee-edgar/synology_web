import streamlit as st
import time
from datetime import datetime, timedelta
from app.utils.singleton import singleton
from app.layout.const import *
import requests
import json
from app.common.common import BACKEND_URL

from app.layout.portfolio_layout import Portfolio
from app.layout.profile_layout import Profile
from app.layout.study_layout import Study
from app.layout.story_layout import Story
from app.layout.portfolio_channel_layout import Portfolio_Channel_Layout
@singleton
class DashLayout:
    def __init__(self):
        self.submenu_mapping = {
            Menu.study_group: list(StudyGroup),
            Menu.story_group: list(StoryGroup),
            Menu.profile_group: list(ProfileGroup),
            # Menu.portfolio_group: list(PortfolioGroup),
        }
        self.profile_layout = Profile()
        self.portfolio_layout = Portfolio()
        self.channel_healthcare = Portfolio_Channel_Layout()
        self.study_layout = Study()
        self.story_layout = Story()

        # 스트림릿은 상호작용마다 스크립트를 재실행하기에, 전역으로 둘 수 없음
        if 'column_state' not in st.session_state:
            st.session_state.column_state = {'width': 2}

        if 'layout_options' not in st.session_state:
            st.session_state.layout_options = {
                'default': [1, 1.5],  # 1:1.5 비율
                'wide': [1, 3],  # 1:3 비율
                'balanced': [1, 1],  # 1:1 비율
                'custom': [2, 3]  # 2:3 비율
            }

        # active_tab 초기화를 먼저 수행
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = ProfileGroup.profile.value
            # 기본 URL 파라미터도 설정
            st.query_params["group"] = Menu.profile_group.value
            st.query_params["submenu"] = ProfileGroup.profile.value

        if 'group' in st.query_params and 'submenu' in st.query_params:
            st.session_state.active_tab = st.query_params.submenu
        elif 'active_tab' not in st.session_state:
            st.session_state.active_tab = ProfileGroup.profile.value

    def draw_dashboard(self):
        stime = time.time()
        selected = self.draw_sidebar()
        self.update_main_panel(selected=selected)
        etime = time.time()
        # self.side_selector()
        st.markdown(f' Update Time = {timedelta(seconds=etime - stime)}')



    def side_selector(self):
        if 'layout_options' not in st.session_state:
            st.session_state.layout_options = {
                'default': [1, 1.5],  # 1:1.5 비율
                'wide': [1, 3],  # 1:3 비율
                'balanced': [1, 1],  # 1:1 비율
                'custom': [2, 3]  # 2:3 비율
            }

        # 현재 선택된 레이아웃 상태 관리
        if 'current_layout' not in st.session_state:
            st.session_state.current_layout = 'default'

        # 레이아웃 선택 UI
        # layout_choice = st.sidebar.selectbox(
        st.session_state.current_layout = st.sidebar.selectbox(

            "레이아웃 선택",
            options=list(st.session_state.layout_options.keys()),
            index=list(st.session_state.layout_options.keys()).index(st.session_state.current_layout),
            format_func=lambda x: {
                'default': '기본 (1:1.5)',
                'wide': '와이드 (1:3)',
                'balanced': '균형 (1:1)',
                'custom': '커스텀 (2:3)'
            }[x]
        )

    def draw_sidebar(self):
        self.side_selector()

        st.sidebar.header("메뉴")
        for menu in Menu:
            with st.sidebar.expander(menu.value, expanded=True):
                for submenu in self.submenu_mapping[menu]:
                    if st.button(submenu.value, key=f"{menu.value}-{submenu.value}"):
                        st.session_state.active_tab = submenu.value
                        st.query_params["group"] = menu.value
                        st.query_params["submenu"] = submenu.value

        # active_tab이 없을 경우를 대비한 안전장치
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = ProfileGroup.profile.value

        return st.session_state.active_tab

    def update_main_panel(self, selected):

        if selected in [item.value for item in ProfileGroup]:
            if selected == ProfileGroup.profile.value:

                st.markdown(f"{PROFILEGROUP_VIEW_MARKDOWN}")
                st.write('---')

                # 사이드바의 레이아웃 선택에 의한 화면 분할 사이즈 조정
                current_layout = st.session_state.get("current_layout", "default")
                layout_values = st.session_state.layout_options[current_layout]
                cols = st.columns(layout_values)

                with cols[0]:
                    self.profile_layout.draw()
                with cols[1]:
                    self.portfolio_layout.draw()
            elif selected == ProfileGroup.channel_healthcare.value:
                st.write(f"Debug: Calling channel_healthcare.draw() with selected={selected}")
                self.channel_healthcare.initialize_session_render()


        elif selected in [item.value for item in PortfolioGroup]:
            self.portfolio_layout.navigation()
        elif selected in [item.value for item in StoryGroup]:
            self.story_layout.draw()
        elif selected in [item.value for item in StudyGroup]:
            self.study_layout.draw()

    def _fallback_view(self, selected):
        if selected in [item.value for item in ProfileGroup]:
            self.profile_layout.draw_ProfileGroup_view()
        elif selected in [item.value for item in StoryGroup]:
            self.draw_StoryGroup_view(selected)
        elif selected in [item.value for item in StudyGroup]:
            self.draw_StudyGroup_view(selected)
        elif selected in [item.value for item in PortfolioGroup]:
            self.draw_PortfolioGroup_view(selected)

    def draw_StoryGroup_view(self, selected):
        st.markdown(f"{STORYGROUP_VIEW_MARKDOWN} ({selected})")

    def draw_StudyGroup_view(self, selected):
        st.markdown(f"{STUDYGROUP_VIEW_MARKDOWN} ({selected})")

    def draw_PortfolioGroup_view(self, selected):
        st.markdown(f"{PORTFOLIO_VIEW_MARKDOWN} ({selected})")

dashboard_layout: DashLayout = DashLayout()