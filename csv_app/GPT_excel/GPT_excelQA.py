# 엑셀 파일을 업로드하면
# 시트 선택
# 미리보기
# 📈 자동 분석
# 💬 GPT가 해석까지!

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
import os

# ✅ 한글 설정
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 🔐 OpenAI 키 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=api_key)

# 🌐 페이지 설정
st.set_page_config(page_title="엑셀 GPT 분석기", page_icon="📊")
st.title("📊 성주의 Excel 기반 GPT 분석기")
st.markdown("엑셀(.xlsx)을 업로드하면 GPT가 분석해줍니다!")

# 📁 엑셀 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file is not None:
    # 🔄 시트 목록 확인
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    sheet = st.selectbox("분석할 시트를 선택하세요", sheet_names)

    # ✅ 선택된 시트 읽기
    df = pd.read_excel(uploaded_file, sheet_name=sheet)
    st.subheader("📄 데이터 미리보기")
    st.dataframe(df)

    # 📊 자동 시각화 (예: 단가 vs 판매량)
    st.subheader("📈 자동 시각화 (예시)")
    if "단가" in df.columns and "판매량" in df.columns:
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x="단가", y="판매량", hue="제품명", s=100, ax=ax)
        plt.title("단가 vs 판매량")
        st.pyplot(fig)

    # 🧠 GPT 해석
    st.subheader("🧠 GPT 자동 해석")
    describe_text = df.describe(include='all').to_string()
    head_text = df.head().to_string()

    prompt = f"""
    아래는 Excel 데이터입니다.
    [요약 통계]
    {describe_text}

    [샘플 데이터]
    {head_text}

    이 데이터를 분석해서 중요한 특징과 의미 있는 인사이트를 알려줘.
    """

    with st.spinner("GPT가 분석 중입니다..."):
        response = llm(prompt)

    st.success("✅ GPT의 분석 결과:")
    st.write(response)

else:
    st.info("먼저 .xlsx 파일을 업로드해주세요.")

#실행 명령어 : streamlit run csv_app/Chat_GPT_excelQA.py

