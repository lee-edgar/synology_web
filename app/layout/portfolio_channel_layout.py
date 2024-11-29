import streamlit as st
import requests
import json
from app.common.common import BACKEND_URL
from app.utils.singleton import  singleton
from app.layout.const import *
from streamlit_pdf_viewer import pdf_viewer
from datetime import date, datetime, timedelta
from app.session.channel_healthcare_info import channel_healthcare_info_session
from app.utils.streamlit_utils import get_session_state, update_session_state, initialize_session_state, str2datetime
import plotly.graph_objects as go
import pandas as pd


class Portfolio_Channel_Layout():
    def __init__(self):
        pass

    def initialize_session_render(self):
        '''
        초기 세션 상태 설정:
        기본 세션 정보를 DEFAULT_SESSION_STATE 값으로 초기화함.
        세션 변경이 필요한 경우, 자식함수에서 변경할 수 있음.
        '''
        st.markdown(f"{CHANNEL_HEALTHCARE_MARKDOWN}")

        initialize_session_state(DEFAULT_SESSION_STATE)

        self.draw_graph()
        self.draw_sub_graph()
        self.draw_table()

    def draw_graph(self):
        user_uid = st.session_state['user_uid']
        sdate = str2datetime(st.session_state['sdate'])
        edate = str2datetime(st.session_state['edate'])


        # self.get_cgm(user_uid, sdate, edate)
        # self.get_exercise(user_uid, sdate, edate)
        # self.get_meal(user_uid, sdate, edate)

        # self.get_medicine(user_uid, sdate)

        fig = go.Figure()
        self.plot_cgm(fig, user_uid, sdate, edate)
        self.plot_exercise(fig, user_uid, sdate, edate)
        self.plot_meal(fig, user_uid, sdate, edate)

        st.plotly_chart(fig , use_container_width=True)

    def draw_sub_graph(self):
        user_uid = st.session_state['user_uid']
        sdate = str2datetime(st.session_state['sdate'])
        edate = str2datetime(st.session_state['edate'])

        # self.get_cgm(user_uid, sdate, edate)
        # self.get_exercise(user_uid, sdate, edate)
        # self.get_meal(user_uid, sdate, edate)
        # self.get_medicine(user_uid, sdate)

        fig = go.Figure()
        self.plot_cgm(fig, user_uid, sdate, edate)
        self.plot_exercise(fig, user_uid, sdate, edate)
        self.plot_meal_zone(fig, user_uid, sdate, edate)

        st.plotly_chart(fig, use_container_width=True)


    def draw_table(self):
        mode = st.radio('회원 정보 탭', [item.value for item in TableView],
                        horizontal=True, label_visibility='collapsed')
        st.info(st.session_state.data_call_session)
        if mode == TableView.cgm:
            st.dataframe(self.get_cgm(st.session_state['user_uid'],  str2datetime(st.session_state['sdate']), str2datetime(st.session_state['edate'])))

        elif mode == TableView.meal:
            st.dataframe(self.get_meal(st.session_state['user_uid'], str2datetime(st.session_state['sdate']), str2datetime(st.session_state['edate'])))

        elif mode == TableView.exercise:
            get_exercise = self.get_exercise(st.session_state['user_uid'],
                              str2datetime(st.session_state['sdate']),
                              str2datetime(st.session_state['edate']))
            if get_exercise is None:
                return None
            st.dataframe(get_exercise)

        elif mode == TableView.medicine:
            st.dataframe(self.get_medicine(st.session_state['user_uid'],  str2datetime(st.session_state['sdate'])))

    def plot_cgm(self, fig, user_uid:int, sdate:datetime, edate:datetime):
        all_y_axis_values = []
        max_bg = []

        df = self.get_cgm(user_uid, sdate, edate)
        df['std_time'] = pd.to_datetime(df['std_time'])
        df = df[['std_time', 'bg']]
        if df is None:
            st.warning(MSG_NO_CGM_DATA)
            return None

        df_line_list = self.split_break_line(df)
        for df_list in df_line_list:
            all_y_axis_values.extend(df_list.bg.tolist())
            fig.add_trace(go.Scatter(x=df_list.std_time, y=df_list.bg,  mode='lines', line=dict(color='blue')))

        y_axis_range = self.calculate_y_axis_range(all_y_axis_values)
        x_axis_dtick = self.calculate_x_axis_range(pd.to_datetime(st.session_state.sdate), pd.to_datetime(st.session_state.edate))


        self.add_marker(fig, df, column='bg', marker_type='max', color='red', label='Max BG')
        self.add_marker(fig, df, column='bg', marker_type='min', color='green', label='Min BG')
        self.add_marker(fig, df, column='bg', marker_type='mean', color='purple', label='Mean BG')

        fig.add_hrect(y0=70, y1=180, fillcolor='yellow', opacity=0.09)
        fig.update_layout(
            title={ "text": "<span style='font-size: 14px; color: gray'>라벤더 영역 : 식사 데이터, 초록색 영역 : 운동 데이터, 붉은색 영역 : 투약 데이터 </span>",
                "y": 0.95, "x": 0.025, "xanchor": "left", "yanchor": "top"},
            yaxis=dict(range=y_axis_range, tickmode='linear', tick0=0, dtick=20, fixedrange=True),
            xaxis=dict(tickangle=0, automargin=True, dtick=x_axis_dtick, tickformat='%H시<br>%m-%d', hoverformat='%H:%M<br>%y-%m-%d'),
            hovermode='x unified', showlegend=False)
        fig.update_layout(yaxis=dict(range=y_axis_range), xaxis=dict(dtick=x_axis_dtick))

    def plot_exercise(self, fig, user_uid:int, sdate:datetime, edate:datetime):
        df = self.get_exercise(user_uid, sdate, edate)

        if df is None:
            return None

        df = df[['start_time', 'end_time']]
        for index, row in df.iterrows():
            ex_start = str(row['start_time'])
            ex_end = str(row['end_time'])
            fig.add_vrect(x0=ex_start, x1=ex_end, fillcolor='rgba(0, 255, 100, 0.5)', line_width=0.3,
                          annotation_position='top left', annotation_text="운동")


    def plot_meal(self, fig, user_uid: int, sdate: datetime, edate: datetime):
        df = self.get_meal(user_uid, sdate, edate)
        df = df[['start_time', 'end_time', 'meal_div_code', 'top_bg', 'tir']]

        if df is None or df.empty:
            return None

        for index, row in df.iterrows():
            start_time_dt = pd.to_datetime(row['start_time'])
            end_time_dt = pd.to_datetime(row['end_time'])
            midpoint = start_time_dt + (end_time_dt - start_time_dt) / 2
            # meal_zone_time = start_time_dt + timedelta(hours=4)  # 4시간 더하기

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
        df = self.get_meal(user_uid, sdate, edate)
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


    def get_cgm(self, user_uid: int, sdate: date, edate:date):
        return channel_healthcare_info_session.get_cgm_data(user_uid, sdate, edate)

    def get_exercise(self, user_uid: int, sdate: date, edate:date):
        get_exercise_data = channel_healthcare_info_session.get_exercise_data(user_uid, sdate, edate)
        if get_exercise_data is None:
            return None
        return channel_healthcare_info_session.get_exercise_data(user_uid, sdate, edate)

    def get_meal(self, user_uid: int, sdate: date, edate:date):
        return channel_healthcare_info_session.get_meal_data(user_uid, sdate, edate)

    def get_medicine(self, user_uid: int, sdate: date):
        return channel_healthcare_info_session.get_medicine_data(user_uid, sdate)


    def split_break_line(self, df:pd.DataFrame):
        df_line_list = []
        diff = df.std_time.diff()
        for index, row in df.iterrows():
            # 첫째 간격은 무조건 NaT, 서브 리스트 생성 및 초기값 저장
            if pd.isna(diff.iloc[index]):
                line_list = []
                line_list.append(row)
            # 간격이 20분 넘어가면 이전리스트까지 갈무리하고, 서브 리스트 생성 초기값 저장
            elif diff.iloc[index] > pd.Timedelta(minutes=20):
                df_split = pd.DataFrame(line_list)
                df_line_list.append(df_split)
                line_list = []
                line_list.append(row)
            # 그외에는 서브 리스트에 저장
            else:
                line_list.append(row)

        df_split = pd.DataFrame(line_list)
        df_line_list.append(df_split)
        return df_line_list

    def calculate_y_axis_range(self, all_y_axis_values: list):
        """
            Y축 범위를 계산합니다.

            목적:
                - 입력된 Y축 값(all_y_axis_values)의 최소값과 최대값을 기준으로 Y축 범위를 동적으로 설정합니다.
                - 그래프가 기본 범위(60, 240) 내에 있는 경우 해당 범위를 유지합니다.
                - 기본 범위를 벗어나는 값이 있으면 상/하단에 여유를 두어 그래프를 조정합니다.

            동작:
                1. `all_y_axis_values`가 비어 있으면 기본 범위 [60, 240]을 반환합니다.
                2. 최소값과 최대값이 기본 범위(60, 240) 안에 있을 경우 기본 범위를 반환합니다.
                3. 최소값이 기본 범위를 벗어나면 최소값에서 20을 뺀 값을 하한으로 설정합니다.
                4. 최대값이 기본 범위를 벗어나면 최대값에 20을 더한 값을 상한으로 설정합니다.
                5. 상한값은 최대 480까지 설정 가능하며, 최소값은 60 미만으로 내려가지 않도록 제한합니다.
                6. 최대값이 420 이상인 경우 상한값을 480으로 고정합니다.

            Args:
                all_y_axis_values (list): Y축 데이터 값 리스트.

            Returns:
                list: Y축 범위 [min_y, max_y].
            """

        if all_y_axis_values:
            min_y, max_y = min(all_y_axis_values), max(all_y_axis_values)

            # 기본 혈당 범위 내에서 처리
            if 60 < min_y < 240 and 60 < max_y < 240:
                return [60, 240]
            else:
                # 최대 혈당이 420 이상인 경우 상한선을 480으로 설정
                max_limit = 480 if max_y > 420 else 350
                return [min(60, min_y - 20), max(max_limit, max_y + 20)]
        else:
            return [60, 240]

    def calculate_x_axis_range(self, sdate: datetime, edate: datetime) -> int:
        """
        X축의 dtick 값을 계산합니다.

        Args:
            sdate (datetime): 시작 날짜
            edate (datetime): 종료 날짜

        Returns:
            int: dtick 값 (밀리초 단위)
        """
        days_diff = (sdate - edate).days

        for day_limit in sorted(X_AXIS_DTICK_VALUES.keys(), reverse=True):
            if days_diff <= day_limit:
                dtick_value = X_AXIS_DTICK_VALUES[day_limit]

        return dtick_value

    def add_marker(self, fig, df, column: str, marker_type: str, color: str, label: str):
        """
        최대값, 최소값, 또는 평균값을 그래프에 추가하는 함수.

        Args:
            fig: Plotly Figure 객체
            df (pd.DataFrame): 데이터프레임 (시간 및 값 포함)
            column (str): 값을 찾을 열 이름
            marker_type (str): 'max', 'min', 또는 'mean' (최대값, 최소값, 평균값)
            color (str): 마커 또는 선의 색상
            label (str): 그래프에 표시할 라벨 ('Max BG', 'Min BG', 또는 'Mean BG')
        """
        if marker_type == 'max':
            value = df[column].max()
            row = df[df[column] == value].iloc[0]
            time = row['std_time']
            # 최대값 마커 추가
            fig.add_trace(go.Scatter(
                x=[time],
                y=[value],
                mode='markers+text',
                marker=dict(color=color, size=10),
                text=[f"{label}: ({time.strftime('%H:%M')}, {value})"],
                textposition="top center",
                name=label
            ))
        elif marker_type == 'min':
            value = df[column].min()
            row = df[df[column] == value].iloc[0]
            time = row['std_time']
            # 최소값 마커 추가
            fig.add_trace(go.Scatter(
                x=[time],
                y=[value],
                mode='markers+text',
                marker=dict(color=color, size=10),
                text=[f"{label}: ({time.strftime('%H:%M')}, {value})"],
                textposition="top center",
                name=label
            ))
        elif marker_type == 'mean':
            value = df[column].mean()
            # 평균값 수평선 추가
            fig.add_hline(
                y=value,
                line=dict(color=color, dash='dash', width=2),
                annotation_text=f"{label}: {value:.2f}",
                annotation_position="top left"
            )
        else:
            raise ValueError("marker_type must be 'max', 'min', or 'mean'")
