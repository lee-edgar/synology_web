from app.utils.singleton import singleton
import streamlit as st

@singleton
class ChannelHealthcareInfo:
    def __init__(self):
        pass

    def __(self):
        st.write('st.session_state', st.session_state)

channel_healthcare_info_session: ChannelHealthcareInfo = ChannelHealthcareInfo()