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
        # self.portfolio_channel_layout = Portfolio_Channel_Layout()

        pass

    def draw(self):
        st.markdown(f"{PORTFOLIO_VIEW_MARKDOWN}")

        self.draw_portfolio_group_view()




        # st.markdown('PortfolioGroup', PortfolioGroup.retinal_oct_disease_classification)
    def draw_portfolio_group_view(self):
        # st.image('penguin_mov.gif', use_column_width='auto')
        with st.expander(" 버섯분류프로젝트 ", expanded=True):
            pdf_path = '버섯분류프로젝트.pdf'
            pdf_viewer(
                pdf_path,
                width=1300,
                height=1000,
                render_text=True,
                pages_vertical_spacing=1,
                scroll_to_page=3,
                annotation_outline_size=2
            )
        with st.expander(" OCT를 활용한 질병 분류", expanded=True):
            pdf_path = 'DL_project.pdf'
            pdf_viewer(
                pdf_path,
                width=1300,
                height=1000,
                render_text=True,
                pages_vertical_spacing=1,
                scroll_to_page=3,
                annotation_outline_size=2
            )
        with st.expander('channel healthcare', expanded=True):
            self.portfolio_layout.draw()
