# import streamlit as st
# import time
# from datetime import datetime, timedelta
#
# import os
# from utils.singletonimport singleton
# from app.layout.const import *
# from st_on_hover_tabs import on_hover_tabs
# from style.style import get_sidebar_styles
# from streamlit import session_state as ss
# import requests
#
# @singleton
# class DashLayout:
#     def __init__(self):
#         pass
#
#     def draw_dashboard(self):
#         stime = time.time()
#         selected = self.draw_sidebar()
#         etime = time.time()
#         st.markdown(f' Update Time = {timedelta(seconds=etime - stime)}')
#         self.update_main_panel(selected=selected)
#
#     def draw_sidebar(self):
#
#         # api_url = "http://127.0.0.1:8000/players"
#         #
#         # # Streamlit 제목 설정
#         # st.title("Player Name Lookup")
#         #
#         # # 사용자로부터 player_id 입력받기
#         # player_id = st.number_input("Enter Player ID:", min_value=1, step=1)
#         #
#         # # 버튼 클릭 시 API 요청
#         # if st.button("Get Player Name"):
#         #     try:
#         #         # FastAPI 엔드포인트에 요청
#         #         response = requests.get(f"{api_url}/{player_id}")
#         #
#         #         # 응답이 성공적이면 이름 출력
#         #         if response.status_code == 200:
#         #             player_data = response.json()
#         #             st.success(f"Player Name: {player_data['name']}")
#         #         elif response.status_code == 404:
#         #             st.error("Player not found.")
#         #         else:
#         #             st.error(f"Error: {response.status_code}")
#         #     except requests.exceptions.RequestException as e:
#         #         st.error(f"Request failed: {e}")
#
#
#         # st.header("전설의 김박펭귄 모험가의 여정을 담은 페이지입니다.")
#         # st.image('app/image/kimparkpenguin.png', use_column_width='auto')
#         # if 'pdf_ref' not in ss:
#         #     ss.pdf_ref = None
#         # st.file_uploader("Upload PDF file", type=('pdf'), key='pdf')
#         # if ss.pdf:
#         #     ss.pdf_ref = ss.pdf  # backup
#         # if ss.pdf_ref:
#         #     binary_data = ss.pdf_ref.getvalue()
#         #     pdf_viewer(input=binary_data, width=700)
#         #
#         # options = list(Menu)
#         # tabs = on_hover_tabs(
#         #     tabName=[menu.value for menu in options],
#         #     iconName=['list'] * len(options),
#         #     default_choice=2,
#         #     styles=get_sidebar_styles()
#         #
#         # )
#         #
#         # if tabs == Menu.study_group.value:
#         #     study_options = list(StudyGroup)
#         #     study_tabs = on_hover_tabs(
#         #         tabName=[menu.value for menu in study_options],
#         #         iconName=['list'] * len(study_options),
#         #         default_choice=0,
#         #         styles=get_sidebar_styles()
#         #
#         #     )
#         #     # 여기에 study_group 탭의 컨텐츠를 추가할 수 있습니다.
#         # elif tabs == Menu.story_group.value:
#         #     story_options = list(StoryGroup)
#         #     story_tabs = on_hover_tabs(
#         #         tabName=[menu.value for menu in story_options],
#         #         iconName=['list'] * len(story_options),
#         #         default_choice=0,
#         #         styles=get_sidebar_styles()
#         #
#         #     )
#         #     # 여기에 story_group 탭의 컨텐츠를 추가할 수 있습니다.
#         # elif tabs == Menu.profile_group.value:
#         #     profile_options = list(ProfileGroup)
#         #     profile_tabs = on_hover_tabs(
#         #         tabName=[menu.value for menu in profile_options],
#         #         iconName=['list'] * len(profile_options),
#         #         default_choice=0,
#         #         styles=get_sidebar_styles()
#         #     )
#         #     # 여기에 profile_group에 대한 코드를 작성할 수 있습니다.
#         #     pass
#
#         st.sidebar.header("메뉴")
#         # Dictionary to map main categories to their subcategories
#         submenu_mapping = {
#             Menu.study_group: list(StudyGroup),
#             Menu.story_group: list(StoryGroup),
#             Menu.profile_group: list(ProfileGroup),
#             Menu.portfolio_group: list(PortfolioGroup),
#
#         }
#
#         # Initialize session state for menu
#         # if 'active_tab' not in st.session_state:
#         #     st.session_state.active_tab = None
#
#         # defalut를 profile
#         if 'active_tab' not in st.session_state:
#             st.session_state.active_tab = ProfileGroup.profile.value
#
#         # Display main categories with default expanded state
#         for menu in Menu:
#             with st.sidebar.expander(menu.value, expanded=True):
#                 for submenu in submenu_mapping[menu]:
#                     if st.button(submenu.value, key=f"{menu.value}-{submenu.value}"):
#                         st.session_state.active_tab = submenu.value
#         return st.session_state.active_tab
#
#     def update_main_panel(self, selected:str):
#         if selected in [item.value for item in ProfileGroup]:
#             self.draw_ProfileGroup_view(selected)
#         elif selected in [item.value for item in StoryGroup]:
#             self.draw_StoryGroup_view(selected)
#         elif selected in [item.value for item in StudyGroup]:
#             self.draw_StudyGroup_view(selected)
#         elif selected in [item.value for item in PortfolioGroup]:
#             self.draw_PortfolioGroup_view(selected)
#
#
#     def draw_ProfileGroup_view(self, selected):
#         st.markdown(f"{PROFILEGROUP_VIEW_MARKDOWN} ({selected})")
#
#     def draw_StoryGroup_view(self, selected):
#         st.markdown(f"{STORYGROUP_VIEW_MARKDOWN} ({selected})")
#
#     def draw_StudyGroup_view(self, selected):
#         st.markdown(f"{STUDYGROUP_VIEW_MARKDOWN} ({selected})")
#
#     def draw_PortfolioGroup_view(self, selected):
#         st.markdown(f"{PORTFOLIO_VIEW_MARKDOWN} ({selected})")
# dashboard_layout: DashLayout = DashLayout()


# # app/layout/dashboard.py
# import streamlit as st
# import time
# from datetime import datetime, timedelta
# from app.utils.singleton import singleton
# import requests
# from app.layout.const import *
#
#
# @singleton
# class DashLayout:
#     def __init__(self):
#         self.api_url = "http://localhost:8000/api"  # FastAPI 서버 주소
#
#         # API 서버 상태 체크
#         try:
#             requests.get(f"{self.api_url}/health")
#             st.session_state.api_connected = True
#         except:
#             st.session_state.api_connected = False
#
#         # URL 파라미터 체크
#         params = st.experimental_get_query_params()
#         current_page = params.get('page', ['profile'])[0]
#
#         if 'current_page' not in st.session_state:
#             st.session_state.current_page = current_page
#
#     def draw_dashboard(self):
#         if not st.session_state.api_connected:
#             st.error("API 서버에 연결할 수 없습니다.")
#             return
#
#         stime = time.time()
#         self.draw_sidebar()
#         etime = time.time()
#         st.markdown(f'Update Time = {timedelta(seconds=etime - stime)}')
#
#         self.show_page_content(st.session_state.current_page)
#
#     def draw_sidebar(self):
#         st.sidebar.header("메뉴")
#
#         # 각 메뉴 버튼
#         for page in ['profile', 'portfolio', 'study']:
#             if st.sidebar.button(page.title()):
#                 st.session_state.current_page = page
#                 st.experimental_set_query_params(page=page)
#                 st.rerun()
#
#     def show_page_content(self, page):
#         try:
#             # FastAPI에서 페이지 데이터 가져오기
#             response = requests.get(f"{self.api_url}/pages/{page}")
#             if response.status_code == 200:
#                 data = response.json()
#                 st.title(data["title"])
#                 st.write(data["content"])
#
#                 # 페이지별 추가 데이터 표시
#                 if page == "portfolio" and "projects" in data:
#                     for project in data["projects"]:
#                         st.write(project)
#
#                 elif page == "study" and "topics" in data:
#                     for topic in data["topics"]:
#                         st.write(topic)
#
#             else:
#                 st.error("페이지를 불러올 수 없습니다.")
#
#         except Exception as e:
#             st.error(f"에러가 발생했습니다: {str(e)}")
#
#
# dashboard_layout: DashLayout = DashLayout()

# backend/main.py
# app/layout/dashboard.py
# import streamlit as st
# import time
# from datetime import datetime, timedelta
# from utils.singleton import singleton
# from app.layout.const import *
# import requests
#
#
# @singleton
# class DashLayout:
#     def __init__(self):
#         self.api_url = "http://localhost:8000/api"
#
#         # submenu_mapping을 클래스 속성으로 이동
#         self.submenu_mapping = {
#             Menu.study_group: list(StudyGroup),
#             Menu.story_group: list(StoryGroup),
#             Menu.profile_group: list(ProfileGroup),
#             Menu.portfolio_group: list(PortfolioGroup),
#         }
#
#         # 기본 active_tab 설정
#         if 'active_tab' not in st.session_state:
#             st.session_state.active_tab = ProfileGroup.profile.value
#
#     def draw_dashboard(self):
#         stime = time.time()
#         selected = self.draw_sidebar()
#         etime = time.time()
#         st.markdown(f' Update Time = {timedelta(seconds=etime - stime)}')
#         self.update_main_panel(selected=selected)
#
#     def draw_sidebar(self):
#         st.sidebar.header("메뉴")
#
#         # Display main categories with default expanded state
#         for menu in Menu:
#             with st.sidebar.expander(menu.value, expanded=True):
#                 for submenu in self.submenu_mapping[menu]:
#                     if st.button(submenu.value, key=f"{menu.value}-{submenu.value}"):
#                         st.session_state.active_tab = submenu.value
#                         # URL 파라미터 업데이트
#                         st.experimental_set_query_params(
#                             group=menu.__class__.__name__,
#                             submenu=submenu.value
#                         )
#
#         return st.session_state.active_tab
#
#     def update_main_panel(self, selected: str):
#         try:
#             # 현재 선택된 메뉴에 해당하는 그룹 찾기
#             current_group = None
#             for menu in Menu:
#                 if selected in [item.value for item in self.submenu_mapping[menu]]:
#                     current_group = menu.__class__.__name__
#                     break
#
#             if current_group:
#                 # FastAPI에서 컨텐츠 가져오기
#                 response = requests.get(f"{self.api_url}/content/{current_group}/{selected}")
#                 if response.status_code == 200:
#                     content = response.json()
#                     st.title(content["title"])
#                     st.write(content["content"])
#                 else:
#                     # API 호출 실패시 기존 동작 유지
#                     if selected in [item.value for item in ProfileGroup]:
#                         self.draw_ProfileGroup_view(selected)
#                     elif selected in [item.value for item in StoryGroup]:
#                         self.draw_StoryGroup_view(selected)
#                     elif selected in [item.value for item in StudyGroup]:
#                         self.draw_StudyGroup_view(selected)
#                     elif selected in [item.value for item in PortfolioGroup]:
#                         self.draw_PortfolioGroup_view(selected)
#
#         except requests.exceptions.RequestException:
#             # API 서버 연결 실패시 기존 동작 유지
#             if selected in [item.value for item in ProfileGroup]:
#                 self.draw_ProfileGroup_view(selected)
#             elif selected in [item.value for item in StoryGroup]:
#                 self.draw_StoryGroup_view(selected)
#             elif selected in [item.value for item in StudyGroup]:
#                 self.draw_StudyGroup_view(selected)
#             elif selected in [item.value for item in PortfolioGroup]:
#                 self.draw_PortfolioGroup_view(selected)
#
#     # 기존 view 메소드들 유지
#     def draw_ProfileGroup_view(self, selected):
#         st.markdown(f"{PROFILEGROUP_VIEW_MARKDOWN} ({selected})")
#
#     def draw_StoryGroup_view(self, selected):
#         st.markdown(f"{STORYGROUP_VIEW_MARKDOWN} ({selected})")
#
#     def draw_StudyGroup_view(self, selected):
#         st.markdown(f"{STUDYGROUP_VIEW_MARKDOWN} ({selected})")
#
#     def draw_PortfolioGroup_view(self, selected):
#         st.markdown(f"{PORTFOLIO_VIEW_MARKDOWN} ({selected})")
#
#
# dashboard_layout: DashLayout = DashLayout()
import streamlit as st
import time
from datetime import datetime, timedelta
from utils.singleton import singleton
from app.layout.const import *
import requests
import json
from app.common.common import BACKEND_URL

@singleton
class DashLayout:
    def __init__(self):
        self.submenu_mapping = {
            Menu.study_group: list(StudyGroup),
            Menu.story_group: list(StoryGroup),
            Menu.profile_group: list(ProfileGroup),
            Menu.portfolio_group: list(PortfolioGroup),
        }
        # active_tab 초기화를 먼저 수행
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = ProfileGroup.profile.value
            # 기본 URL 파라미터도 설정
            st.query_params["group"] = Menu.profile_group.value
            st.query_params["submenu"] = ProfileGroup.profile.value
        # URL 파라미터 확인 (새로운 방식 사용)
        if 'group' in st.query_params and 'submenu' in st.query_params:
            st.session_state.active_tab = st.query_params.submenu
        elif 'active_tab' not in st.session_state:
            st.session_state.active_tab = ProfileGroup.profile.value

    def draw_dashboard(self):
        stime = time.time()
        selected = self.draw_sidebar()
        etime = time.time()
        st.markdown(f' Update Time = {timedelta(seconds=etime - stime)}')
        self.update_main_panel(selected=selected)


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


    def update_main_panel(self, selected: str):
        try:
            current_group, current_submenu = st.query_params.get("group"), st.query_params.get("submenu")

            if current_group and current_submenu:
                # API URL 구성
                api_url = f"{BACKEND_URL}/content/{current_group}/{current_submenu}"

                # 요청 시 헤더 추가
                headers = { 'Accept': 'application/json' }

                response = requests.get(api_url, headers=headers)

                try:
                    content = response.json()
                    if "error" in content:
                        st.error(content["error"])
                    else:
                        st.title(content["title"])
                        # st.write(content["subtitle"])
                        self.draw_ProfileGroup_view(selected)

                except json.JSONDecodeError as e:
                    st.error(f"JSON 파싱 오류: {str(e)}")
                    st.write('Full Response:', response.text)
            else:
                st.warning("No group or submenu parameters found")
                self._fallback_view(selected)

        except requests.exceptions.RequestException as e:
            st.error(f"Request Error: {str(e)}")
            self._fallback_view(selected)

    def _fallback_view(self, selected):
        if selected in [item.value for item in ProfileGroup]:
            # self.draw_ProfileGroup_view(selected)
            self.draw_ProfileGroup_view(selected)
        elif selected in [item.value for item in StoryGroup]:
            self.draw_StoryGroup_view(selected)
        elif selected in [item.value for item in StudyGroup]:
            self.draw_StudyGroup_view(selected)
        elif selected in [item.value for item in PortfolioGroup]:
            self.draw_PortfolioGroup_view(selected)

    # def draw_ProfileGroup_view(self, selected):
    #     st.markdown(f"{PROFILEGROUP_VIEW_MARKDOWN} ({selected})")

    def draw_StoryGroup_view(self, selected):
        st.markdown(f"{STORYGROUP_VIEW_MARKDOWN} ({selected})")

    def draw_StudyGroup_view(self, selected):
        st.markdown(f"{STUDYGROUP_VIEW_MARKDOWN} ({selected})")

    def draw_PortfolioGroup_view(self, selected):
        st.markdown(f"{PORTFOLIO_VIEW_MARKDOWN} ({selected})")

    # app/layout/dashboard.py
    def draw_ProfileGroup_view(self, selected: str):
        try:
            response = requests.get(f"{BACKEND_URL}/careers")
            if response.status_code == 200:
                careers = response.json()
                st.title("🏢 경력 사항")
                # st.write('careers',careers[0]['files'])

                for career in careers:
                    with st.container():
                        col1, col2 = st.columns([3, 1])

                        with col1:
                            # 회사명과 직책
                            st.subheader(f"{career['title']}")
                            st.write(f"🏢 **{career['company']}**  •  {career['company_type']}  •  {career['location']}")

                        with col2:
                            # 근무 기간
                            period = f"{career['start_date']} ~ {career['end_date'] if career['end_date'] else '현재'}"
                            st.caption(f"🗓️ {period}")

                        # 업무 설명
                        if career.get('description'):
                            st.markdown(career['description'])

                        if career.get('files'):
                            try:
                                files = career.get('files').split(", ")  # 쉼표와 공백을 기준으로 분리
                                # 파일 이름과 타입 추출
                                file_name = files[0]
                                file_type = files[1]
                                file_caption = files[2] if len(files) > 2 else None

                                # 파일 타입에 따라 처리
                                if file_type == 'image':
                                    if file_caption is None :
                                        st.image(file_name)
                                    else:
                                        st.image(file_name, caption=file_caption)
                                elif file_type == 'pdf':
                                    st.write("📄 관련 문서")
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.write(f"• {file_name}")
                                    with col2:
                                        st.download_button(
                                            label="다운로드",
                                            data=file_name,  # 실제 파일 데이터를 전달해야 함
                                            file_name=file_name,
                                            mime="application/pdf"
                                        )
                            except json.JSONDecodeError as e:
                                st.error(f"파일 정보 파싱 오류: {str(e)}")

                        # 태그 표시
                        if career.get('tags'):
                            try:
                                tags = career.get('tags').split(", ")
                                max_columns = 1
                                for i in range(0, len(tags), max_columns):
                                    cols = st.columns(max_columns)
                                    for idx, tag in enumerate(tags[i:i + max_columns]):
                                        with cols[idx]:
                                            st.markdown(
                                                f"<span style='background-color: #f0f2f6; margin:left; padding: 2px 8px; border-radius: 12px;'>#{tag}</span>",
                                                unsafe_allow_html=True
                                            )
                            except json.JSONDecodeError as e:
                                st.error(f"태그 파싱 오류: {str(e)}")
                            st.write("---")  # 구분선

            else:
                st.error(f"데이터를 불러오는데 실패했습니다. (Status: {response.status_code})")
                if response.text:
                    st.write("Error details:", response.text)

        except Exception as e:
            st.error("오류가 발생했습니다!")
            st.write("Error details:", str(e))
            st.markdown(PROFILEGROUP_VIEW_MARKDOWN)

dashboard_layout: DashLayout = DashLayout()