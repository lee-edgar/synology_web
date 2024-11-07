import streamlit as st
import requests
import json
from app.common.common import BACKEND_URL
from app.utils.singleton import  singleton
from app.layout.const import *


class Portfolio:

    def __init__(self):
        pass

    def draw(self):
        st.markdown(f"{PORTFOLIO_VIEW_MARKDOWN}")
        self.draw_portfolio_group_view()

    def draw_portfolio_group_view(self):
        st.image('penguin_mov.gif', use_column_width='auto')

