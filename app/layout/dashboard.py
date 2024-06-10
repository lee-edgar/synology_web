import streamlit as st
import time
from datetime import datetime, timedelta

import os
from app.utils.singleton import singleton
from app.layout.const import *
from st_on_hover_tabs import on_hover_tabs


@singleton
class DashLayout:
    def __init__(self):
        pass

    def draw_dashboard(self):
        stime = time.time()
        self.draw_sidebar()
        etime = time.time()
        st.markdown(f'### Update Time = {timedelta(seconds=etime - stime)}')

    def draw_sidebar(self):
        st.header("Custom tab component for on-hover navigation bar")

        with st.sidebar:
            options = list(Menu)
            tabs = on_hover_tabs(tabName=[menu.value for menu in options],
                                 iconName=['house', 'upload', 'list'],
                                 default_choice=0, styles={'navtab': {'background-color': '#f2f2f2',
                                                                      'color': '#818181',
                                                                      'font-size': '18px',
                                                                      'transition': '.3s',
                                                                      'white-space': 'nowrap',
                                                                      'text-transform': 'uppercase'},
                                                           'tabOptionsStyle': {':hover :hover': {'color': 'red',
                                                                                                 'cursor': 'pointer'}},
                                                           'iconStyle': {'position': 'fixed',
                                                                         'left': '7.5px',
                                                                         'text-align': 'left'},
                                                           'tabStyle': {'list-style-type': 'none',
                                                                        'margin-bottom': '30px',
                                                                        'padding-left': '30px',
                                                                        'padding-right': '30px'}})



dashboard_layout: DashLayout = DashLayout()
