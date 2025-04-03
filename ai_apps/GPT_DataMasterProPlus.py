# 📊 GPT_DataMasterProPlus.py - 바탕체 기반 GPT 통합 분석 시스템

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_experimental.agents import create_pandas_dataframe_agent

# 🌱 환경변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ GPT 연결
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# 🎨 한글 깨짐 방지 설정 (Matplotlib)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 🌐 Streamlit 앱 설정
st.set_page_config(page_title="GPT 데이터마스터 PRO", page_icon="🤖")
st.title("🤖 GPT 데이터마스터 PRO")
st.markdown("엑셀 파일을 업로드하면 자동 EDA, GPT 분석, PDF 저장까지 완료!")

# 📁 엑셀 업로드
uploaded_file = st.file_uploader("📤 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    chart_type = st.selectbox("📊 차트 유형", ["바 차트", "선 차트", "원형 차트"])
    x_col = st.selectbox("🔠 X축 컬럼", df.columns)
    y_col = st.selectbox("🔢 Y축 컬럼", df.columns)

    if st.button("📈 분석 및 PDF 저장"):
        # ✅ 시각화
        fig, ax = plt.subplots()
        if chart_type == "바 차트":
            sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "선 차트":
            sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "원형 차트":
            grouped = df.groupby(x_col)[y_col].sum()
            ax.pie(grouped, labels=grouped.index, autopct="%1.1f%%")
            ax.set_ylabel("")
        st.pyplot(fig)

        # ✅ 일변량 EDA
        st.subheader("📊 일변량 EDA")
        st.dataframe(df.describe(include="all"))

        # ✅ 다변량 EDA
        st.subheader("🔗 다변량 EDA (상관관계 히트맵)")
        corr = df.corr(numeric_only=True)
        fig_corr, ax_corr = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="Blues", ax=ax_corr)
        st.pyplot(fig_corr)

        # ✅ GPT 해석
        summary_prompt = PromptTemplate(
            input_variables=["x", "y", "type"],
            template="""
            너는 데이터 분석가야. 아래는 사용자 선택 정보야:
            - 차트 종류: {type}
            - X축: {x}
            - Y축: {y}
            이 정보를 바탕으로 의미 있는 인사이트를 간결하게 설명해줘.
            """
        ).format(x=x_col, y=y_col, type=chart_type)
        chart_summary = llm.predict(summary_prompt)

        corr_summary = llm.predict(
            f"다음은 데이터의 상관관계 행렬이야:\n{corr.to_string()}\n요약해서 설명해줘."
        )

        # ✅ PDF 저장
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = f"GPT_Report_{now}.pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("batang", fname="./csv_app/fonts/batang.ttc", uni=True)
        pdf.set_font("batang", size=12)

        pdf.multi_cell(0, 10, f"[GPT 자동 보고서 생성 시간: {now}]\n\n")
        pdf.multi_cell(0, 10, f"[시각화 정보]\n차트 유형: {chart_type}\nX축: {x_col}\nY축: {y_col}\n")
        pdf.multi_cell(0, 10, f"[시각화 인사이트]\n{chart_summary}\n")
        pdf.multi_cell(0, 10, f"[상관관계 인사이트]\n{corr_summary}\n")

        pdf.output(pdf_path)
        st.success("📄 PDF 보고서 저장 완료!")
        with open(pdf_path, "rb") as f:
            st.download_button("📥 PDF 다운로드", data=f, file_name=pdf_path)

    # ✅ 사용자 질문 기반 분석
    st.subheader("💬 질문 기반 분석")
    question = st.text_input("GPT에게 분석 질문을 해보세요:")

    if st.button("🔍 GPT 분석 실행"):
        agent = create_pandas_dataframe_agent(llm, df, verbose=False, allow_dangerous_code=True)
        answer = agent.run(question)
        st.info(answer)

# ✅ 실행 명령어
# streamlit run GPT_DataMasterProPlus.py


