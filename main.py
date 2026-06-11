import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="청소년 수면시간 탐구보고서",
    layout="wide"
)

st.title("필수생활시간에 따라 변하는 청소년 평균 수면시간")

# =====================
# 데이터 불러오기
# =====================

life_file = "필수생활시간_20260611113006.xlsx"
sleep_file = "청소년+평균수면시간+및+주관적+건강인지율_20260611112856_분석(2007_대비_증감).xlsx"

life_raw = pd.read_excel(life_file, sheet_name="데이터")
sleep_raw = pd.read_excel(sleep_file, sheet_name="데이터")

# =====================
# 필수생활시간 데이터 정리
# =====================

life_row = life_raw[
    (life_raw["행동분류별(1)"] == "필수생활시간") &
    (life_raw["행동분류별(2)"] == "소계")
].iloc[0]

years = [1999, 2004, 2009, 2014, 2019, 2024]

life_time = []

for year in years:
    value = life_row[str(year)]

    h, m = map(int, str(value).split(":"))
    life_time.append(round(h + m/60, 2))

life_df = pd.DataFrame({
    "연도": years,
    "필수생활시간": life_time
})

# =====================
# 청소년 수면시간 데이터 정리
# =====================

sleep_df = sleep_raw.iloc[1:].copy()

sleep_df.columns = [
    "연도",
    "수면시간",
    "남학생수면",
    "여학생수면",
    "건강인지율",
    "남학생건강",
    "여학생건강"
]

sleep_df["연도"] = pd.to_numeric(sleep_df["연도"])

sleep_df["수면시간"] = pd.to_numeric(
    sleep_df["수면시간"],
    errors="coerce"
)

sleep_df["건강인지율"] = pd.to_numeric(
    sleep_df["건강인지율"],
    errors="coerce"
)

# =====================
# 화면 구성
# =====================

tab1, tab2, tab3, tab4 = st.tabs([
    "필수생활시간",
    "수면시간",
    "상관관계",
    "탐구결론"
])

# =====================
# 탭1
# =====================

with tab1:

    st.header("필수생활시간 변화")

    st.dataframe(life_df)

    st.line_chart(
        life_df.set_index("연도")
    )

# =====================
# 탭2
# =====================

with tab2:

    st.header("청소년 평균 수면시간 변화")

    st.dataframe(
        sleep_df[["연도", "수면시간"]]
    )

    st.line_chart(
        sleep_df.set_index("연도")[["수면시간"]]
    )

# =====================
# 탭3
# =====================

with tab3:

    st.header("상관관계 분석")

    merge_df = pd.merge_asof(
        sleep_df.sort_values("연도"),
        life_df.sort_values("연도"),
        on="연도",
        direction="nearest"
    )

    corr = merge_df[
        ["수면시간", "필수생활시간"]
    ].corr().iloc[0,1]

    st.metric(
        "상관계수",
        round(corr, 3)
    )

    st.write("""
    상관계수 해석

    - 1에 가까울수록 강한 양의 상관관계
    - 0에 가까울수록 관계 없음
    - -1에 가까울수록 강한 음의 상관관계
    """)

    st.dataframe(
        merge_df[
            ["연도","수면시간","필수생활시간"]
        ]
    )

# =====================
# 탭4
# =====================

with tab4:

    st.header("탐구 결론")

    latest_sleep = sleep_df["수면시간"].iloc[-2]

    st.write(f"""
### 연구 결과

1. 필수생활시간은 전반적으로 증가하는 경향을 보였다.

2. 청소년 평균 수면시간은 장기적으로 감소하는 경향을 보였다.

3. 상관계수는 **{round(corr,3)}** 로 나타났다.

4. 이는 필수생활시간 변화가 청소년 수면시간 변화와 일정한 관련성이 있음을 보여준다.

5. 따라서 청소년의 충분한 수면 확보를 위해서는 학업·통학·식사 등 필수생활시간을 고려한 생활 설계가 필요하다.
""")
