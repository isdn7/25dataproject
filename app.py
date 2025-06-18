import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연령별 인구 구조 시각화", layout="wide")

st.title("지역별 연령별 인구 구조 시각화")
st.write("업로드된 월별 연령별 인구현황 자료를 바탕으로 원하는 지역의 인구 피라미드를 확인하세요.")

# 파일 업로드 or 기본 파일 사용
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="cp949")  # 대부분의 인구통계는 cp949/utf-8로 저장됨
else:
    # Streamlit Cloud 사용시, 파일을 프로젝트 루트에 넣었다고 가정
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="cp949")

# 데이터 구조 확인 및 전처리 예시
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 주요 컬럼 추출 예시 (컬럼명은 실제 파일과 맞게 수정 필요)
# 예시: ["시도", "시군구", "연령구간", "남자", "여자", "총인구"]
지역_컬럼 = [col for col in df.columns if "시군구" in col or "행정구역" in col or "지역" in col]
연령_컬럼 = [col for col in df.columns if "연령" in col]
남_컬럼 = [col for col in df.columns if "남" in col and "인구" in col]
여_컬럼 = [col for col in df.columns if "여" in col and "인구" in col]
총_컬럼 = [col for col in df.columns if "총" in col and "인구" in col]

# 지역 선택
if 지역_컬럼:
    지역명 = 지역_컬럼[0]
    지역목록 = sorted(df[지역명].unique())
    선택지역 = st.selectbox("지역 선택", 지역목록)
    지역_df = df[df[지역명] == 선택지역]
else:
    st.error("지역(시군구/행정구역) 컬럼이 자동 감지되지 않았어요. app.py에서 컬럼명을 직접 지정해주세요!")
    st.stop()

# 연령 구간, 남/여 추출
연령구간명 = 연령_컬럼[0] if 연령_컬럼 else "연령구간"
남자_컬럼 = 남_컬럼[0] if 남_컬럼 else "남자인구수"
여자_컬럼 = 여_컬럼[0] if 여_컬럼 else "여자인구수"

# 인구 피라미드 데이터셋 가공
pop_df = 지역_df[[연령구간명, 남자_컬럼, 여자_컬럼]].copy()
pop_df[남자_컬럼] = -pop_df[남자_컬럼].astype(int)  # 남자는 음수로, 피라미드 형태
pop_df[여자_컬럼] = pop_df[여자_컬럼].astype(int)

# 연령 구간 정렬 (예: "0~4세", "5~9세", ... 순으로)
pop_df[연령구간명] = pd.Categorical(pop_df[연령구간명], categories=sorted(pop_df[연령구간명].unique(), key=lambda x: int(x.split('~')[0].replace('세', '').replace(' ', ''))), ordered=True)
pop_df = pop_df.sort_values(연령구간명)

# Plotly 피라미드 그래프
fig = px.bar(
    pop_df,
    x=[남자_컬럼, 여자_컬럼],
    y=연령구간명,
    orientation='h',
    color_discrete_sequence=["blue", "pink"],
    labels={남자_컬럼: "남자", 여자_컬럼: "여자"},
    title=f"{선택지역} 연령별 인구 구조 (인구 피라미드)",
)

fig.update_layout(
    barmode='relative',
    xaxis_title="인구수",
    yaxis_title="연령 구간",
    xaxis_tickformat=',',
    bargap=0.1,
    legend_title_text="성별",
    width=900,
    height=700,
)

st.plotly_chart(fig, use_container_width=True)
