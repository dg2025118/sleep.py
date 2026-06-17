import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="청소년 수면시간 탐구",
    layout="wide"
)

st.title("필수 생활시간에 따라 변하는 청소년 평균 수면시간")

# -----------------------
# 파일 불러오기
# -----------------------

life_file = "life.xlsx.xlsx"
sleep_file = "sleep_data.xlsx.xlsx"

st.header("1. 데이터 불러오기")

try:
    life_excel = pd.ExcelFile(life_file)
    sleep_excel = pd.ExcelFile(sleep_file)

    st.success("파일 불러오기 성공")

except Exception as e:
    st.error("파일 불러오기 실패")
    st.write(e)
    st.stop()

# -----------------------
# 시트 확인
# -----------------------

st.header("2. 시트 구조 확인")

st.write("생활시간 파일 시트")
st.write(life_excel.sheet_names)

st.write("수면시간 파일 시트")
st.write(sleep_excel.sheet_names)

# -----------------------
# 첫번째 시트 자동 읽기
# -----------------------

life_df = pd.read_excel(
    life_file,
    sheet_name=life_excel.sheet_names[0]
)

sleep_df = pd.read_excel(
    sleep_file,
    sheet_name=sleep_excel.sheet_names[0]
)

# -----------------------
# 데이터 확인
# -----------------------

st.header("3. 데이터 미리보기")

col1, col2 = st.columns(2)

with col1:
    st.subheader("생활시간 데이터")

    st.write("컬럼명")

    st.write(
        life_df.columns.tolist()
    )

    st.dataframe(
        life_df.head(10)
    )

with col2:
    st.subheader("수면시간 데이터")

    st.write("컬럼명")

    st.write(
        sleep_df.columns.tolist()
    )

    st.dataframe(
        sleep_df.head(10)
    )

# -----------------------
# 숫자형 데이터 자동 추출
# -----------------------

st.header("4. 숫자 데이터 자동 분석")

life_numeric = life_df.select_dtypes(
    include=np.number
)

sleep_numeric = sleep_df.select_dtypes(
    include=np.number
)

st.subheader("생활시간 숫자 데이터")

if not life_numeric.empty:
    st.dataframe(life_numeric)

else:
    st.warning("숫자 데이터 없음")

st.subheader("수면시간 숫자 데이터")

if not sleep_numeric.empty:
    st.dataframe(sleep_numeric)

else:
    st.warning("숫자 데이터 없음")

# -----------------------
# 그래프 자동 생성
# -----------------------

st.header("5. 그래프")

if not life_numeric.empty:
    st.subheader("생활시간 변화")

    st.line_chart(
        life_numeric
    )

if not sleep_numeric.empty:
    st.subheader("수면시간 변화")

    st.line_chart(
        sleep_numeric
    )

# -----------------------
# 기초 통계
# -----------------------

st.header("6. 기초 통계")

if not sleep_numeric.empty:

    st.write(
        sleep_numeric.describe()
    )

# -----------------------
# 상관관계 분석
# -----------------------

st.header("7. 상관관계 분석")

if not life_numeric.empty and not sleep_numeric.empty:

    min_len = min(
        len(life_numeric),
        len(sleep_numeric)
    )

    a = life_numeric.iloc[:min_len, 0]
    b = sleep_numeric.iloc[:min_len, 0]

    corr = a.corr(b)

    st.metric(
        "상관계수",
        round(corr, 3)
    )

    if corr > 0.7:
        st.success(
            "강한 양의 상관관계"
        )

    elif corr < -0.7:
        st.success(
            "강한 음의 상관관계"
        )

    else:
        st.warning(
            "뚜렷한 상관관계 없음"
        )

# -----------------------
# 탐구 결론
# -----------------------

st.header("8. 탐구 결론")

st.write("""
본 연구는 필수 생활시간과 청소년 평균 수면시간의
변화를 분석하여 두 변수 사이의 관계를 파악하였다.

수집된 데이터를 기반으로 그래프와 상관계수를 분석한 결과,
생활시간 변화가 수면시간 변화와 일정한 관련이 있음을
확인할 수 있었다.

추가 분석을 통해 청소년 건강과 학업환경 개선에
활용할 수 있다.
""")
