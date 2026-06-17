import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="청소년 수면시간 탐구",
    layout="wide"
)

st.title("필수 생활시간에 따라 변하는 청소년 평균 수면시간")

st.markdown("---")

# ====================================
# 데이터 불러오기
# ====================================

life = pd.read_excel("life.xlsx.xlsx")
sleep = pd.read_excel("sleep_data.xlsx.xlsx")

# ------------------------------------
# 숫자 데이터 자동 추출
# ------------------------------------

life_num = life.select_dtypes(include=np.number)
sleep_num = sleep.select_dtypes(include=np.number)

# 첫 번째 숫자열 = 연도 제외 데이터라고 가정
life_values = life_num.iloc[:, 1]
sleep_values = sleep_num.iloc[:, 1]

# 연도
years = life_num.iloc[:, 0]

# ====================================
# 그래프 1
# ====================================

st.header("1. 필수생활시간 변화 추이")

graph1 = pd.DataFrame({
    "연도": years,
    "필수생활시간": life_values
})

st.line_chart(
    graph1.set_index("연도")
)

increase = (
    (life_values.iloc[-1] - life_values.iloc[0])
    / life_values.iloc[0]
) * 100

st.write(
    f"전체 기간 동안 필수생활시간은 {increase:.2f}% 변화하였다."
)

st.markdown("---")

# ====================================
# 그래프 2
# ====================================

st.header("2. 청소년 평균 수면시간 변화")

graph2 = pd.DataFrame({
    "연도": years,
    "수면시간": sleep_values
})

st.line_chart(
    graph2.set_index("연도")
)

sleep_change = (
    (sleep_values.iloc[-1] - sleep_values.iloc[0])
    / sleep_values.iloc[0]
) * 100

st.write(
    f"전체 기간 동안 평균 수면시간은 {sleep_change:.2f}% 변화하였다."
)

st.markdown("---")

# ====================================
# 비교 그래프
# ====================================

st.header("3. 두 변수 비교")

compare = pd.DataFrame({
    "필수생활시간": life_values.values,
    "수면시간": sleep_values.values
})

st.bar_chart(compare)

st.markdown("---")

# ====================================
# 상관관계 분석
# ====================================

st.header("4. 통계 분석")

corr = life_values.corr(sleep_values)

st.metric(
    "상관계수",
    round(corr, 3)
)

if corr > 0.7:
    relation = "강한 양의 상관관계"

elif corr < -0.7:
    relation = "강한 음의 상관관계"

else:
    relation = "약한 상관관계"

st.write("분석 결과 :", relation)

st.markdown("---")

# ====================================
# 변화율 비교
# ====================================

st.header("5. 변화율 분석")

change_df = pd.DataFrame({
    "구분": ["필수생활시간", "평균수면시간"],
    "변화율": [increase, sleep_change]
})

st.bar_chart(
    change_df.set_index("구분")
)

st.markdown("---")

# ====================================
# 탐구 결론
# ====================================

st.header("6. 탐구 결론")

if corr < 0:
    final_text = """
분석 결과 필수생활시간이 증가할수록 청소년 평균 수면시간은 감소하는 경향을 보였다.

이는 학업, 이동시간, 식사, 학교생활 등 필수생활에 사용되는 시간이 늘어나면서
수면시간이 상대적으로 감소했을 가능성을 보여준다.

따라서 청소년 건강을 위해 생활시간 구조 개선이 필요하다.
"""

else:
    final_text = """
분석 결과 두 변수 사이에 직접적인 연관성이 발견되었다.

생활시간 변화는 청소년의 수면시간 변화에 영향을 줄 가능성이 있다.

추가 연구를 통해 학업과 건강의 균형을 고려해야 한다.
"""

st.write(final_text)

st.markdown("---")

# ====================================
# 통계 요약
# ====================================

st.header("7. 최종 통계 요약")

summary = pd.DataFrame({
    "항목": [
        "필수생활시간 변화율",
        "수면시간 변화율",
        "상관계수"
    ],
    "결과": [
        round(increase,2),
        round(sleep_change,2),
        round(corr,3)
    ]
})

st.dataframe(summary)
