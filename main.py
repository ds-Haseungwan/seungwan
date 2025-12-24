import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import unicodedata
from pathlib import Path
import io

# 한글 폰트 깨짐 방지
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# 파일 경로 설정
DATA_PATH = Path("data")

# 파일 인식 함수
def normalize_filename(filename: str) -> str:
    """파일명 정상화 (NFC)"""
    return un
