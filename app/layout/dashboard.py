import streamlit as st
import time
from datetime import datetime, timedelta

import os
from app.utils.singleton import singleton
from app.layout.const import *
from st_on_hover_tabs import on_hover_tabs
from app.style.style import get_sidebar_styles
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, '..\image\kimparkpenguin.jpg')
        st.header("전설의 김박펭귄 모험가의 여정을 담은 페이지입니다.")
        with st.sidebar:
            st.image(image_path, use_column_width=True)

            options = list(Menu)
            tabs = on_hover_tabs(
                tabName=[menu.value for menu in options],
                iconName=['list'] * len(options),
                default_choice=0,
                styles=get_sidebar_styles()

            )

            if tabs == Menu.study_group.value:
                study_options = list(StudyGroup)
                study_tabs = on_hover_tabs(
                    tabName=[menu.value for menu in study_options],
                    iconName=['list'] * len(study_options),
                    default_choice=0,
                    styles=get_sidebar_styles()

                )
                # 여기에 study_group 탭의 컨텐츠를 추가할 수 있습니다.
            elif tabs == Menu.story_group.value:
                story_options = list(StoryGroup)
                story_tabs = on_hover_tabs(
                    tabName=[menu.value for menu in story_options],
                    iconName=['list'] * len(story_options),
                    default_choice=0,
                    styles=get_sidebar_styles()

                )
                # 여기에 story_group 탭의 컨텐츠를 추가할 수 있습니다.
            elif tabs == Menu.profile_group.value:
                profile_options = list(ProfileGroup)
                profile_tabs = on_hover_tabs(
                    tabName=[menu.value for menu in profile_options],
                    iconName=['list'] * len(profile_options),
                    default_choice=0,
                    styles=get_sidebar_styles()
                )
                # 여기에 profile_group에 대한 코드를 작성할 수 있습니다.
                pass

dashboard_layout: DashLayout = DashLayout()
