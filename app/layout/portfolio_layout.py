import streamlit as st
import requests
import json
from app.common.common import BACKEND_URL
from app.utils.singleton import  singleton
from app.layout.const import *
from streamlit_pdf_viewer import pdf_viewer
from app.layout.portfolio_channel_layout import Portfolio_Channel_Layout


class Portfolio:

    def __init__(self):
        self.portfolio_channel_layout = Portfolio_Channel_Layout()


    def navigation(self):
        # col1, col2, col3 = st.columns([2, 8, 1])  # 8:2:1 비율
        st.markdown(f"{PORTFOLIO_VIEW_MARKDOWN}")

        if st.query_params["submenu"] == CHANNEL_HEALTHCARE_MARKDOWN :
            self.portfolio_channel_layout.draw()
        else:
            self.draw_portfolio_group_view()




        # st.markdown('PortfolioGroup', PortfolioGroup.retinal_oct_disease_classification)
    def draw_portfolio_group_view(self):
        st.image('penguin_mov.gif', use_column_width='auto')

        pdf_path = '버섯분류프로젝트.pdf'
        pdf_viewer(
            pdf_path,
            width=1000,
            height=1000,
            render_text=True,
            pages_vertical_spacing=2,
            scroll_to_page=3,
            annotation_outline_size=2
        )
