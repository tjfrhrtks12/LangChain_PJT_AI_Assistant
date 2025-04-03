# 📊 GPT_DataMasterPro.py - GPT 기반 엑셀 통합 분석 시스템 (EDA + 시각화 + 질문 분석)

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from io import BytesIO
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_experimental.agents import create_pandas_dataframe_agent

# 🌱 환경변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ GPT 연결
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# 🎨 한글 깨짐 방지 설정
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows용
plt.rcParams["axes.unicode_minus"] = False

# 🌐 Streamlit 앱 기본 설정
st.set_page_config(page_title="GPT 데이터마스터 PRO", page_icon="🧠")
st.title("🧠 GPT 데이터마스터 PRO")
st.markdown("엑셀 파일을 업로드하면 자동 분석 + 질문 기반 인사이트까지 모두 수행해드립니다!")

# 📁 파일 업로드
uploaded_file = st.file_uploader("📤 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    st.markdown("---")
    chart_type = st.selectbox("📊 시각화 유형", ["바 차트", "선 차트", "원형 차트"])
    x_col = st.selectbox("🔠 X축 컬럼", df.columns)
    y_col = st.selectbox("🔢 Y축 컬럼", df.columns)

    if st.button("📈 분석 및 보고서 생성"):
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

        # ✅ GPT 인사이트 요약
        prompt = PromptTemplate(
            input_variables=["x", "y", "type"],
            template="""
            너는 데이터 분석가야. 아래는 사용자 선택 정보야:

            - 차트 종류: {type}
            - X축: {x}
            - Y축: {y}

            이 정보를 바탕으로 유의미한 인사이트를 핵심만 간결하게 요약해줘.
            """
        ).format(x=x_col, y=y_col, type=chart_type)
        explanation = llm.predict(prompt)

        # ✅ 상관관계 해석
        corr_prompt = f"""
        다음은 데이터의 상관관계 행렬이야:\n{corr.to_string()}\n
        어떤 변수 간 관계가 강하거나 약한지 핵심 인사이트만 짧게 요약해줘.
        """
        gpt_corr_summary = llm.predict(corr_prompt)

        # ✅ 보고서 저장
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_text = f"""[GPT 자동 보고서 생성 시간: {now}]

[시각화 정보]
차트 유형: {chart_type}
X축: {x_col}
Y축: {y_col}

[시각화 인사이트]
{explanation}

[상관관계 인사이트]
{gpt_corr_summary}
"""
        buffer = BytesIO()
        buffer.write(report_text.encode("utf-8"))
        buffer.seek(0)

        st.success("✅ 보고서 생성 완료!")
        st.download_button("📩 보고서 다운로드 (TXT)", data=buffer, file_name=f"GPT_Report_{now}.txt")

    # ✅ 사용자 질문 기반 분석
    st.markdown("---")
    st.subheader("💬 질문 기반 GPT 분석")
    question = st.text_input("궁금한 점을 질문하세요 (예: 가장 높은 매출 지역은?)")

    if st.button("🔍 GPT에게 분석 요청"):
        agent = create_pandas_dataframe_agent(
            llm, df,
            verbose=False,
            agent_type="openai-tools",
            handle_parsing_errors=True,
            allow_dangerous_code=True
        )
        answer = agent.run(question)
        st.info(answer)

# 실행 명령어 : streamlit run GPT_DataMasterPro.py
