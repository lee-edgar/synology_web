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

@singleton
class DashLayout:
    def __init__(self):
        self.submenu_mapping = {
            Menu.study_group: list(StudyGroup),
            Menu.story_group: list(StoryGroup),
            Menu.profile_group: list(ProfileGroup),
            Menu.portfolio_group: list(PortfolioGroup),
        }
        self.profile_layout = Profile()
        self.portfolio_layout = Portfolio()
        self.study_layout = Study()
        self.story_layout = Story()

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
        st.markdown(f' Update Time = {timedelta(seconds=etime - stime)}')


    def draw_sidebar(self):
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
            self.profile_layout.draw()
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


    # app/layout/dashboard.py
    # def draw_ProfileGroup_view(self, selected: str):
    #     try:
    #         response = requests.get(f"{BACKEND_URL}/careers")
    #         if response.status_code == 200:
    #             careers = response.json()
    #             st.title("🏢 경력 사항")
    #
    #             for career in careers:
    #                 with st.container():
    #                     col1, col2 = st.columns([3, 1])
    #
    #                     with col1:
    #                         # 회사명과 직책
    #                         st.subheader(f"{career['title']}")
    #                         st.write(f"🏢 **{career['company']}**  •  {career['company_type']}  •  {career['location']}")
    #
    #                     with col2:
    #                         # 근무 기간
    #                         period = f"{career['start_date']} ~ {career['end_date'] if career['end_date'] else '현재'}"
    #                         st.caption(f"🗓️ {period}")
    #
    #                     # 업무 설명
    #                     if career.get('description'):
    #                         st.markdown(career['description'])
    #
    #                     if career.get('files'):
    #                         try:
    #                             files = career.get('files')
    #                             # 파일 이름과 타입 추출
    #                             file_name = files[0]
    #                             file_type = files[1]
    #                             file_caption = files[2] if len(files) > 2 else None
    #
    #                             # 파일 타입에 따라 처리
    #                             if file_type == 'image':
    #                                 if file_caption is None :
    #                                     st.image(file_name, use_column_width='always')
    #                                 else:
    #                                     st.image(file_name, caption=file_caption, use_column_width='always')
    #                             elif file_type == 'pdf':
    #                                 st.write("📄 관련 문서")
    #                                 col1, col2 = st.columns([3, 1])
    #                                 with col1:
    #                                     st.write(f"• {file_name}")
    #                                 with col2:
    #                                     st.download_button(
    #                                         label="다운로드",
    #                                         data=file_name,  # 실제 파일 데이터를 전달해야 함
    #                                         file_name=file_name,
    #                                         mime="application/pdf"
    #                                     )
    #                         except json.JSONDecodeError as e:
    #                             st.error(f"파일 정보 파싱 오류: {str(e)}")
    #
    #                     # 태그 표시
    #                     if career.get('tags'):
    #                         try:
    #                             tags = career.get('tags')
    #                             max_columns = 1
    #                             for i in range(0, len(tags), max_columns):
    #                                 cols = st.columns(max_columns)
    #                                 for idx, tag in enumerate(tags[i:i + max_columns]):
    #                                     with cols[idx]:
    #                                         st.markdown(
    #                                             f"<span style='background-color: #f0f2f6; margin:left; padding: 2px 8px; border-radius: 12px;'>#{tag}</span>",
    #                                             unsafe_allow_html=True
    #                                         )
    #                         except json.JSONDecodeError as e:
    #                             st.error(f"태그 파싱 오류: {str(e)}")
    #                         st.write("---")  # 구분선
    #         else:
    #             st.error(f"데이터를 불러오는데 실패했습니다. (Status: {response.status_code})")
    #             if response.text:
    #                 st.write("Error details:", response.text)
    #
    #     except Exception as e:
    #         st.error("오류가 발생했습니다!")
    #         st.write("Error details:", str(e))
    #         st.markdown(PROFILEGROUP_VIEW_MARKDOWN)

dashboard_layout: DashLayout = DashLayout()