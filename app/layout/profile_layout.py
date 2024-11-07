import streamlit as st
import requests
import json


from app.common.common import BACKEND_URL
from app.utils.singleton import  singleton
from app.layout.const import *

class Profile:
    def __init__(self):
        pass

    def draw(self):
        st.markdown(f"{PROFILEGROUP_VIEW_MARKDOWN}")
        self.draw_profile_group_view()

    def draw_profile_group_view(self):
        try:
            response = requests.get(f"{BACKEND_URL}/careers")
            if response.status_code == 200:
                careers = response.json()
                st.title("🏢 경력 사항")
                for career in careers:
                    with st.expander(f"{career['title']}", expanded=True):
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

                            if career.get('files') and career.get('files') != ["[]"]:
                                # st.write("Files content:", career.get('files'))  # 디버깅용

                                try:
                                    files = career.get('files')
                                    # 파일 이름과 타입 추출
                                    file_name = files[0]
                                    file_type = files[1]
                                    file_caption = files[2] if len(files) > 2 else None

                                    # 파일 타입에 따라 처리
                                    if file_type == 'image':
                                        if file_caption is None:
                                            st.image(file_name, use_column_width='always')
                                        else:
                                            st.image(file_name, caption=file_caption, use_column_width='always')
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
                                    tags = career.get('tags')
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