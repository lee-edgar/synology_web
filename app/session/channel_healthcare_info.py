from app.utils.singleton import singleton
import streamlit as st
from app.utils.data_agent import DataAgent, data_agent


@singleton
class ChannelHealthcareInfo:
    def __init__(self):
        pass

    def get_cgm_date(self, user_uid, sdate, edate):
        # st.write('st.session_state', st.session_state)
        data_agent.get_cgm(user_uid, sdate, edate)
        pass


channel_healthcare_info_session: ChannelHealthcareInfo = ChannelHealthcareInfo()