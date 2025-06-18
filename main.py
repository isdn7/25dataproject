import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연령별 인구 구조 시각화", layout="wide")
st.title("지역별 연령별 인구 구조 시각화")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="cp949")
else:
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="cp949")

# 컬럼명 자동 추출
지역_컬럼 = "행정구역"
연령컬럼목록 = [col for col in df.columns if "계_" in col and ("세" in col or "이상" in col) and not ("총인구수" in col or "연령구간인구수" in col)]

# 지역 선택
지역목록 = df[지역_컬럼].unique()
선택지역 = st.selectbox("지역 선택", 지역목록)
지역_df = df[df[지역_컬럼] == 선택지역]

# 연령별 인구 데이터 추출
연령구간 = [col.split('_')[-1] for col in 연령컬럼목록]
인구수 = 지역_df[연령컬럼목록].iloc[0].str.replace(",", "").astype(int).tolist()

pop_df = pd.DataFrame({
    "연령": 연령구간,
    "인구수": 인구수
})

# 그래프 (세로 막대)
fig = px.bar(
    pop_df,
    x="연령",
    y="인구수",
    title=f"{선택지역} 연령별 인구 구조",
    labels={"연령": "연령(세)", "인구수": "인구수"},
    hover_data=["인구수"]
)
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)
