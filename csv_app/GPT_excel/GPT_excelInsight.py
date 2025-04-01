# 📊 GPT 자동 인사이트 제안 시스템 (GPT_excelInsight.py)
# 엑셀 데이터 업로드 → GPT가 분석 방향 제안 → 선택 시 시각화 + 해석까지 수행

import pandas as pd
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 🌱 환경 변수 로드 및 GPT 모델 설정
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# 🖥️ Streamlit UI 설정
st.set_page_config(page_title="📈 GPT 자동 인사이트 분석기", page_icon="🔍")
st.title("📈 GPT 자동 인사이트 분석기")
st.markdown("엑셀 데이터를 업로드하면 GPT가 분석 방향을 추천하고 시각화합니다!")

# 📁 파일 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    # 🔍 GPT에게 인사이트 추천 요청
    st.markdown("---")
    st.subheader("🧠 GPT가 추천하는 분석 방향")

    col_list = ", ".join(df.columns)
    prompt = PromptTemplate(
        input_variables=["columns"],
        template="""
        너는 뛰어난 데이터 분석가야. 사용자로부터 다음과 같은 데이터 컬럼들이 주어졌어:
        [컬럼 목록]: {columns}

        이 데이터를 분석한다면 어떤 분석을 추천할지 3가지로 간결하게 알려줘.
        각각 어떤 컬럼을 분석 대상으로 쓰는지 함께 설명해줘.
        """
    )
    gpt_recommend = llm.predict(prompt.format(columns=col_list))
    st.info(gpt_recommend)

    # 🎯 사용자 선택 후 시각화
    st.markdown("---")
    st.subheader("📊 시각화 실행")

    chart_type = st.selectbox("차트 유형 선택", ["바 차트", "선 차트", "원형 차트"])
    x_col = st.selectbox("X축 컬럼", df.columns)
    y_col = st.selectbox("Y축 컬럼", df.columns)

    if st.button("📈 시각화 및 해석 실행"):
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

        # GPT 해석 출력
        explain_prompt = PromptTemplate(
            input_variables=["x", "y", "type"],
            template="""
            다음은 사용자가 선택한 시각화 설정이야:
            - 차트 종류: {type}
            - X축: {x}
            - Y축: {y}

            이 데이터를 바탕으로 의미 있는 인사이트를 간결히 설명해줘.
            """
        )
        gpt_explanation = llm.predict(explain_prompt.format(x=x_col, y=y_col, type=chart_type))

        st.markdown("🧠 **GPT 분석 결과:**")
        st.success(gpt_explanation)

# ▶ 실행 명령어
# streamlit run csv_app/GPT_excel/GPT_excelInsight.py
