# from fastapi import APIRouter
#
# router = APIRouter()
#
#
# @router.get("/content/{group}/{submenu}")
# async def get_content(group: str, submenu: str):
#     content = {
#         "StudyGroup": {
#             "Kaggle": {
#                 "title": "Kaggle 스터디",
#                 "content": "Kaggle 스터디 내용"
#             },
#             "Paper": {
#                 "title": "논문 리뷰",
#                 "content": "논문 리뷰 내용"
#             },
#             "ML": {
#                 "title": "머신러닝",
#                 "content": "머신러닝 학습 내용"
#             }
#         },
#         "StoryGroup": {
#             "회고": {
#                 "title": "회고록",
#                 "content": "회고 내용"
#             },
#             "그때그때 느끼는 것들": {
#                 "title": "일상 기록",
#                 "content": "일상 기록 내용"
#             }
#         },
#         "ProfileGroup": {
#             "프로필": {
#                 "title": "프로필",
#                 "content": "프로필 내용"
#             }
#         },
#         "PortfolioGroup": {
#             "포트폴리오": {
#                 "title": "포트폴리오",
#                 "content": "포트폴리오 내용"
#             }
#         }
#     }
#
#     return content.get(group, {}).get(submenu, {"error": "Content not found"})

# backend/api/content.py
# backend/api/content.py
from fastapi import APIRouter
import logging
import json
router = APIRouter()


@router.get("/content/{group}/{submenu}")
async def get_content(group: str, submenu: str):
    # 디버깅을 위한 로그
    logging.info(f"Requested - group: {group}, submenu: {submenu}")

    content = {
        # Menu.study_group.value와 매칭
        "StudyGroup": {
            # StudyGroup Enum 값들과 매칭
            "Kaggle": {
                "title": "Kaggle",
                "subtitle": "Kaggle 스터디 내용"
            },
            "Paper": {
                "title": "논문 리뷰",
                "subtitle": "논문 리뷰 내용"
            },
            "ML": {
                "title": "머신러닝",
                "subtitle": "머신러닝 학습 내용"
            },
            "CV": {
                "title": "컴퓨터 비전",
                "subtitle": "CV 학습 내용"
            },
            "Streamlit": {
                "title": "Streamlit",
                "subtitle": "Streamlit 학습 내용"
            },
            "Math": {
                "title": "수학",
                "subtitle": "수학 학습 내용"
            },
            "Coursera": {
                "title": "Coursera",
                "subtitle": "Coursera 학습 내용"
            },
            "LinkCollection": {
                "title": "링크 모음",
                "subtitle": "유용한 링크 모음"
            }
        },
        # Menu.story_group.value와 매칭
        "StoryGroup": {
            # StoryGroup Enum 값들과 매칭
            "회고": {
                "title": "회고록",
                "subtitle": "회고 내용"
            },
            "그때그때느끼는것들": {
                "title": "일상 기록",
                "subtitle": "일상 기록 내용"
            },
            "현재시놀로지웹의구성": {
                "title": "시놀로지 웹 구성",
                "subtitle": "현재 시놀로지 웹 구성에 대한 설명"
            }
        },
        # Menu.profile_group.value와 매칭
        "ProfileGroup": {
            # ProfileGroup Enum 값과 매칭
            "프로필": {
                "title": "프로필",
                "subtitle": "프로필 내용"
            }
        },
        # Menu.portfolio_group.value와 매칭
        "PortfolioGroup": {
            # PortfolioGroup Enum 값과 매칭
            "포트폴리오": {
                "title": "포트폴리오",
                "subtitle": "포트폴리오 내용"
            }
        }
    }

    result = content.get(group, {}).get(submenu)
    if result is None:
        logging.warning(f"Content not found for group: {group}, submenu: {submenu}")
        logging.warning(f"Available groups: {list(content.keys())}")
        logging.warning(f"Available submenus for {group}: {list(content.get(group, {}).keys())}")
        return {"error": "Content not found"}

    logging.info(f"Returning content for {group}/{submenu}")
    return result

    # # 디버깅용 로그
    # print("Available content:", json.dumps(content, ensure_ascii=False, indent=2))
    #
    # result = content.get(group, {}).get(submenu)
    # if result is None:
    #     print(f"Content not found for {group}/{submenu}")
    #     return {"error": "Content not found"}
    #
    # print("Returning:", json.dumps(result, ensure_ascii=False))
    # return result