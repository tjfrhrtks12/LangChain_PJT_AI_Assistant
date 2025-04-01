# 🧠 핵심 기능
# Pandas + Seaborn으로 차트 시각화
# GPT에게 plt.savefig()로 저장된 이미지를 설명하도록 전달
# 또는 GPT에게 시각화된 데이터의 요약 통계 정보를 전달하여 분석하게 하기

# ✅ GPT_excelChartExplainer.py 주요 기능
# 엑셀 파일 업로드
# 시각화 옵션 선택 (예: 바 차트, 원형 차트, 선형 차트 등)
# 시각화 실행
# GPT가 자동으로 그래프를 해석해서 설명 제공

###보고서 생성기와 연동을 해야함###


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# GPT 모델 설정
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# Streamlit 페이지 설정
st.set_page_config(page_title="📊 GPT 엑셀 시각화 분석기", page_icon="📈")
st.title("📊 GPT 엑셀 시각화 분석기")
st.markdown("엑셀 데이터를 업로드하고 시각화 타입을 선택하면 GPT가 자동으로 해석해드려요!")

# 파일 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일을 업로드하세요", type=["xlsx"])

# 시각화 실행
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📄 미리보기")
    st.dataframe(df.head())

    st.markdown("---")

    # 시각화 선택
    chart_type = st.selectbox("📊 시각화 유형을 선택하세요", ["바 차트", "선 차트", "원형 차트"])
    x_col = st.selectbox("🧩 X축 컬럼 선택", df.columns)
    y_col = st.selectbox("🧩 Y축 컬럼 선택", df.columns)

    if st.button("📈 시각화 실행"):
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

        # GPT에게 시각화 해석 요청
        chart_prompt = PromptTemplate(
            input_variables=["x", "y", "type"],
            template="""
너는 데이터 분석가야. 다음은 사용자로부터 선택된 시각화 정보야:

- 차트 종류: {type}
- X축 항목: {x}
- Y축 항목: {y}

이 정보를 바탕으로 사용자에게 어떤 인사이트가 나올 수 있는지 간단히 설명해줘. 너무 길게 말하지 말고 핵심만 짚어줘!
"""
        )

        prompt = chart_prompt.format(x=x_col, y=y_col, type=chart_type)
        gpt_response = llm.predict(prompt)

        st.markdown("🧠 **GPT 분석 결과:**")
        st.info(gpt_response)
