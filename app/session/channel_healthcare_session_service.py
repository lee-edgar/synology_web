import pandas as pd

from app.utils.singleton import singleton
import streamlit as st
from app.utils.data_agent import DataAgent, data_agent
from datetime import datetime, date
import plotly.graph_objects as go
from app.layout.const import *
from datetime import date, datetime, timedelta
from app.utils.streamlit_utils import (get_session_state, update_session_state, initialize_session_state, str2datetime,
                                       str2datetime_strptim, format_date_range)


@singleton
class ChannelHealthcareSessionService:
    def __init__(self):
        pass

    def request_data(self, user_uid, sdate, edate):
        self.get_cgm_data(user_uid, sdate, edate)
        self.get_meal_data(user_uid, sdate, edate)
        self.get_exercise_data(user_uid, sdate, edate)
        self.get_medicine_data(user_uid, sdate)

    def get_cgm_data(self, user_uid: int, sdate: date, edate:date):
        cgm_info = data_agent.get_cgm(user_uid, sdate, edate)
        if cgm_info is None:
            return None

        return pd.DataFrame(cgm_info)

    def get_exercise_data(self, user_uid: int, sdate: date, edate:date):
        exercise_info = data_agent.get_exercise(user_uid, sdate, edate)
        if exercise_info is None:
            return None
        return pd.DataFrame(exercise_info)

    def get_meal_data(self, user_uid: int, sdate: date, edate: date):
        meal_info = data_agent.get_meal(user_uid, sdate, edate)
        if meal_info is None:
            return None
        return pd.DataFrame(meal_info)

    def get_medicine_data(self, user_uid: int, sdate: date):
        medicine_info = data_agent.get_medicine(user_uid, sdate)

        if medicine_info is None:
            return None

        df = pd.DataFrame(data_agent.get_medicine(user_uid, sdate))
        # st.session_state에서 날짜 가져오기
        session_sdate, session_edate = pd.to_datetime(st.session_state.sdate), pd.to_datetime(st.session_state.edate)
        # regist_time 필터링
        df['regist_time'] = pd.to_datetime(df['regist_time'])  # datetime 형식으로 변환
        filtered_df = df[(df['regist_time'] >= session_sdate) & (df['regist_time'] <= session_edate)]

        return filtered_df

    def add_marker(self, fig, df, column: str, marker_type: str, color: str, label: str, mode: str):
        """
        최대값 또는 평균값을 그래프에 추가하는 함수.

        Args:
            fig: Plotly Figure 객체
            df (pd.DataFrame): 데이터프레임 (시간 및 값 포함)
            column (str): 값을 찾을 열 이름
            marker_type (str): 'max' 또는 'mean' (최대값 또는 평균값)
            color (str): 마커 또는 선의 색상
            label (str): 그래프에 표시할 라벨 ('Max BG' 또는 'Mean BG')
            mode (str): 'all' 또는 'selected' - all인 경우 일별로 최대값 표시
        """
        if marker_type == 'max':
            if mode == "all":
                # 일별 최대값 계산
                df['date'] = df['std_time'].dt.date  # 날짜만 추출
                daily_max = df.groupby('date')[column].max().reset_index()

                # 일별 최대값을 그래프에 추가
                for _, row in daily_max.iterrows():
                    date = row['date']
                    value = row[column]
                    time = df[(df['date'] == date) & (df[column] == value)]['std_time'].iloc[0]  # 해당 값의 시간

                    fig.add_trace(go.Scatter(
                        x=[time],
                        y=[value],
                        mode='markers+text',
                        marker=dict(color=color, size=10),
                        text=[f"{label}: ({time.strftime('%H:%M')}, {value})"],
                        textposition="middle right",
                        name=f"{label} ({date})"
                    ))
            elif mode == "selected":
                # 선택된 기간 내 최대값
                value = df[column].max()
                row = df[df[column] == value].iloc[0]
                time = row['std_time']

                fig.add_trace(go.Scatter(
                    x=[time],
                    y=[value],
                    mode='markers+text',
                    marker=dict(color=color, size=10),
                    text=[f"Daily {label}: ({time.strftime('%H:%M')}, {value})"],
                    textposition="middle right",
                    name=label
                ))

        elif marker_type == 'min' and mode == "selected":
            # 선택된 기간 내 최소값 (mode="selected"일 때만 표시)
            value = df[column].min()
            row = df[df[column] == value].iloc[0]
            time = row['std_time']

            fig.add_trace(go.Scatter(
                x=[time],
                y=[value],
                mode='markers+text',
                marker=dict(color=color, size=10),
                text=[f"Daily {label}: ({time.strftime('%H:%M')}, {value})"],
                textposition="middle right",
                name=label
            ))

        elif marker_type == 'mean':
            # 평균값 수평선 추가
            value = df[column].mean()
            fig.add_hline(
                y=value,
                line=dict(color=color, dash='dash', width=2),
                annotation_text=f"{label}: {value:.2f}",
                annotation_position="top left"
            )
        else:
            if mode == "all" and marker_type == 'min':
                # mode='all'일 때는 최저혈당을 무시합니다.
                return
            raise ValueError("marker_type must be 'max', 'min', or 'mean'")

    def split_break_line(self, df: pd.DataFrame):
        # 30분 기준으로 데이터가 시각적으로 연속된 구간과 끊어진 구간을 구분할 수 있음.
        # 연속적인 구간과 비연속적인 구간을 강제로 잇게하면 신뢰성이 떨어지고, 라인 퀄리티가 떨어질 가능성이 있음.

        df_line_list = []  # 분리된 구간 리스트
        line_list = []  # 현재 구간 저장 리스트

        if df.empty:
            st.warning("빈 데이터프레임입니다.")
            return df_line_list

        # 시간 차이 계산
        df['diff'] = df['std_time'].diff()  # 시간 차이 추가

        for index, row in df.iterrows():
            # 첫 번째 행 처리
            if pd.isna(row['diff']):
                if line_list:  # 이전 구간이 있으면 저장
                    df_line_list.append(pd.DataFrame(line_list))
                line_list = []  # 새로운 리스트 초기화
                line_list.append(row)
            # 시간 차이가 30분 이상인 경우
            elif row['diff'] > pd.Timedelta(minutes=20):
                df_line_list.append(pd.DataFrame(line_list))  # 현재 구간 저장
                line_list = [row]  # 새 구간 시작
            else:
                line_list.append(row)  # 현재 구간에 추가

        # 마지막 구간 저장
        if line_list:
            df_line_list.append(pd.DataFrame(line_list))

        return df_line_list

    def calculate_y_axis_range(self, all_y_axis_values: list, mode: str):
        """
        Y축 범위를 계산합니다.

        Args:
            all_y_axis_values (list): Y축 데이터 값 리스트.
            mode (str): 그래프 모드 ("all" 또는 "selected").

        Returns:
            list: Y축 범위 [min_y, max_y].
        """
        if all_y_axis_values:
            min_y, max_y = min(all_y_axis_values), max(all_y_axis_values)

            # 모드가 'all'인 경우 50단위로 범위를 계산
            if mode == "all":
                min_y = (min_y // 50) * 50  # 최소값을 50단위로 내림
                max_y = ((max_y // 50) + 1) * 50  # 최대값을 50단위로 올림
                return [min_y, max_y]

            # 기본 혈당 범위 내에서 처리
            if 60 < min_y < 240 and 60 < max_y < 240:
                return [60, 240]
            else:
                # 최대 혈당이 420 이상인 경우 상한선을 480으로 설정
                max_limit = 480 if max_y > 420 else 350
                return [min(60, min_y - 20), max(max_limit, max_y + 20)]
        else:
            return [60, 240]


    def calculate_x_axis_range(self, sdate: datetime, edate: datetime, mode: str ) -> int:
        """
        X축의 dtick 값을 계산합니다.

        Args:
            sdate (datetime): 시작 날짜
            edate (datetime): 종료 날짜
            mode (str): "selected" (기존 방식) 또는 "all" (전체 데이터용)

        Returns:
            int: dtick 값 (밀리초 단위)
        """
        days_diff = (edate - sdate).days  # edate - sdate로 변경 (양수로 계산)

        if mode == "all":
            # 전체 데이터의 경우 더 긴 기간을 가정하여 dtick 값 계산
            if days_diff <= 7:
                dtick_value = 43200 * 1000  # 12시간 간격
            else:
                dtick_value = 86400 * 1000  # 1일 간격
        elif mode == "selected":
            # 기존 로직 (선택된 데이터 범위 기준)
            for day_limit in sorted(X_AXIS_DTICK_VALUES.keys(), reverse=True):
                if days_diff <= day_limit:
                    dtick_value = X_AXIS_DTICK_VALUES[day_limit]
                    break
            else:
                dtick_value = X_AXIS_DTICK_VALUES[max(X_AXIS_DTICK_VALUES.keys())]  # 최대 범위 기본값
        else:
            raise ValueError("Invalid mode. Choose 'selected' or 'all'.")

        return dtick_value

    def extract_cgm_for_meal_zones(self, user_uid, sdate, edate, meal_zone_df):

        # cgm 데이터 가져오기
        cgm_df = self.get_cgm_data(user_uid, sdate, edate)

        # std_time 열을 datetime 형식으로 변환
        cgm_df['std_time'] = pd.to_datetime(cgm_df['std_time'])

        # meal_zone_df의 start_time 및 end_time도 datetime 형식으로 변환
        meal_zone_df['start_time'] = pd.to_datetime(meal_zone_df['start_time'])
        meal_zone_df['end_time'] = pd.to_datetime(meal_zone_df['start_time']) + timedelta(hours=4)

        # 결과 저장을 위한 리스트
        results = []

        # meal_zone_df의 각 행에 대해 반복
        for _, row in meal_zone_df.iterrows():
            # 현재 meal zone에 해당하는 cgm 데이터 필터링
            filtered = cgm_df[(cgm_df['std_time'] >= row['start_time']) & (cgm_df['std_time'] <= row['end_time'])]

            if not filtered.empty:
                # max 및 min 값과 해당 시간 추출
                max_bg = filtered['bg'].max()
                max_bg_time = filtered.loc[filtered['bg'].idxmax(), 'std_time']
                min_bg = filtered['bg'].min()
                min_bg_time = filtered.loc[filtered['bg'].idxmin(), 'std_time']
            else:
                max_bg = min_bg = max_bg_time = min_bg_time = None

            # 결과 저장
            results.append({
                'meal_div_code': row['meal_div_code'],
                'start_time': row['start_time'],
                'end_time': row['end_time'],
                'max_bg': max_bg,
                'max_bg_time': max_bg_time,
                'min_bg': min_bg,
                'min_bg_time': min_bg_time
            })

        # 결과를 DataFrame으로 변환
        results_df = pd.DataFrame(results)

        return results_df

    # 리펙토링
    def get_filtered_meal_zones(self,user_uid, sdate, edate, mode, cgm_df):
        """
        Filter meal zone data based on the selected mode.
        """
        meal_data = self.get_meal_data(self, user_uid, sdate, edate)
        if meal_data is None or meal_data.empty:
            return None

        meal_data['start_time'] = pd.to_datetime(meal_data['start_time'])
        meal_data['end_time'] = pd.to_datetime(meal_data['end_time'])

        if mode == 'selected':
            # 특정 날짜 범위로 필터링
            viz_start_date = get_session_state(SESSION_VIZ_START_DATE)
            viz_end_date = get_session_state(SESSION_VIZ_END_DATE)
            meal_data = meal_data[
                (meal_data['start_time'] >= viz_start_date) & (meal_data['end_time'] <= viz_end_date)
                ]

        if meal_data.empty:
            return None

        # Meal zone에 따른 연속혈당 데이터 추출
        matched_cgm_data = self.extract_cgm_for_meal_zones(meal_data, cgm_df)
        return meal_data, matched_cgm_data




    # 미사용 함수
    # def update_navigatation(self):
    #     __, __, col1, col2, col3 = st.columns((0.5, 1, 1, 1, 1))
    # 
    #     # 현재 viz_start_date와 viz_end_date를 세션에서 가져오기
    #     viz_start_date = get_session_state(SESSION_VIZ_START_DATE)
    #     viz_end_date = get_session_state(SESSION_VIZ_END_DATE)
    # 
    #     # "이전" 버튼 클릭 시 처리
    #     with col1:
    #         if st.button(":arrow_backward: 이전", use_container_width=True):
    #             # 날짜를 하루 전으로 이동
    #             viz_start_date -= timedelta(days=1)
    #             viz_end_date -= timedelta(days=1)
    # 
    #             # 변경된 날짜를 세션 상태에 업데이트
    #             update_session_state(SESSION_VIZ_START_DATE, viz_start_date)
    #             update_session_state(SESSION_VIZ_END_DATE, viz_end_date)
    # 
    #     # "다음" 버튼 클릭 시 처리
    #     with col3:
    #         if st.button("다음 :arrow_forward:", use_container_width=True):
    #             # 날짜를 하루 후로 이동
    #             viz_start_date += timedelta(days=1)
    #             viz_end_date += timedelta(days=1)
    # 
    #             # 변경된 날짜를 세션 상태에 업데이트
    #             update_session_state(SESSION_VIZ_START_DATE, viz_start_date)
    #             update_session_state(SESSION_VIZ_END_DATE, viz_end_date)
    # 
    #     # 현재 날짜 출력
    #     with col2:
    #         st.date_input('날짜 선택',
    #                       (viz_start_date, viz_end_date),
    #                       label_visibility='collapsed')



channel_healthcare_session_service: ChannelHealthcareSessionService = ChannelHealthcareSessionService()