import pandas as pd

from app.utils.singleton import singleton
import streamlit as st
from app.utils.data_agent import DataAgent, data_agent


@singleton
class ChannelHealthcareInfo:
    def __init__(self):
        pass

    def get_cgm_date(self, user_uid, sdate, edate):
        cgm_info = data_agent.get_cgm(user_uid, sdate, edate)
        st.write('session info', cgm_info)
        df = pd.DataFrame(cgm_info)
        st.write(df)
channel_healthcare_info_session: ChannelHealthcareInfo = ChannelHealthcareInfo()