import pandas as pd

from app.utils.singleton import singleton
import streamlit as st
from app.utils.data_agent import DataAgent, data_agent
from datetime import datetime, date
import plotly.graph_objects as go
from app.layout.const import *
from datetime import date, datetime, timedelta
from app.utils.streamlit_utils import get_session_state, update_session_state, initialize_session_state, str2datetime, str2datetime_strptim


@singleton
class ChannelHealthcareSessionService:
    def __init__(self):
        pass

    def request_data(self, user_uid, sdate, edate):
        st.success('success request for data')
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

    def split_break_line(self, df: pd.DataFrame):
        """
        데이터프레임의 std_time을 기준으로 20분 이상 차이가 나는 구간별로 분리.
        """
        df_line_list = []
        line_list = []

        # 데이터프레임이 비어 있는지 확인
        if df.empty:
            st.warning("빈 데이터프레임입니다.")
            return df_line_list

        # 시간 차이 계산
        try:
            diff = df.std_time.diff()
            if diff.empty or len(diff) != len(df):
                st.warning("시간 차이를 계산할 수 없습니다.")
                return df_line_list
        except Exception as e:
            st.error(f"시간 차이 계산 중 오류: {e}")
            return df_line_list

        # 구간별 분리
        for index, row in df.iterrows():
            # 유효한 인덱스인지 확인
            if index >= len(diff):
                break

            # 첫 번째 행 처리
            if pd.isna(diff.iloc[index]):
                line_list = []  # 새로운 리스트 초기화
                line_list.append(row)
            # 간격이 20분 이상인 경우
            elif diff.iloc[index] > pd.Timedelta(minutes=20):
                if line_list:  # 기존 리스트가 비어있지 않으면 추가
                    df_split = pd.DataFrame(line_list)
                    df_line_list.append(df_split)
                line_list = []  # 새로운 리스트 초기화
                line_list.append(row)
            # 그 외 경우
            else:
                line_list.append(row)

        # 마지막 리스트 추가
        if line_list:
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

    def update_navigatation(self):
        col_period_caption, col_period, col1, col2, col3 = st.columns((0.5, 1, 1, 1, 1))
        with col_period_caption:
            st.write('연속혈당계 사용 시기')

        with col1:
            click = st.button(':arrow_backward: 이전', use_container_width=True)
            if click:
                sdate = str2datetime(st.session_state['sdate'])  + timedelta(days=-1)
                edate = str2datetime(st.session_state['edate'])  + timedelta(days=-1)

                st.session_state['sdate'] = sdate
                st.session_state['edate'] = edate


                return sdate, edate

        with col3:
            click = st.button('다음 :arrow_forward:', use_container_width=True)
            if click:
                sdate = str2datetime(st.session_state['sdate']) + timedelta(days=+1)
                edate = str2datetime(st.session_state['edate']) + timedelta(days=+1)

                st.session_state['sdate'] = sdate
                st.session_state['edate'] = edate
                return sdate, edate


channel_healthcare_session_service: ChannelHealthcareSessionService = ChannelHealthcareSessionService()