import streamlit as st

import sys
sys.path.append('.')

import os
from app.layout.dashboard import dashboard_layout

st.set_page_config(
    page_title="Adventures of KimParkPenguin",
    page_icon="./image/kimparkpenguin.png",
    layout="wide",
    initial_sidebar_state="expanded", #collapsed
    menu_items={
        'Get Help': 'https://www.channelbiome.com/',
        'Report a bug': "https://www.channelbiome.com/",
        'About': "https://www.channelbiome.com/"
    }
)

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, 'style', 'style.css')
    # st.image('image/kimparkpenguin.png', use_column_width='auto')

    # CSS 파일을 읽어들임
    with open(css_path, 'r', encoding='utf-8') as css_file:
        css_code = css_file.read()
    st.markdown(css_code, unsafe_allow_html=True)

    dashboard_layout.draw_dashboard()