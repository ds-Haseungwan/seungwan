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

# EC별 학교 정보
school_info = {
    "송도고": {"EC": 1.0, "color": "blue", "students": 29},
    "하늘고": {"EC": 2.0, "color": "green", "students": 45},
    "아라고": {"EC": 4.0, "color": "orange", "students": 106},
    "동산고": {"EC": 8.0, "color": "red", "students": 58},
}

# 파일 경로 설정
DATA_PATH = Path("data")

# 데이터 로딩 함수
@st.cache_data
def load_data():
    data = {}
    for file in DATA_PATH.iterdir():
        if file.suffix == '.csv':
            school_name = file.stem
            data[school_name] = pd.read_csv(file)
        elif file.suffix == '.xlsx':
            data["생육결과"] = pd.read_excel(file, sheet_name=None)
    return data

# 데이터 불러오기
data = load_data()

# 학교 선택 드롭다운
school_name = st.sidebar.selectbox("학교 선택", ["전체", "송도고", "하늘고", "아라고", "동산고"])

# 📖 실험 개요 탭
if school_name == "전체":
    st.title("🌱 극지식물 최적 EC 농도 연구")
    st.write("### 연구 배경 및 목적")
    st.write("각 학교의 EC 조건에 맞춰 극지식물의 생육 결과를 분석합니다.")
    st.write("### 학교별 EC 조건")
    ec_data = pd.DataFrame(school_info).T
    st.table(ec_data[['EC', 'students', 'color']])

    # 주요 지표 카드
    st.write("### 주요 지표")
    st.metric("총 개체수", sum(school_info[school]['students'] for school in school_info))
    st.metric("최적 EC", "2.0 (하늘고)")
    
# 환경 데이터 탭
elif school_name == "🌡️ 환경 데이터":
    st.title("환경 데이터")
    
    # 학교별 환경 평균 비교
    if school_name in data:
        school_data = data[school_name]
        st.write(f"### {school_name} 환경 데이터")
        
        # 그래프
        fig = make_subplots(rows=2, cols=2)
        
        fig.add_trace(go.Bar(x=["온도"], y=school_data["temperature"], name="온도"))
        fig.add_trace(go.Bar(x=["습도"], y=school_data["humidity"], name="습도"))
        fig.add_trace(go.Bar(x=["pH"], y=school_data["ph"], name="pH"))
        
        fig.update_layout(height=600, title_text="온도/습도/PH/EC 비교")
        st.plotly_chart(fig)

# 생육 결과
elif school_name == "📊 생육 결과":
    st.write("생육 결과")

# 다운로드 버튼
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

