# 📊 GPT 데이터 마스터 Pro - EDA 통합 버전
# 엑셀 파일을 분석하여 시각화 + GPT 인사이트 + 일변량 EDA + 다변량 EDA 히트맵까지 자동 실행됩니다.

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# 🌱 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# 🖥️ Streamlit 설정
st.set_page_config(page_title="📊 GPT 데이터 마스터 Pro", page_icon="🧠")
st.title("📊 GPT 통합 분석 마스터 시스템 (EDA 포함)")
st.markdown("엑셀 파일을 업로드하면 시각화 + GPT 분석 + 일변량 + 다변량 EDA를 한번에 수행합니다.")

# 📁 엑셀 업로드
uploaded_file = st.file_uploader("📁 분석할 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    st.markdown("---")
    st.subheader("📈 시각화 + GPT 분석")

    chart_type = st.selectbox("차트 유형 선택", ["바 차트", "선 차트", "원형 차트"])
    x_col = st.selectbox("X축 컬럼", df.columns)
    y_col = st.selectbox("Y축 컬럼", df.columns)

    if st.button("✅ 분석 실행"):
        fig, ax = plt.subplots()
        if chart_type == "바 차트":
            sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "선 차트":
            sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "원형 차트":
            df_grouped = df.groupby(x_col)[y_col].sum()
            ax.pie(df_grouped, labels=df_grouped.index, autopct="%1.1f%%")
            ax.set_ylabel("")
        st.pyplot(fig)

        # 🔮 GPT 시각화 인사이트
        chart_prompt = PromptTemplate(
            input_variables=["x", "y", "type"],
            template="""
            너는 데이터 분석가야. 다음은 사용자로부터 선택된 시각화 정보야:

            - 차트 종류: {type}
            - X축 항목: {x}
            - Y축 항목: {y}

            이 시각화를 보고 얻을 수 있는 통찰을 간단히 요약해줘.
            """
        )
        gpt_chart = llm.predict(chart_prompt.format(x=x_col, y=y_col, type=chart_type))
        st.markdown("🧠 **GPT 시각화 인사이트 요약**")
        st.info(gpt_chart)

        # 🔍 일변량 EDA
        st.markdown("---")
        st.subheader("📊 일변량 EDA 통계 요약")
        numeric_cols = df.select_dtypes(include=np.number).columns
        univariate = df[numeric_cols].describe()
        st.dataframe(univariate)

        # 🔗 다변량 EDA
        st.markdown("---")
        st.subheader("📊 다변량 EDA (상관계수 히트맵)")
        corr = df[numeric_cols].corr()
        fig2, ax2 = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax2)
        st.pyplot(fig2)

        # GPT 상관관계 해석
        corr_prompt = PromptTemplate(
            input_variables=["corr"],
            template="""
            아래는 상관관계 히트맵입니다. 어떤 변수들 간의 관계가 중요한지 GPT 전문가로서 요약해주세요:

            {corr}
            """
        )
        gpt_corr = llm.predict(corr_prompt.format(corr=corr.to_string()))
        st.markdown("🧠 **GPT 상관관계 인사이트 요약**")
        st.info(gpt_corr)

#실행 명령어 : streamlit run GPT_DataMasterPro.py
