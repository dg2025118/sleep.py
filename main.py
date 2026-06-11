import streamlit as st
import pandas as pd

st.title("엑셀 파일 구조 확인")

life_file = "필수생활시간_20260611113006.xlsx"
sleep_file = "청소년+평균수면시간+및+주관적+건강인지율_20260611112856_분석(2007_대비_증감).xlsx"

for file in [life_file, sleep_file]:
    st.header(file)

    xls = pd.ExcelFile(file)

    st.write("시트 목록")
    st.write(xls.sheet_names)

    for sheet in xls.sheet_names:
        st.subheader(sheet)

        df = pd.read_excel(file, sheet_name=sheet)

        st.write("컬럼명")
        st.write(df.columns.tolist())

        st.dataframe(df.head())
