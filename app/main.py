import streamlit as st

import sys
sys.path.append('.')

import os
from app.layout.dashboard import dashboard_layout
from app.common.common import BACKEND_URL
import requests
import json
# st.set_page_config(
#     page_title="Adventures of KimParkPenguin",
#     page_icon="./image/kimparkpenguin.png",
#     layout="wide",
#     initial_sidebar_state="expanded", #collapsed
#     menu_items={
#         'Get Help': 'https://www.channelbiome.com/',
#         'Report a bug': "https://www.channelbiome.com/",
#         'About': "https://www.channelbiome.com/"
#     }
# )

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, 'style', 'style.css')
    # st.image('image/kimparkpenguin.png', use_column_width='auto')

    # CSS 파일을 읽어들임
    with open(css_path, 'r', encoding='utf-8') as css_file:
        css_code = css_file.read()
    st.markdown(css_code, unsafe_allow_html=True)
    try:
        response = requests.get(f"{BACKEND_URL}/server_sync")
        dashboard_layout.draw_dashboard()
    except Exception as e:
        st.error("☠️ backend server is dead ☠️")


# import sys, os
# sys.path.append('.')
#
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from contextlib import asynccontextmanager
# from backend.api.content import router as content_router
# from backend.api.career import router as career_router
#
# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from app.common.common import BACKEND_HOST
# from backend.db.session import engine
# from backend.models.base import Base
# import streamlit as st
#
#
#
#
# app = FastAPI(title="Portfolio API")
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[f"http://{BACKEND_HOST}:8501"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # 라우터 등록
# app.include_router(content_router, prefix="/api", tags=["content"])
# app.include_router(career_router, prefix="/api", tags=["careers"])  # 태그 추가
#
# # @app.on_event("startup")
# # async def startup():
# #     print("Registered routes:")
# #     for route in app.routes:
# #         print(f"  {route.path} [{route.methods}]")
# #     Base.metadata.create_all(bind=engine)
#

#
# @app.get("/")
# async def root():
#     return {"message": "API is running"}