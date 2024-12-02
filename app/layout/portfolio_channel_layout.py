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
    str2datetime_strptim
import plotly.graph_objects as go
import pandas as pd


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

        # 데이터 시각화 및 테이블 생성
        select_date = channel_healthcare_session_service.update_navigatation()
        self.draw_graph(select_date)
        self.draw_sub_graph()
        self.draw_table()


    def draw_graph(self, select_date):
        user_uid = st.session_state['user_uid']

        if select_date is not None:
            sdate, edate = (select_date)
            sdate, edate = (sdate), (edate)

            st.write('select date', sdate,edate)
        else:
            sdate = str2datetime(st.session_state['sdate'])
            edate = str2datetime(st.session_state['edate'])



        fig = go.Figure()

        self.plot_cgm(fig, user_uid, sdate, edate)
        self.plot_exercise(fig, user_uid, sdate, edate)
        self.plot_meal(fig, user_uid, sdate, edate)
        self.plot_medicine(fig, user_uid, sdate)
        st.plotly_chart(fig , use_container_width=True)

    def draw_sub_graph(self):
        user_uid = st.session_state['user_uid']
        sdate = str2datetime(st.session_state['sdate'])
        edate = str2datetime(st.session_state['edate'])


        fig = go.Figure()
        self.plot_cgm(fig, user_uid, sdate, edate)
        # self.plot_exercise(fig, user_uid, sdate, edate)
        self.plot_meal_zone(fig, user_uid, sdate, edate)
        # self.plot_medicine(fig, user_uid, sdate)

        st.plotly_chart(fig, use_container_width=True)


    def draw_table(self):
        mode = st.radio('회원 정보 탭', [item.value for item in TableView],
                        horizontal=True, label_visibility='collapsed')
        st.info(st.session_state.data_call_session)
        if mode == TableView.cgm:
            st.dataframe(channel_healthcare_session_service.get_cgm_data(
                st.session_state['user_uid'],
                str2datetime(st.session_state['sdate']),
                str2datetime(st.session_state['edate']))
            )

        elif mode == TableView.meal:
            st.dataframe(channel_healthcare_session_service.get_meal_data(
                st.session_state['user_uid'],
                str2datetime(st.session_state['sdate']),
                str2datetime(st.session_state['edate']))
            )

        elif mode == TableView.exercise:
            st.dataframe(channel_healthcare_session_service.get_exercise_data(
                st.session_state['user_uid'],
                str2datetime(st.session_state['sdate']),
                str2datetime(st.session_state['edate']))
            )

        elif mode == TableView.medicine:
            st.dataframe(channel_healthcare_session_service.get_medicine_data(
                st.session_state['user_uid'],
                str2datetime(st.session_state['sdate']))
            )

    def plot_cgm(self, fig, user_uid:int, sdate:datetime, edate:datetime):
        st.write('plot_cgm', sdate, edate)

        all_y_axis_values = []
        max_bg = []

        df = channel_healthcare_session_service.get_cgm_data(user_uid, sdate, edate)
        df['std_time'] = pd.to_datetime(df['std_time'])
        df = df[['std_time', 'bg']]
        if df is None:
            st.warning(MSG_NO_CGM_DATA)
            return None

        df_line_list = channel_healthcare_session_service.split_break_line(df)
        for df_list in df_line_list:
            all_y_axis_values.extend(df_list.bg.tolist())
            fig.add_trace(go.Scatter(x=df_list.std_time, y=df_list.bg,  mode='lines', line=dict(color='blue')))

        y_axis_range = channel_healthcare_session_service.calculate_y_axis_range(all_y_axis_values)
        x_axis_dtick = channel_healthcare_session_service.calculate_x_axis_range(
            pd.to_datetime(st.session_state.sdate),
            pd.to_datetime(st.session_state.edate)
        )


        channel_healthcare_session_service.add_marker(fig, df, column='bg', marker_type='max', color='red', label='Max BG')
        channel_healthcare_session_service.add_marker(fig, df, column='bg', marker_type='min', color='green', label='Min BG')
        channel_healthcare_session_service.add_marker(fig, df, column='bg', marker_type='mean', color='purple', label='Mean BG')

        fig.add_hrect(y0=70, y1=180, fillcolor='yellow', opacity=0.09)
        fig.update_layout(
            title={
                "text": "<span style='font-size: 14px; color: gray'>라벤더 영역 : 식사 데이터, 초록색 영역 : 운동 데이터, 붉은색 영역 : 투약 데이터 </span>",
                "y": 0.95,
                "x": 0.025,
                "xanchor": "left",
                "yanchor": "top"
            },
            yaxis=dict(range=y_axis_range, tickmode='linear', tick0=0, dtick=20, fixedrange=True),
            xaxis=dict(tickangle=0, automargin=True, dtick=x_axis_dtick, tickformat='%H시<br>%m-%d', hoverformat='%H:%M<br>%y-%m-%d'),
            hovermode='x unified', showlegend=False)
        fig.update_layout(yaxis=dict(range=y_axis_range), xaxis=dict(dtick=x_axis_dtick))

    def plot_exercise(self, fig, user_uid:int, sdate:datetime, edate:datetime):
        df = channel_healthcare_session_service.get_exercise_data(user_uid, sdate, edate)

        if df is None:
            return None

        df = df[['start_time', 'end_time']]
        for index, row in df.iterrows():
            ex_start = str(row['start_time'])
            ex_end = str(row['end_time'])
            fig.add_vrect(x0=ex_start, x1=ex_end, fillcolor='rgba(0, 255, 100, 0.5)', line_width=0.3,
                          annotation_position='top left', annotation_text="운동")


    def plot_meal(self, fig, user_uid: int, sdate: datetime, edate: datetime):
        df = channel_healthcare_session_service.get_meal_data(user_uid, sdate, edate)
        df = df[['start_time', 'end_time', 'meal_div_code', 'top_bg', 'tir']]

        if df is None or df.empty:
            return None

        for index, row in df.iterrows():
            start_time_dt = pd.to_datetime(row['start_time'])
            end_time_dt = pd.to_datetime(row['end_time'])
            midpoint = start_time_dt + (end_time_dt - start_time_dt) / 2

            # meal_zone_time이 edate를 초과하면 제외
            if end_time_dt.date() > edate.date():
                continue

            start_time = str(row['start_time'])
            end_time = str(row['end_time'])
            meal_div_code = str(row['meal_div_code'])
            top_bg = str(row['top_bg'])
            tir = str(row['tir'])

            fig.add_vrect(
                x0=start_time,
                x1=end_time,
                fillcolor='rgba(255, 0, 0, 0.2)',
                line_width=0.3,
                annotation_position='bottom left',
                annotation_text=meal_div_code
            )



    def plot_meal_zone(self, fig, user_uid: int, sdate: datetime, edate: datetime):
        df = channel_healthcare_session_service.get_meal_data(user_uid, sdate, edate)
        df = df[['start_time', 'end_time', 'meal_div_code', 'top_bg', 'tir']]

        if df is None or df.empty:
            return None

        for index, row in df.iterrows():
            start_time_dt = pd.to_datetime(row['start_time'])
            end_time_dt = pd.to_datetime(row['end_time'])
            midpoint = start_time_dt + (end_time_dt - start_time_dt) / 2
            meal_zone_time = start_time_dt + timedelta(hours=4)  # 4시간 더하기

            # meal_zone_time이 edate를 초과하면 제외
            if meal_zone_time.date() > edate.date():
                continue

            start_time = str(row['start_time'])
            end_time = str(row['end_time'])
            meal_div_code = str(row['meal_div_code'])
            top_bg = str(row['top_bg'])
            tir = str(row['tir'])

            fig.add_vrect(
                x0=start_time,
                x1=meal_zone_time,
                fillcolor='rgba(255, 0, 0, 0.2)',
                line_width=0.3,
            )

            fig.add_trace(go.Scatter(
                x=[start_time_dt],  # 중간값에 마커 추가
                y=[1],  # 고정된 Y 값
                mode='markers+text',
                marker=dict(size=20, color='black', symbol='circle'),  # 검은색 마커
                text=[f"{meal_div_code}<br>"
                      f"Start: {start_time}<br>"
                      f"End: {end_time}<br>"
                      f"TOP_BG: {top_bg}<br>"
                      f"TIR: {tir}<br>"],
                textposition="top center",  # 텍스트 위치 설정
                hoverinfo='text',
                name='Meal Info'
            ))


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
