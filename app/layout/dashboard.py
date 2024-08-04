import streamlit as st
import time
from datetime import datetime, timedelta

import os
from utils.singleton import singleton
from layout.const import *
from st_on_hover_tabs import on_hover_tabs
from style.style import get_sidebar_styles
from streamlit import session_state as ss
from streamlit_pdf_viewer import pdf_viewer

@singleton
class DashLayout:
    def __init__(self):
        pass

    def draw_dashboard(self):
        stime = time.time()
        self.draw_sidebar()
        etime = time.time()
        st.markdown(f'### Update Time = {timedelta(seconds=etime - stime)}')

    def draw_sidebar(self):
        # st.header("전설의 김박펭귄 모험가의 여정을 담은 페이지입니다.")
        # st.image('image/kimparkpenguin.png', use_column_width='auto')

        # if 'pdf_ref' not in ss:
        #     ss.pdf_ref = None
        # st.file_uploader("Upload PDF file", type=('pdf'), key='pdf')
        # if ss.pdf:
        #     ss.pdf_ref = ss.pdf  # backup
        # if ss.pdf_ref:
        #     binary_data = ss.pdf_ref.getvalue()
        #     pdf_viewer(input=binary_data, width=700)

        # options = list(Menu)
        # tabs = on_hover_tabs(
        #     tabName=[menu.value for menu in options],
        #     iconName=['list'] * len(options),
        #     default_choice=2,
        #     styles=get_sidebar_styles()
        #
        # )
        #
        # if tabs == Menu.study_group.value:
        #     study_options = list(StudyGroup)
        #     study_tabs = on_hover_tabs(
        #         tabName=[menu.value for menu in study_options],
        #         iconName=['list'] * len(study_options),
        #         default_choice=0,
        #         styles=get_sidebar_styles()
        #
        #     )
        #     # 여기에 study_group 탭의 컨텐츠를 추가할 수 있습니다.
        # elif tabs == Menu.story_group.value:
        #     story_options = list(StoryGroup)
        #     story_tabs = on_hover_tabs(
        #         tabName=[menu.value for menu in story_options],
        #         iconName=['list'] * len(story_options),
        #         default_choice=0,
        #         styles=get_sidebar_styles()
        #
        #     )
        #     # 여기에 story_group 탭의 컨텐츠를 추가할 수 있습니다.
        # elif tabs == Menu.profile_group.value:
        #     profile_options = list(ProfileGroup)
        #     profile_tabs = on_hover_tabs(
        #         tabName=[menu.value for menu in profile_options],
        #         iconName=['list'] * len(profile_options),
        #         default_choice=0,
        #         styles=get_sidebar_styles()
        #     )
        #     # 여기에 profile_group에 대한 코드를 작성할 수 있습니다.
        #     pass

        st.sidebar.header("메뉴")

        # Dictionary to map main categories to their subcategories
        submenu_mapping = {
            Menu.study_group: list(StudyGroup),
            Menu.story_group: list(StoryGroup),
            Menu.profile_group: list(ProfileGroup)
        }

        # Initialize session state for menu
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = None

        # Display main categories with default expanded state
        for menu in Menu:
            with st.sidebar.expander(menu.value, expanded=True):
                for submenu in submenu_mapping[menu]:
                    if st.button(submenu.value, key=f"{menu.value}-{submenu.value}"):
                        st.session_state.active_tab = submenu.value

dashboard_layout: DashLayout = DashLayout()
