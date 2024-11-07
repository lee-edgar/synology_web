import streamlit as st
import requests
import json
from app.common.common import BACKEND_URL
from app.utils.singleton import  singleton
from app.layout.const import *


class Study:

    def __init__(self):
        pass

    def draw(self):
        st.markdown(f"{STUDYGROUP_VIEW_MARKDOWN}")
        st.markdown(f"{COMMING_SOON}")
        self.draw_study_group_view()

    def draw_study_group_view(self):
        st.image('penguin_mov.gif', use_column_width='auto')
