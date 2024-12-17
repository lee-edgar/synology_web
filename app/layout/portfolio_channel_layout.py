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

        st.markdown(f"{CHANNEL_HEALTHCARE_MARKDOWN}")


        # channel_healthcare_session_service.draw_user_navigation()
        self.draw_user_info()

        user_uid = get_session_state(SESSION_USER_UID)
        viz_start_date = get_session_state(SESSION_VIZ_START_DATE)
        viz_end_date = get_session_state(SESSION_VIZ_END_DATE)
        load_start_date = get_session_state(SESSION_LOAD_START_DATE)
        load_end_date= get_session_state(SESSION_LOAD_END_DATE)

        self.draw_bollinger_bend_graph(user_uid, load_start_date, load_end_date)
        self.draw_allday_graph(user_uid, load_start_date, load_end_date )
        self.draw_graph(user_uid, viz_start_date, viz_end_date)
        self.draw_sub_graph(user_uid, viz_start_date, viz_end_date)
        self.draw_table(user_uid, viz_start_date, viz_end_date)

    def draw_user_info(self):

        col1, col2, col3, col4, col5 = st.columns((1, 1, 1, 1, 1))
        error_message = None

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
            self.bollinger_band(fig, user_uid, channel_healthcare_session_service.get_cgm_data(user_uid, sdate, edate),
                                std_multiplier, window, smoothing_window, show_moving_avg, band_range, sdate, edate, 'all')
            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=500)
            st.plotly_chart(fig, use_container_width=True)


        with col3:
            st.info(""" 
                        1. 기존 CGM 그래프는 TIR 범위를 80~180 mg/dL로 제한하여, 혈당이 높은 환자에게 적절한 정보를 제공하지 못할 수 있습니다.
                        볼린저 밴드는 혈당 데이터를 감싸는 안전 울타리와 같아, 환자별 혈당 패턴에 맞춘 개인화된 TIR 범위를 제공합니다.
                        2. 주황색 영역은 안정적인 혈당 관리 상태를 나타내며, 이를 벗어나면 혈당 스파이크나 저혈당 위험으로 간주할 수 있습니다.
                        초록색 이동 평균선은 전반적인 혈당 추세를 이해하는 가이드로, 환자가 안정적인 혈당 관리를 유지하고 있는지 확인할 수 있습니다.
                        3. 이를 통해 환자는 자신의 데이터를 직관적으로 분석하고 맞춤형 관리 전략을 수립할 수 있으며, 볼린저 밴드는 환자 중심의 분석 도구로서 보다 효과적인 혈당 관리에 기여합니다.
                        """, icon="ℹ️")
            st.info("""
                        표준 편차 배수 (Std Multiplier): 볼린저 밴드의 상한선과 하한선을 결정합니다.
                        값이 작아질수록 밴드가 좁아져 민감하게 반응하며, 커질수록 밴드가 넓어져 변동성을 더 많이 수용합니다.
    
                        이동 평균 윈도우 (Moving Avg Window): 혈당의 전반적인 추세를 계산하는 데 사용됩니다.
                        값이 작아질수록 짧은 기간의 변화를 잘 반영하며, 커질수록 장기적인 추세를 부드럽게 보여줍니다.
    
                        스무싱 윈도우 (Smoothing Window): 이동 평균과 볼린저 밴드를 부드럽게 표시합니다.
                        값이 작아질수록 원본 데이터에 가깝게 표현되며, 커질수록 그래프가 부드럽고 노이즈가 줄어듭니다.
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
                self.bollinger_band(fig, user_uid, channel_healthcare_session_service.get_cgm_data(user_uid, sdate, edate), std_multiplier, window, smoothing_window, show_moving_avg, band_range, sdate, edate, 'all')
            # self.bollinger_band(fig, user_uid, channel_healthcare_session_service.get_cgm_data(user_uid, sdate, edate), std_multiplier, window, smoothing_window, show_moving_avg, band_range)

            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.info("""
                                    Overall Blood Glucose Trends 페이지는 환자의 일상 혈당 데이터를 다각적으로 분석할 수 있도록 다양한 뷰를 제공합니다. 이 그래프에서는 볼린저 밴드, Meal Zone(식사 시간대), 운동 데이터, 일별 최고 혈당 값을 옵셔널하게 선택하여 시각화할 수 있습니다. 이를 통해 환자는 자신의 혈당 변화를 직관적으로 이해하고 맞춤형 혈당 관리 전략을 수립할 수 있습니다.

                                    Meal Zone 개념 : Meal Zone은 식사 시작 시간부터 식사 시작 후 4시간까지의 구간을 나타냅니다. 식사 직후 혈당은 일반적으로 상승하기 시작하여 일정 시간 후 최고점에 도달하고, 이후 혈당이 정상 범위로 회복되는 패턴을 보입니다. 이 4시간 구간은 식사에 따른 혈당 변화를 명확하게 관찰할 수 있는 기준이 됩니다.

                                    Meal Zone과 볼린저 밴드의 활용 : 볼린저 밴드는 식사 시간대 혈당의 변동성을 감싸는 개인화된 안전 영역을 제공합니다. Meal Zone과 볼린저 밴드를 함께 시각화하면 다음과 같은 해석이 가능합니다.
                                    
                                    Meal Zone의 혈당 상승 패턴 : 볼린저 밴드의 상한선(Upper Band)을 초과하는 경우, 식사 후 혈당이 과도하게 상승했음을 의미합니다. 이는 당뇨 환자나 고혈당 위험군에서 식후 스파이크(Postprandial Spike)로 해석될 수 있으며, 식사량 조절이나 식단 개선이 필요함을 시사합니다.
                                    
                                    Meal Zone 혈당 회복 패턴 : 볼린저 밴드 하한선(Lower Band)으로 내려가거나 지나치게 가까워진다면 저혈당 위험이 있음을 나타낼 수 있습니다. 특히 인슐린이나 약물을 사용하는 환자는 Meal Zone에서 저혈당이 발생하지 않도록 주의해야 합니다.
                                    
                                    다른 Meal Zone과의 비교 : 여러 Meal Zone을 비교하면 특정 시간대에 식사 후 혈당이 지속적으로 높아지는 패턴을 발견할 수 있습니다. 예를 들어, 저녁 식사 시간의 Meal Zone이 다른 시간대보다 자주 볼린저 밴드를 초과한다면, 해당 시간의 식단이나 활동량에 대한 재평가가 필요할 수 있습니다.
                                    
                                    """, icon="ℹ️")




    def draw_graph(self, user_uid, sdate, edate):
        st.markdown('#### Daily Summay')
        fig = go.Figure()
        self.plot_cgm(fig, user_uid, sdate, edate, 'selected')
        self.plot_exercise(fig, user_uid, sdate, edate, 'selected')
        self.plot_meal(fig, user_uid, sdate, edate, 'selected')
        self.plot_medicine(fig, user_uid, sdate)
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10),height=200)  # 마진 최소화

        st.plotly_chart(fig , use_container_width=True)

    def draw_sub_graph(self,  user_uid, sdate, edate):
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
                self.bollinger_band(fig, user_uid,
                                    channel_healthcare_session_service.get_cgm_data(user_uid, sdate, edate),
                                    std_multiplier, window, smoothing_window, show_moving_avg, band_range, sdate, edate, 'selected')

            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10),height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            pass


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

        for date, daily_df in df.groupby('date'):

            if len(daily_df) < window:
                st.warning(f"Insufficient data points for {date}: {len(daily_df)} (required: {window})")
                continue

            daily_df['moving_avg'] = daily_df['bg'].rolling(window=window).mean().fillna(method='bfill')
            daily_df['moving_std'] = daily_df['bg'].rolling(window=window).std().fillna(method='bfill')

            daily_df['upper_band'] = daily_df['moving_avg'] + (std_multiplier * daily_df['moving_std'])
            daily_df['lower_band'] = daily_df['moving_avg'] - (std_multiplier * daily_df['moving_std'])

            daily_dataframes.append(daily_df)

        all_daily_data = pd.concat(daily_dataframes)

        all_daily_data['bg_smooth'] = all_daily_data['bg'].rolling(window=smoothing_window).mean()
        all_daily_data['upper_band_smooth'] = all_daily_data['upper_band'].rolling(window=smoothing_window).mean()
        all_daily_data['lower_band_smooth'] = all_daily_data['lower_band'].rolling(window=smoothing_window).mean()
        all_daily_data['moving_avg_smooth'] = all_daily_data['moving_avg'].rolling(window=smoothing_window).mean()

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

    # 리펙토링 원본
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

        df = df[['start_time', 'end_time', 'meal_div_code', 'top_bg', 'tir']]
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
                            f"{row['meal_div_code']}(TIR: {row['tir']})<br> "
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
