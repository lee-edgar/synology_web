import streamlit as st
import requests
import json
from app.common.common import BACKEND_URL
from app.utils.singleton import  singleton
from app.layout.const import *
from streamlit_pdf_viewer import pdf_viewer
from datetime import date, datetime, timedelta
from app.session.channel_healthcare_session_service import channel_healthcare_session_service
from app.utils.streamlit_utils import get_session_state, update_session_state, initialize_session_state, str2datetime, \
    str2datetime_strptim, format_date_range
import plotly.graph_objects as go
import pandas as pd
from typing import List
from backend.service.bollinger_band_service import bollinger


class Portfolio_Channel_Layout():
    def __init__(self):
        pass

    def initialize_session_render(self):
        '''
        초기 세션 상태를 설정하고 UI 요소를 렌더링합니다.

        Streamlit은 매번 새로고침될 때 전체 스크립트를 다시 실행하는 특성을 가집니다.
        따라서 클래스의 __init__ 메서드에서 실행된 초기화 코드는 유지되지 않고,
        새로고침 시 다시 초기화가 필요합니다.

        이 함수는 Streamlit의 세션 상태(st.session_state)를 강제로 초기화한 뒤,
        필요한 데이터를 세팅하고 화면(UI)을 구성하는 역할을 합니다.

        주요 역할:
        1. `initialize_session_state(DEFAULT_SESSION_STATE)`를 통해 세션 상태를 설정합니다.
            - 세션 상태는 Streamlit의 전역 상태 관리 객체로, 화면 간 데이터 공유와 유지에 사용됩니다.
        2. Streamlit의 동작 방식에 따라, 이 함수는 특정 시점에서 호출되어야만 세션 상태가 반영됩니다.
        3. 초기화 후, 데이터를 활용해 그래프나 표 등의 UI 요소를 렌더링합니다.

        Streamlit을 처음 접하거나 익숙하지 않은 개발자를 위해:
        - Streamlit은 페이지 새로고침이나 특정 UI 이벤트 발생 시, 전체 코드가 다시 실행됩니다.
        - `__init__` 메서드에 초기화 코드를 넣더라도, Streamlit의 재실행 특성 때문에 유지되지 않습니다.
        - 따라서, **필요한 시점**에서 상태를 초기화하고 UI를 렌더링하는 별도 함수를 정의하여 호출해야 합니다.
        """
        '''
        initialize_session_state(DEFAULT_SESSION_STATE)
        self.render_layout()


    def render_layout(self):
        """
        그래프 및 테이블 렌더링 호출
        """

        st.error(""" 
                이 페이지는 채널헬스케어에서 준비했던 당뇨 관리 서비스의 주요 기능 중 일부를 새롭게 재구성한 결과물입니다. 
                약 300여 명의 베타테스터들과 함께 실질적인 테스트를 진행한 후 도출된 결과에 기반하였습니다.
                제가 가지고 있는 Synology NAS 환경에서 FastAPI와 Streamlit을 활용해 MVC 패턴을 기반으로 설계 및 구현하였으며, 기존 회사 소스를 사용하지 않고 새롭게 개발했습니다. 
                데이터는 유사한 더미 데이터를 생성해 활용했습니다. 특히, 볼린저 밴드 분석 기능 등 제가 생각했던 아이디어를 반영한 것으로, 혈당 데이터를 개인화된 범위에서 분석 및 시각화할 수 있도록 설계되었음을 알립니다.
                """)


        # channel_healthcare_session_service.draw_user_navigation()
        self.draw_user_info()

        user_uid = get_session_state(SESSION_USER_UID)
        viz_start_date = get_session_state(SESSION_VIZ_START_DATE)
        viz_end_date = get_session_state(SESSION_VIZ_END_DATE)
        load_start_date = get_session_state(SESSION_LOAD_START_DATE)
        load_end_date= get_session_state(SESSION_LOAD_END_DATE)

        self.draw_summary(user_uid, viz_start_date, viz_end_date)
        st.write('---')
        self.draw_mealzone_graph(user_uid, viz_start_date, viz_end_date)
        st.write('---')
        self.draw_bollinger_bend_graph(user_uid, load_start_date, load_end_date)
        st.write('---')
        self.draw_allday_graph(user_uid, load_start_date, load_end_date )
        st.write('---')

        # 개인정보 관련으로 인해 hide
        # self.draw_table(user_uid, viz_start_date, viz_end_date)

    def draw_user_info(self):
        st.info(""" 시각화 하고자 하는 유저를 선택 할 수 있습니다. 캘린더를 이용하여 원하는 날짜를 지정 할 수 있으며, 화살표 버튼으로 이전날짜와 이후날짜를 선택 할 수 있습니다. 
        캘린더의 기간을 3일 선택을 하고 이전과 이후를 누른다면 해당 기간만큼 날짜가 미뤄지고 땡겨집니다. 추가로, 이 페이지는 인터렉티브한 데이터 시각화 기능을 통해 데이터를 동적으로 분석할 수 있도록 설계하였습니다. """, icon="ℹ️")
        col1, col2, col3, col4, col5 = st.columns((1, 0.5, 1, 1, 1))
        error_message = None

        with col1:
            st.write(""" 187: 열심히 관리하는 당뇨 초기 환자 / 350: 일반적인 당뇨 환자 """)


        with col2 :
            selected_user = st.selectbox(" 유저 선택 ", USER_GROUP, index=0,  label_visibility='collapsed')

            user_date_range = USER_DATE_RANGES.get(selected_user, {})
            load_start_date = user_date_range.get("load_start_date")
            load_end_date = user_date_range.get("load_end_date")
            viz_start_date = user_date_range.get("viz_start_date")
            viz_end_date = user_date_range.get("viz_end_date")

            if get_session_state(SESSION_USER_UID) != selected_user:
                update_session_state(SESSION_USER_UID, selected_user)
                update_session_state(SESSION_LOAD_START_DATE, load_start_date)
                update_session_state(SESSION_LOAD_END_DATE, load_end_date)
                update_session_state(SESSION_VIZ_START_DATE, viz_start_date)
                update_session_state(SESSION_VIZ_END_DATE, viz_end_date)

            # st.write('get session', get_session_state(SESSION_USER_UID),  get_session_state(SESSION_LOAD_START_DATE),  get_session_state(SESSION_LOAD_END_DATE),
            #          get_session_state(SESSION_VIZ_START_DATE), get_session_state(SESSION_VIZ_END_DATE))
            channel_healthcare_session_service.request_data(selected_user, load_start_date, load_end_date)

        # channel_healthcare_session_service.update_navigatation()

        # 현재 viz_start_date와 viz_end_date를 세션에서 가져오기
        viz_start_date = get_session_state(SESSION_VIZ_START_DATE)
        viz_end_date = get_session_state(SESSION_VIZ_END_DATE)

        # "이전" 버튼 클릭 시 처리
        with col3:
            if st.button(":arrow_backward: 이전", use_container_width=True):

                # # 날짜를 하루 전으로 이동
                new_viz_start_date = viz_start_date - timedelta(days=1)
                new_viz_end_date = viz_end_date - timedelta(days=1)

                # 이동한 날짜가 load_start_date와 load_end_date 범위 내에 있도록 제한
                if new_viz_start_date >= load_start_date:
                    viz_start_date = new_viz_start_date
                    viz_end_date = new_viz_end_date
                    update_session_state(SESSION_VIZ_START_DATE, viz_start_date)
                    update_session_state(SESSION_VIZ_END_DATE, viz_end_date)
                else:
                    error_message = (f"더 이상 이전 날짜로 이동할 수 없습니다. {load_start_date} ~ {load_end_date}")


        # "다음" 버튼 클릭 시 처리
        with col5:
            if st.button("다음 :arrow_forward:", use_container_width=True):

                # 날짜를 하루 후로 이동
                new_viz_start_date = viz_start_date + timedelta(days=1)
                new_viz_end_date = viz_end_date + timedelta(days=1)

                # 이동한 날짜가 load_start_date와 load_end_date 범위 내에 있도록 제한
                if new_viz_end_date <= load_end_date:
                    viz_start_date = new_viz_start_date
                    viz_end_date = new_viz_end_date
                    update_session_state(SESSION_VIZ_START_DATE, viz_start_date)
                    update_session_state(SESSION_VIZ_END_DATE, viz_end_date)
                else:
                    error_message = (f"더 이상 다음 날짜로 이동할 수 없습니다. {load_start_date} ~ {load_end_date}")

        # 현재 날짜 출력
        with col4:
            clander_date = st.date_input('날짜 선택',
                          (viz_start_date.date(), viz_end_date.date()),
                          label_visibility='collapsed')

            if clander_date[0] <= clander_date[1]:
                # sdate, edate = clander_date[0], clander_date[1]
                new_viz_start_date, new_viz_end_date = format_date_range(clander_date[0], clander_date[1])

                # 선택된 날짜 범위가 load_start_date ~ load_end_date 범위를 초과하지 않도록 제한
                if new_viz_start_date >= load_start_date and new_viz_end_date <= load_end_date:
                    update_session_state(SESSION_VIZ_START_DATE, new_viz_start_date)
                    update_session_state(SESSION_VIZ_END_DATE, new_viz_end_date)
                else:
                    error_message = (f"선택한 날짜는 허용 범위를 초과했습니다. {load_start_date.date()} ~ {load_end_date.date()}")

        if error_message is not None:
            st.error(f'{error_message}')




    def draw_bollinger_bend_graph(self, user_uid, sdate, edate):
        st.markdown('#### Bollinger Bend Glucose Trends')

        col1, col2, col3 = st.columns((1, 7, 3))

        with col1:
            show_moving_avg = st.checkbox("Show Moving Average", value=True, key='bollinger_show_moving_avg')
            band_range = st.checkbox("Show Band Range (Upper/Lower)", value=True, key='bollinger_show_band_range')
            std_multiplier = st.slider("Select Standard Deviation Multiplier", 1.0, 3.0, 2.0, 0.1, key='bollinger_std_multiplier')
            window = st.slider("Select Moving Average Window", 5, 50, 10, 1, key='bollinger_window')
            smoothing_window = st.slider("Select Smoothing Window", 3, 20, 5, 1, key='bollinger_smoothing_window')
        with col2:
            fig = go.Figure()
            self.plot_cgm(fig, user_uid, sdate, edate, 'all')
            fig, bollinger_tir_df = self.bollinger_band(fig, user_uid, channel_healthcare_session_service.get_cgm_data(user_uid, sdate, edate),
                                std_multiplier, window, smoothing_window, show_moving_avg, band_range, sdate, edate, 'all')
            col1.write(f"### Bollinger TIR ")
            col1.write(bollinger_tir_df)

            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=500)
            st.plotly_chart(fig, use_container_width=True)
            st.write("""ℹ️ 연속혈당 데이터의 정확한 판단을 위한 최소 기간인 2주 데이터를 표시합니다.""")

        with col3.expander('설명', expanded=True):
            st.info(""" 
                        기존 CGM(Continuous Glucose Monitoring) 그래프는 TIR 범위를 80~180 mg/dL로 제한하여, 혈당이 높은 환자에게 적절한 정보를 제공하지 못하는 한계가 있습니다.
                        이에 반해 볼린저 밴드는 혈당 데이터를 감싸는 개인화된 안전 범위를 제공하여 환자별 혈당 패턴에 맞춘 TIR 범위를 분석 할 수 있습니다.
                        
                        **주황색 영역**  
                        안정적인 혈당 관리 상태를 나타냅니다. 이 영역을 벗어날 경우, 혈당 스파이크(고혈당), 저혈당 위험으로 간주할 수 있습니다.
                        
                        **초록색 이동 평균선**  
                        전반적인 혈당 추세를 이해하는 가이드로, 환자가 안정적인 혈당 관리를 유지하고 있는지 확인할 수 있는 지표입니다.
                        
                        볼린저 밴드는 환자 중심의 분석을 가능하게 하며, 혈당 데이터를 직관적으로 이해하고 맞춤형 관리 전략을 수립하는데 도움을 줄 수 있습니다. 볼린저 밴드는 더 나은 혈당 관리를 위한 강력한 도구로, 환자의 혈당 상태를 보다 효과적으로 지원합니다.
                        """, icon="ℹ️")
            st.info(""" 
                        #### 좌측 옵션 사이드바
                        
                        **표준 편차 배수 (Std Multiplier)**  
                        볼린저 밴드의 상한선과 하한선을 결정합니다.
                        값이 작아질수록 밴드가 좁아져 민감하게 반응하며, 커질수록 밴드가 넓어져 변동성을 더 많이 수용합니다.
    
                        **이동 평균 윈도우 (Moving Avg Window)**  
                         혈당의 전반적인 추세를 계산하는 데 사용됩니다.
                        값이 작아질수록 짧은 기간의 변화를 잘 반영하며, 커질수록 장기적인 추세를 부드럽게 보여줍니다.
    
                        **스무싱 윈도우 (Smoothing Window)**  
                        이동 평균과 볼린저 밴드를 부드럽게 표시합니다.
                        값이 작아질수록 원본 데이터에 가깝게 표현되며, 커질수록 그래프가 부드럽고 노이즈가 줄어듭니다.
                        
                        좌측 옵션 사이드바의 값을 변경하면 하단 Bollinger TIR값도 변경되는 동적인 기능
                        """, icon="ℹ️")

    def draw_allday_graph(self, user_uid, sdate, edate):
        st.markdown('#### Overall Blood Glucose Trends')
        col1, col2, col3 = st.columns((1, 7, 3))


        with col1:
            meal_mode = st.radio("Select meal type:", ["Invisible", "Meal", "Meal Zone(4H)"], index=0, horizontal=True)
            exercise_mode = st.radio("Select exercise type", ["Invisible", "Visible"], index=0, horizontal=True)
            bollinger_bend_mode = st.radio("Select bollinger bend type", ["Invisible", "Visible"], index=0,horizontal=True, key='all_day_bollinger_bend_mode')

            if bollinger_bend_mode == 'Visible':
                show_moving_avg = st.checkbox("Show Moving Average", value=True, key='normal_show_moving_avg')
                band_range = st.checkbox("Show Band Range (Upper/Lower)", value=True, key='normal_band_range')

                std_multiplier = st.slider("Select Standard Deviation Multiplier", 1.0, 3.0, 2.0, 0.1, key='normal_std_multiplier')
                window = st.slider("Select Moving Average Window", 5, 50, 10, 1, key='normal_window')
                smoothing_window = st.slider("Select Smoothing Window", 3, 20, 5, 1, key='normal_smoothing_window')
            else:
                std_multiplier, window, smoothing_window = 2.0, 10, 5

        with col2:
            fig = go.Figure()
            self.plot_cgm(fig, user_uid, sdate, edate, 'all')

            if meal_mode == "Meal":
                self.plot_meal(fig, user_uid, sdate, edate, 'all')
            elif meal_mode == "Meal Zone(4H)":
                self.plot_meal_zone(fig, user_uid, sdate, edate, 'all')
            elif meal_mode =="Invisible":
                pass
            if exercise_mode == 'Visible':
                self.plot_exercise(fig, user_uid, sdate, edate, 'all')

            if bollinger_bend_mode == 'Visible':
                fig, bollinger_tir_df = self.bollinger_band(fig, user_uid, channel_healthcare_session_service.get_cgm_data(user_uid, sdate, edate), std_multiplier, window, smoothing_window, show_moving_avg, band_range, sdate, edate, 'all')
                col1.write(f"### Bollinger TIR ")
                col1.write(bollinger_tir_df)
            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=500)
            st.plotly_chart(fig, use_container_width=True)
            st.write("""ℹ️ 연속혈당 데이터의 정확한 판단을 위한 최소 기간인 2주 데이터를 표시합니다.""")


        with col3.expander('설명', expanded=True):
            st.info("""
                                    Overall Blood Glucose Trend는 환자의 혈당 데이터를 심층적으로 분석할 수 있는 다양한 도구와 시각적 요소를 제공합니다. 사용자는 볼린저 밴드, Meal Zone(식사 시간대), 운동 데이터, 일별 최고 혈당 값 등의 요소를 조합하여 자신만의 혈당 패턴을 직관적으로 파악하고, 맞춤형 혈당 관리 전략을 수립할 수 있습니다.

                                    **옵션을 활용한 심화 분석**  
                                    Select Meal Type : 개별 식사 시간대 또는 Meal Zone을 시각화하여 각 식사와 혈당 변화를 연결할 수 있습니다.
                                    Select Exercis Type : 운동 시간이 포함된 데이터를 시각화하여 혈당 조절에 운동이 미친 영향을 분석할 수 있습니다.
                                    Select Bollinger Band Type : 볼린저 밴드를 활성화하여 혈당 변동성을 직관적으로 파악하고 안정적인 혈당 관리 상태를 확인할 수 있습니다.
                                    
                                    **Meal Zone 개념**  
                                    Meal Zone은 식사 시작 시간부터 4시간 동안의 혈당 변화를 분석하기 위한 구간입니다. 이 시간 동안 혈당은 일반적으로 상승 후 정상 범위로 회복됩니다. 이 구간을 통해 식사 후 혈당의 상승과 회복 패턴을 명확히 관찰할 수 있습니다.
                                    볼린저 밴드는 개인화된 혈당 변동 영역을 제공하며, 식사 시간대의 혈당 관리를 평가 하는 데 효과적입니다.
                                    
                                    **볼린저 밴드 활용**  
                                    볼린저 밴드는 개인화된 혈당 변동 영역을 제공하며, 식사 시간대의 혈당 관리를 평가하는데 효과적입니다.
                                    볼린저 밴드 상한선(Upper Band)을 초과하면 식후 혈당 스파이크가 발생했음을 나타내며, 이는 식사량 조절인 ㅏ식단 개선이 필요함을 시사합니다.
                                    볼린저 밴드 하한선(Lower Band)에 도달하거나 근접하면 저혈당 위험이 있음을 나타낼 수 있습니다.
                                    
                                    **비교 분석**  
                                    여러 Meal Zone을 비교하여 시간대별 혈당 패턴을 분석하고 특정 식단대에서 반복적으로 높은 혈당이 나타나는 원인을 파악할 수 있습니다. 예를 들어, 저녁 식사 시간의 Meal Zone이 다른 시간대보다 자주 볼린저 밴드를 초과한다면, 해당 시간의 식단이나 활동량에 대한 재평가가 필요할 수 있습니다.
                                    """, icon="ℹ️")




    def draw_summary(self, user_uid, sdate, edate):
        st.markdown('#### Daily Summary')
        col1, col2, col3 = st.columns((1, 7, 3))
        with col2:
            fig = go.Figure()
            self.plot_cgm(fig, user_uid, sdate, edate, 'selected')
            self.plot_exercise(fig, user_uid, sdate, edate, 'selected')
            self.plot_meal(fig, user_uid, sdate, edate, 'selected')
            self.plot_medicine(fig, user_uid, sdate)
            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10),height=200)  # 마진 최소화

            st.plotly_chart(fig , use_container_width=True)
        with col3.expander('설명', expanded=True):
            st.info(""" Daily Summary는 선택한 기간의 식사(식사 시작 시간 ~ 식사 종료 시간이며, 'Meal Zone' 과는 무관함), 운동, 복약, 혈당, 최대 혈당값, 최소 혈당값 등을 간단하게 요약 된 그래프를 볼 수 있습니다. 좀 더 다양한 멀티모달 정보(물 섭취, 수면, 처치 및 치료)들을 추가로 업로드 하기에 적절합니다. """, icon="ℹ️")

    def draw_mealzone_graph(self,  user_uid, sdate, edate):
        st.markdown('#### Meal Zone Analysis(4hours)')
        col1, col2, col3 = st.columns((1, 7, 3))

        with col1:
            bollinger_bend_mode = st.radio("Select bollinger bend type", ["Invisible", "Visible"], index=0,horizontal=True, key='daily_bollinger_bend_mode')
            if bollinger_bend_mode == 'Visible':
                show_moving_avg = st.checkbox("Show Moving Average", value=True, key='sub_show_moving_avg')
                band_range = st.checkbox("Show Band Range (Upper/Lower)", value=True, key='sub_show_moving_avg_band_range')

                std_multiplier = st.slider("Select Standard Deviation Multiplier", 1.0, 3.0, 2.0, 0.1, key='sub_show_moving_avg_std_multiplier')
                window = st.slider("Select Moving Average Window", 5, 50, 10, 1, key='sub_show_moving_avg_window')
                smoothing_window = st.slider("Select Smoothing Window", 3, 20, 5, 1, key='sub_show_moving_avg_smoothing_window')
            else:
                std_multiplier, window, smoothing_window = 2.0, 10, 5

        with col2:
            fig = go.Figure()
            self.plot_cgm(fig, user_uid, sdate, edate, 'selected')
            self.plot_meal_zone(fig, user_uid, sdate, edate, 'selected')
            if bollinger_bend_mode == 'Visible':
                fig, bollinger_tir_df = self.bollinger_band(fig, user_uid,
                                    channel_healthcare_session_service.get_cgm_data(user_uid, sdate, edate),
                                    std_multiplier, window, smoothing_window, show_moving_avg, band_range, sdate, edate, 'selected')

                col1.write(f"### Bollinger TIR")
                col1.write(bollinger_tir_df)
            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10),height=300)
            st.plotly_chart(fig, use_container_width=True)
            st.write('ℹ️ 칼로리는 더미로 생성하였으며, 탄,단,지 등의 섭취정보 DB가 있으면 일일 권장 섭취량 등의 자세한 설명 가능')
            self.plot_meal_food(get_session_state(SESSION_MEAL_ID))


        with col3.expander('설명', expanded=True):
            st.info("""

                                    **Meal Zone 개념**  
                                    Meal Zone은 식사 시작 시간부터 식사 시작 후 4시간까지의 구간을 나타냅니다. 이 구간은 식사에 따른 혈당 변화를 관찰하는 데 중요한 기준으로, 혈당이 식사 직후 상승한 후 최고점에 도달하고, 다시 정상 범위로 점차 회복되는 패턴을 명확히 보여줍니다.
                                    
                                    **회색영역**  
                                    일반적인 혈당의 범위는 80~180 mg/dL이며, 그래프에서 이 범위(y axis)를 회색영역으로 표시하였습니다.

                                    **분석 그래프 설명**  
                                    혈당 그래프와 Meal Zone에 속한 식단을 통해 해당 식단이 적절한지 객관적으로 평가 할 수 있습니다. 볼린저 밴드를 활용하여 혈당이 안정적으로 관리되었는지 확인할 수 있습니다. 이를 통해 식단이 혈당 관리에 적합했는지, 개선이 필요한지 판단할 수 있습니다. Meal Zone 내에서 최고 혈당, 최저 혈당, 그리고 혈당의 상승 및 하강 패턴을 시각적으로 확인 할 수 있습니다.

                                    **Meal Zone과 혈당 관리**  
                                    **혈당이 일반적인 범위(80~180 mg/dL)**에 속할 경우 TIR 값을 통해 혈당 관리 상태를 평가할 수 있습니다.(*TIR 값이 높을 수록 혈당이 정상 범위에 머물렀음을 의미합니다. 혈당이 정상 범주를 크게 벗어나는 경우, TIR 값이 낮거나 0이 될 수 있습니다. 이때, 개인화된 혈당 범위를 기반으로 한 TIR 값을 보고 싶다면, 볼린저 밴드를 활용해 혈당 흐름과 변동성을 확인할 수 있습니다.

                                    **식단 개선에 대한 도움**  
                                    그래프와 Meal Zone에 표시된 식단 정보를  통해 먹어도 되는 식단인지, 혹은 먹지 말아야 할 식단인지 유추가 가능합니다. 이를 바탕으로 다음 식단에 대한 개선 방향을 설정하고, 더 나은 혈당 관리를 도모할 수 있습니다.

                                    """, icon="ℹ️")




    def draw_table(self, user_uid, sdate, edate):
        mode = st.radio('회원 정보 탭', [item.value for item in TableView],
                        horizontal=True, label_visibility='collapsed')
        st.info(st.session_state.data_call_session)


        if mode == TableView.cgm:
            df = channel_healthcare_session_service.get_cgm_data(user_uid, sdate, edate)
            df['std_time'] = pd.to_datetime(df['std_time'])
            df = df[(df['std_time'] >= sdate) & (df['std_time'] < edate)]
            st.dataframe(df)

        elif mode == TableView.meal:
            st.dataframe(channel_healthcare_session_service.get_meal_data(
                user_uid,
                sdate,
                edate)
            )

        elif mode == TableView.exercise:
            st.dataframe(channel_healthcare_session_service.get_exercise_data(
                user_uid,
                sdate,
                edate)
            )

        elif mode == TableView.medicine:
            st.dataframe(channel_healthcare_session_service.get_medicine_data(
                user_uid,
                sdate)
            )

    def bollinger_band(self, fig, user_uid, df, std_multiplier, window, smoothing_window, show_moving_avg, band_range, sdate, edate, mode):
        df['std_time'] = pd.to_datetime(df['std_time'])
        df['date'] = df['std_time'].dt.date
        df = df.sort_values(by=['date', 'std_time'])

        if mode == 'selected':
            df = df[(df['std_time'] >= sdate) & (df['std_time'] < edate)]
        elif mode == "all":
            pass
        else:
            raise ValueError("Invalid mode. Choose 'all' or 'selected'.")

        daily_dataframes = []
        bollinger_tir_data = []
        for date, daily_df in df.groupby('date'):

            if len(daily_df) < window:
                st.warning(f"Insufficient data points for {date}: {len(daily_df)} (required: {window})")
                continue

            daily_df['moving_avg'] = daily_df['bg'].rolling(window=window).mean().fillna(method='bfill')
            daily_df['moving_std'] = daily_df['bg'].rolling(window=window).std().fillna(method='bfill')

            daily_df['upper_band'] = daily_df['moving_avg'] + (std_multiplier * daily_df['moving_std'])
            daily_df['lower_band'] = daily_df['moving_avg'] - (std_multiplier * daily_df['moving_std'])

            bollinger_tir_value = channel_healthcare_session_service.calculate_bollinger_tir(daily_df)
            bollinger_tir_data.append({'date': date, 'Bollinger TIR(%)': bollinger_tir_value})

            daily_dataframes.append(daily_df)

        all_daily_data = pd.concat(daily_dataframes)
        all_daily_data['bg_smooth'] = all_daily_data['bg'].rolling(window=smoothing_window).mean()
        all_daily_data['upper_band_smooth'] = all_daily_data['upper_band'].rolling(window=smoothing_window).mean()
        all_daily_data['lower_band_smooth'] = all_daily_data['lower_band'].rolling(window=smoothing_window).mean()
        all_daily_data['moving_avg_smooth'] = all_daily_data['moving_avg'].rolling(window=smoothing_window).mean()

        # 전체 Bollinger Band TIR
        overall_bollinger_tir = channel_healthcare_session_service.calculate_bollinger_tir(all_daily_data)
        bollinger_tir_df = pd.DataFrame(bollinger_tir_data)
        bollinger_tir_df.loc[len(bollinger_tir_df)] = {'date': '전체 평균', 'Bollinger TIR(%)': overall_bollinger_tir}


        if band_range:
            fig.add_trace(go.Scatter(
                x=all_daily_data['std_time'], y=all_daily_data['upper_band_smooth'],
                mode='lines',
                name=f'Upper Band (Std x {std_multiplier})',
                line=dict(color='rgba(255, 204, 0, 1.0)', dash='solid')
            ))
            fig.add_trace(go.Scatter(
                x=all_daily_data['std_time'], y=all_daily_data['lower_band_smooth'],
                mode='lines',
                name=f'Lower Band (Std x {std_multiplier})',
                line=dict(color='rgba(255, 204, 0, 1.0)', dash='solid'),
                fill='tonexty',  # 상단 밴드와 하단 밴드 사이를 채움
                fillcolor='rgba(255, 204, 0, 0.2)'
            ))
        if show_moving_avg:
            fig.add_trace(go.Scatter(
                x=all_daily_data['std_time'], y=all_daily_data['moving_avg_smooth'],
                mode='lines',
                name='Moving Average (Smoothed)',
                line=dict(color='green'),
                ))
        return fig, bollinger_tir_df

    def plot_cgm(self, fig, user_uid: int, sdate: datetime, edate: datetime, mode: str):
        df = channel_healthcare_session_service.get_cgm_data(user_uid, sdate, edate)

        df['std_time'] = pd.to_datetime(df['std_time'])
        if mode == 'selected':
            df = df[(df['std_time'] >= sdate) & (df['std_time'] < edate)]
        elif mode == "all":
            pass
        else:
            raise ValueError("Invalid mode. Choose 'all' or 'selected'.")

        df_line_list = channel_healthcare_session_service.split_by_time_gap(df[['std_time', 'bg']])
        all_y_axis_values = channel_healthcare_session_service.extract_values_from_segments(df_line_list)

        for df_list in df_line_list:
            fig.add_trace(go.Scatter(x=df_list.std_time, y=df_list.bg, mode='lines', line=dict(color='blue')))

        y_axis_range = channel_healthcare_session_service.calculate_y_axis_range(all_y_axis_values, mode)
        x_axis_dtick = channel_healthcare_session_service.calculate_x_axis_range(
            pd.to_datetime(get_session_state(SESSION_VIZ_START_DATE)),
            pd.to_datetime(get_session_state(SESSION_VIZ_END_DATE)),
            mode
        )

        # 일별 또는 전체 최대값 추가
        channel_healthcare_session_service.add_marker(fig, df, column='bg', marker_type='max', color='red',
                                                      label='Max BG', mode=mode)
        channel_healthcare_session_service.add_marker(fig, df, column='bg', marker_type='min', color='red',
                                                      label='Min BG', mode=mode)
        channel_healthcare_session_service.add_marker(fig, df, column='bg', marker_type='mean', color='purple',
                                                      label='Mean BG', mode=mode)

        fig.add_hrect(y0=70, y1=180, fillcolor='gray', opacity=0.09)
        fig.update_layout(
            yaxis=dict(range=y_axis_range, tickmode='linear', tick0=0, dtick=20, fixedrange=True),
            xaxis=dict(tickangle=0, automargin=True, dtick=x_axis_dtick, tickformat='%H시<br>%m-%d',
                       hoverformat='%H:%M<br>%y-%m-%d'),
            hovermode='x unified', showlegend=False,
        )

            
    # 운동 부분 데이터 업데이트 확인 후 적용
    def plot_exercise(self, fig, user_uid: int, sdate: datetime, edate: datetime, mode: str):
        """
        운동 데이터를 시각화하는 함수.

        Args:
            fig: Plotly Figure 객체
            user_uid: 사용자 ID
            sdate: 시작 날짜
            edate: 종료 날짜
            mode: 'all' 또는 'selected'로 동작을 분기
        """
        df = channel_healthcare_session_service.get_exercise_data(user_uid, sdate, edate)

        if df is None or df.empty:
            st.warning("No exercise data available for the selected range.")
            return None

        # 운동 데이터 필터링
        df = df[['start_time', 'end_time']]
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])

        if mode == "selected":
            # SESSION_VIZ_START_DATE와 SESSION_VIZ_END_DATE로 필터링
            viz_start_date = get_session_state(SESSION_VIZ_START_DATE)
            viz_end_date = get_session_state(SESSION_VIZ_END_DATE)
            df = df[(df['start_time'] >= viz_start_date) & (df['end_time'] <= viz_end_date)]
        elif mode == "all":
            # 전체 기간의 운동 데이터를 유지
            df = df[(df['start_time'] >= sdate) & (df['end_time'] <= edate)]
        else:
            raise ValueError("Invalid mode. Choose 'all' or 'selected'.")


        if df.empty:
            st.warning(f"No exercise data after filtering for mode: {mode}")
            return None

        # Plotting
        for index, row in df.iterrows():
            ex_start = str(row['start_time'])
            ex_end = str(row['end_time'])
            fig.add_vrect(
                x0=ex_start,
                x1=ex_end,
                fillcolor='rgba(0, 255, 100, 0.5)' if mode == "selected" else 'rgba(0, 255, 100, 0.2)',
                line_width=0.3,
                annotation_position='top left',
                annotation_text="운동" if mode == "selected" else f"운동 ({row['start_time'].strftime('%Y-%m-%d')})"
            )

    def plot_meal(self, fig, user_uid: int, sdate: datetime, edate: datetime, mode: str):
        """
        Meal Plot Function with mode parameter.

        Args:
            fig: Plotly figure object.
            user_uid: User ID for filtering data.
            sdate: Start date for data filtering.
            edate: End date for data filtering.
            mode: 'all' for daily meal zones, 'selected' for specific date range.
        """
        # 데이터를 가져오고 필터링
        df = channel_healthcare_session_service.get_meal_data(user_uid, sdate, edate)

        if df is None or df.empty:
            st.warning("No meal data available for the selected range.")
            return None

        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])

        # mode=all: 일별로 그룹화하여 처리
        if mode == 'all':
            daily_grouped = df.groupby(df['start_time'].dt.date)
            for date, group in daily_grouped:
                for _, row in group.iterrows():
                    start_time_dt = row['start_time']
                    end_time_dt = row['end_time']

                    # 식사 영역 추가
                    fig.add_vrect(
                        x0=start_time_dt,
                        x1=end_time_dt,
                        fillcolor='rgba(255, 0, 0, 0.2)',
                        line_width=0.3,
                    )
        # mode=selected: 기존 로직 유지
        elif mode == 'selected':
            viz_start_date = get_session_state(SESSION_VIZ_START_DATE)
            viz_end_date = get_session_state(SESSION_VIZ_END_DATE)
            df = df[(df['start_time'] >= viz_start_date) & (df['end_time'] <= viz_end_date)]

            if df.empty:
                st.warning("No meal data after filtering by visualization range.")
                return None

            # 필요한 열만 선택
            df = df[['start_time', 'end_time', 'meal_div_code', 'top_bg', 'tir']]

            # 그래프에 데이터를 추가
            for _, row in df.iterrows():
                start_time_dt = row['start_time']
                end_time_dt = row['end_time']
                meal_div_code = str(row['meal_div_code'])

                # 영역 추가
                fig.add_vrect(
                    x0=start_time_dt,
                    x1=end_time_dt,
                    fillcolor='rgba(255, 0, 0, 0.2)',
                    line_width=0.3,
                    annotation_position='bottom left',
                    annotation_text=meal_div_code
                )
        else:
            raise ValueError("Invalid mode. Choose 'all' or 'selected'.")



    def plot_meal_food(self, meal_ids: list):
        cols = st.columns(len(meal_ids))  # meal_ids 개수만큼 컬럼 생성
        for idx, meal_id in enumerate(meal_ids):
            with cols[idx]:
                food_data = channel_healthcare_session_service.get_meal_food_data(meal_id)

                meal_df = pd.DataFrame(food_data, columns=["food_name", "serving_unit"])
                meal_df.insert(0, "meal_id", meal_id)  # meal_id 컬럼 추가
                meal_df['칼로리'] = meal_df['food_name'].apply(lambda x: FOOD_CALORIES_DUMMY.get(x, 0))
                meal_df.columns = ["식사ID", "음식", "용기", "칼로리"]
                total_calories = meal_df['칼로리'].sum()
                st.write(f"### Meal Zone{idx+1}(총 칼로리:{total_calories})")
                st.dataframe(meal_df)


    def plot_meal_zone(self, fig, user_uid: int, sdate: datetime, edate: datetime, mode: str):
        """
        Meal Zone Plot Function with mode parameter.

        Args:
            fig: Plotly figure object.
            user_uid: User ID for filtering data.
            sdate: Start date for data filtering.
            edate: End date for data filtering.
            mode: 'all' for daily meal zones, 'selected' for specific date range.
        """

        df = channel_healthcare_session_service.get_meal_data(user_uid, sdate, edate)
        if df is None or df.empty:
            st.warning("No meal data available for the selected range.")
            return None
        # channel_healthcare_session_service.extract_cgm_for_meal_zones(sdate, edate)
        df = df[['start_time', 'end_time', 'meal_div_code', 'top_bg', 'tir', 'meal_id']]
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])


        # mode=all: Add vrect for each meal zone in daily intervals
        if mode == 'all':
            daily_grouped = df.groupby(df['start_time'].dt.date)  # Group by date
            for date, group in daily_grouped:
                for _, row in group.iterrows():
                    start_time_dt = pd.to_datetime(row['start_time'])
                    meal_zone_time = start_time_dt + timedelta(hours=4)  # 4-hour meal zone

                    # Add vrect only if within the global date range
                    if meal_zone_time <= edate:
                        fig.add_vrect(
                            x0=start_time_dt,
                            x1=meal_zone_time,
                            fillcolor='rgba(255, 0, 0, 0.2)',
                            line_width=0.3,
                        )

        # mode=selected: Plot meal zones in the selected date range
        elif mode == 'selected':
            viz_start_date = get_session_state(SESSION_VIZ_START_DATE)
            viz_end_date = get_session_state(SESSION_VIZ_END_DATE)
            df = df[(df['start_time'] >= viz_start_date) & (df['end_time'] <= viz_end_date)]

            update_session_state(SESSION_MEAL_ID, df['meal_id'].dropna().unique().tolist())

            extract_meal_zone_df = channel_healthcare_session_service.extract_cgm_for_meal_zones(user_uid, sdate, edate, df)
            for _, row in df.iterrows():
                start_time_dt = pd.to_datetime(row['start_time'])
                end_time_dt = pd.to_datetime(row['end_time'])
                meal_zone_time = start_time_dt + timedelta(hours=4)  # 4-hour meal zone

                # Add vrect for the selected date range
                if meal_zone_time.date() <= edate.date():
                    fig.add_vrect(
                        x0=start_time_dt,
                        x1=meal_zone_time,
                        fillcolor='rgba(255, 0, 0, 0.1)',
                        line_width=0.3,
                    )

                    # Add meal info marker
                    fig.add_trace(go.Scatter(
                        x=[start_time_dt],
                        y=[1],  # Fixed Y value
                        mode='markers+text',
                        marker=dict(size=20, color='black', symbol='circle'),
                        text=[
                            f"{row['meal_div_code']}(TIR:{row['tir']}  ID:{row['meal_id']})<br> "
                            f"<br>"
                            f"<br>"
                        ],
                        textposition="top center",
                        hoverinfo='text',
                        name='Meal Info'
                    ))

            for _, row in extract_meal_zone_df.iterrows():
                max_bg_time = pd.to_datetime(row['max_bg_time'])
                min_bg_time = pd.to_datetime(row['min_bg_time'])

                # Max BG marker
                fig.add_trace(go.Scatter(
                    x=[max_bg_time],
                    y=[row['max_bg']],
                    mode='markers+text',
                    marker=dict(size=15, color='blue', symbol='circle'),
                    text=[f"Max BG: {row['max_bg']}<br>Time: {max_bg_time}"],
                    textposition="top center",
                    hoverinfo='text',
                    name=f"Max BG ({row['meal_div_code']})"
                ))

                # Min BG marker
                fig.add_trace(go.Scatter(
                    x=[min_bg_time],
                    y=[row['min_bg']],
                    mode='markers+text',
                    marker=dict(size=15, color='green', symbol='circle'),
                    text=[f"Min BG: {row['min_bg']}<br>Time: {min_bg_time}"],
                    textposition="bottom center",
                    hoverinfo='text',
                    name=f"Min BG ({row['meal_div_code']})"
                ))


        #
        #
        # else:
        #     raise ValueError("Invalid mode. Choose 'all' or 'selected'.")



    def plot_medicine(self, fig, user_uid: int, sdate: datetime):
        '''
        약물의 vrect표현을 end time 생성
        end : start + 1minutes
        '''
        df = channel_healthcare_session_service.get_medicine_data(user_uid, sdate)
        if df is None:
            return None

        # Ensure 'regist_time' is in datetime format
        df['regist_time'] = pd.to_datetime(df['regist_time'])

        # Add a new column 'end_time' by adding 5 minutes to 'regist_time'
        df['end_time'] = df['regist_time'] + pd.Timedelta(minutes=1)

        for index, row in df.iterrows():
            ex_start = row['regist_time']
            ex_end = row['end_time']
            fig.add_vrect(
                x0=ex_start,
                x1=ex_end,
                fillcolor='rgba(255, 255, 100, 0.5)',
                line_width=0.3,
                annotation_position='top left',
                annotation_text="복약"
            )