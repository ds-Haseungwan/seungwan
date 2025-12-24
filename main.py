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
    return unicodedata.normalize("NFC", filename)

# 데이터 로딩 함수
@st.cache_data
def load_data():
    data = {}
    for file in DATA_PATH.iterdir():
        if file.suffix == '.csv':
            school_name = normalize_filename(file.stem)
            data[school_name] = pd.read_csv(file)
        elif file.suffix == '.xlsx':
            data["생육결과"] = pd.read_excel(file, sheet_name=None)
    return data

# 데이터 불러오기
data = load_data()

# 학교 선택 드롭다운
school_name = st.sidebar.selectbox("학교 선택", ["전체", "송도고", "하늘고", "아라고", "동산고"])

# 📊 데이터 처리 및 시각화 함수
def plot_temperature_ec_corr(df):
    fig = make_subplots(rows=1, cols=1)
    
    # 온도-EC 상관 관계 그래프
    fig.add_trace(go.Scatter(x=df["temperature"], y=df["ec"], mode="markers", name="온도 vs EC"))
    fig.update_layout(title="온도와 EC의 상관 관계", font=dict(family="Malgun Gothic, sans-serif"))
    st.plotly_chart(fig)

def plot_temperature_ph_corr(df):
    fig = make_subplots(rows=1, cols=1)
    
    # 온도-pH 상관 관계 그래프
    fig.add_trace(go.Scatter(x=df["temperature"], y=df["ph"], mode="markers", name="온도 vs pH"))
    fig.update_layout(title="온도와 pH의 상관 관계", font=dict(family="Malgun Gothic, sans-serif"))
    st.plotly_chart(fig)

def plot_ec_ph_corr(df):
    fig = make_subplots(rows=1, cols=1)
    
    # EC-pH 상관 관계 그래프
    fig.add_trace(go.Scatter(x=df["ec"], y=df["ph"], mode="markers", name="EC vs pH"))
    fig.update_layout(title="EC와 pH의 상관 관계", font=dict(family="Malgun Gothic, sans-serif"))
    st.plotly_chart(fig)

# 온도별 성장률 계산 및 시각화
def plot_growth_rate_by_temperature(df):
    fig = make_subplots(rows=1, cols=1)
    
    # 성장률을 온도별로 시각화 (생중량 / 시간)
    df["growth_rate"] = df["생중량(g)"] / df["time"]  # 성장률 예시 계산 (시간 대비 생중량)
    fig.add_trace(go.Scatter(x=df["temperature"], y=df["growth_rate"], mode="lines+markers", name="성장률"))
    fig.update_layout(title="온도별 성장률", font=dict(family="Malgun Gothic, sans-serif"))
    st.plotly_chart(fig)

# Tab1: 온도-ec, 온도-ph, ec-ph 상관관계
if school_name == "전체":
    st.title("극지 식물의 온도별 성장률")
    st.write("### 온도, EC, pH 간의 상관 관계")

    if "송도고" in data:
        school_data = data["송도고"]
        st.write("### 송도고 데이터")
        plot_temperature_ec_corr(school_data)
        plot_temperature_ph_corr(school_data)
        plot_ec_ph_corr(school_data)

# Tab2: 온도별 성장률
if school_name == "온도별 성장률":
    st.title("온도별 성장률")

    if "송도고" in data:
        school_data = data["송도고"]
        st.write("### 송도고 데이터")
        plot_growth_rate_by_temperature(school_data)

# Tab3: 극지생물이지만 상온 환경에서도 잘 자람
if school_name == "극지생물이지만 상온 환경에서도 잘 자람":
    st.title("극지 생물이지만 상온 환경에서도 잘 자람")
    st.write("극지 식물은 상온 환경에서도 자라나며, 온도에 따른 다양한 변화를 보여줍니다.")

# XLSX 다운로드 버튼
def generate_xlsx(df):
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)
    return buffer

# 다운로드 버튼
st.download_button(
    label="데이터 다운로드",
    data=generate_xlsx(df),
    file_name="data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
