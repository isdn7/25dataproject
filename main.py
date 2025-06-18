import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연령별 인구 구조 시각화", layout="wide")
st.title("지역별 연령별 인구 구조 시각화")

# 1. 파일 불러오기 (업로드 기능 X, 프로젝트 루트의 CSV만 사용)
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="cp949")

# 2. 컬럼명 자동 감지
지역_컬럼 = "행정구역"
연령컬럼목록 = [col for col in df.columns if "계_" in col and ("세" in col or "이상" in col) and not ("총인구수" in col or "연령구간인구수" in col)]
연령구간 = [col.split('_')[-1] for col in 연령컬럼목록]

# 3. 지역 검색 & 선택 기능
st.subheader("지역명 검색 후 선택")
search = st.text_input("찾고 싶은 지역명을 입력하세요 (예: 강남, 용산, 청운)", "")
지역목록 = df[지역_컬럼].unique()
if search:
    지역_후보 = [z for z in 지역목록 if search in z]
else:
    # 아무 것도 안 입력하면 전체 상위 20개만 보여주기 (너무 많으면 UX 안 좋으니)
    지역_후보 = 지역목록[:20]

선택지역 = st.selectbox("아래에서 지역을 선택하세요", 지역_후보)

# 4. 연령별 인구 데이터 추출 및 변환
if 선택지역:
    지역_df = df[df[지역_컬럼] == 선택지역]
    인구수 = []
    for col in 연령컬럼목록:
        val = 지역_df[col].values[0]
        try:
            val = int(str(val).replace(",", ""))
        except:
            val = 0
        인구수.append(val)
    pop_df = pd.DataFrame({
        "연령": 연령구간,
        "인구수": 인구수
    })
    # 5. Plotly 그래프 출력
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

