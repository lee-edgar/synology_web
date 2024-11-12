import streamlit as st
import requests
import json
from app.common.common import BACKEND_URL
from app.utils.singleton import  singleton
from app.layout.const import *
from streamlit_pdf_viewer import pdf_viewer


class Portfolio_Channel_Layout():
    def __init__(self):
        pass

    def draw(self):
        st.markdown(f"{CHANNEL_HEALTHCARE_MARKDOWN}")
