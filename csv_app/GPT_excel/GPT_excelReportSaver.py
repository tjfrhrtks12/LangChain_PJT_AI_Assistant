import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import io

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# GPT 모델 설정
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# Streamlit 설정
st.set_page_config(page_title="📑 GPT 자동 보고서 생성기", page_icon="📝")
st.title("📑 GPT 자동 보고서 생성기")
st.markdown("엑셀 데이터를 기반으로 차트와 해석 내용을 보고서로 저장합니다!")

# 파일 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📄 데이터 미리보기")
    st.dataframe(df.head())

    st.markdown("---")
    st.subheader("📈 시각화 설정")

    chart_type = st.selectbox("📊 차트 유형", ["바 차트", "선 차트", "원형 차트"])
    x_col = st.selectbox("🔵 X축", df.columns)
    y_col = st.selectbox("🟣 Y축", df.columns)

    if st.button("📊 시각화 및 보고서 생성"):
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

        # GPT 해석 요청
        prompt_template = PromptTemplate(
            input_variables=["x", "y", "type"],
            template="""
너는 데이터 분석가야. 다음은 사용자로부터 선택된 시각화 정보야:

- 차트 종류: {type}
- X축 항목: {x}
- Y축 항목: {y}

이 정보를 바탕으로 사용자가 얻을 수 있는 데이터 인사이트를 간결하게 설명해줘.
"""
        )
        prompt = prompt_template.format(x=x_col, y=y_col, type=chart_type)
        interpretation = llm.predict(prompt)

        st.subheader("🧠 GPT 해석 결과")
        st.info(interpretation)

        # 보고서 저장
        st.markdown("---")
        st.subheader("📥 보고서 저장")

        buffer = io.StringIO()
        buffer.write("📊 GPT 자동 보고서\n")
        buffer.write(f"▶ 차트 유형: {chart_type}\n")
        buffer.write(f"▶ X축: {x_col}\n")
        buffer.write(f"▶ Y축: {y_col}\n\n")
        buffer.write("📌 GPT 해석 요약:\n")
        buffer.write(interpretation)

        report_filename = "GPT_엑셀_시각화_보고서.txt"
        st.download_button("📩 보고서 저장 (텍스트)", buffer.getvalue(), file_name=report_filename)
