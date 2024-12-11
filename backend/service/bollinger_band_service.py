import pandas as pd

class Bollinger:
    def __init__(self):
        pass
#
    def calculate_bollinger_bands(self, cgm_data: list, window: int = 20, num_std_dev: int = 2):
        """
        볼린저 밴드 계산
        Args:
            cgm_data (list): 연속혈당 데이터 리스트 (dict 형태로 std_time, value 포함).
            window (int): 이동 평균을 계산할 윈도우 크기 (기본값: 20).
            num_std_dev (int): 표준편차 계수 (기본값: 2).

        Returns:
            list: 각 데이터에 대해 upper_band, lower_band, moving_avg 추가된 dict 리스트.
        """
        if not cgm_data:
            raise ValueError("CGM data is empty")

        # 데이터를 DataFrame으로 변환
        df = pd.DataFrame(cgm_data)

        # 값이 없으면 에러 처리
        if 'value' not in df.columns or 'std_time' not in df.columns:
            raise ValueError("CGM data must contain 'std_time' and 'value' fields")

        # 시간 정렬 및 이동 평균 계산
        df['std_time'] = pd.to_datetime(df['std_time'])
        df = df.sort_values(by='std_time')
        df['moving_avg'] = df['value'].rolling(window=window).mean()
        df['moving_std'] = df['value'].rolling(window=window).std()

        # 볼린저 밴드 계산
        df['upper_band'] = df['moving_avg'] + (num_std_dev * df['moving_std'])
        df['lower_band'] = df['moving_avg'] - (num_std_dev * df['moving_std'])

        # 필요한 열만 반환
        return df[['std_time', 'value', 'moving_avg', 'upper_band', 'lower_band']].to_dict(orient='records')
#
#     @staticmethod
#     def calculate_overall_bollinger_stats(bollinger_data: list):
#         """
#         전체 볼린저 밴드 통계를 계산
#         Args:
#             bollinger_data (list): 볼린저 밴드가 포함된 데이터 리스트
#
#         Returns:
#             dict: 상한, 하한, 평균값에 대한 통계
#         """
#         df = pd.DataFrame(bollinger_data)
#
#         overall_stats = {
#             "overall_upper_band": df['upper_band'].mean(),
#             "overall_lower_band": df['lower_band'].mean(),
#             "overall_moving_avg": df['moving_avg'].mean()
#         }
#
#         return overall_stats
#
bollinger:Bollinger = Bollinger()
