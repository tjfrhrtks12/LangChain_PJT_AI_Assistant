# 📦 GPT 데이터 통합 분석 시스템 (GPT_DataMaster.py)

# 📊 GPT_DataMaster.py
# -----------------------------------------------------------
# ✅ 엑셀 기반 GPT 데이터 분석 통합 시스템 (All-in-One Assistant)
#
# ▶ 주요 기능:
#   - 엑셀 파일 업로드
#   - 시각화 타입 선택 (막대 / 선 / 원형)
#   - GPT 분석 설명 자동 생성
#   - 보고서 자동 저장 (.txt)
#
# ▶ 사용 목적:
#   - 기업 실무 데이터(판매/실적/매출 등) 시각화 & 해석 자동화
#   - 데이터 인사이트 도출과 보고서 작성을 동시에
#
# ▶ 기대 효과:
#   - 비전문가도 클릭 몇 번으로 데이터 분석 + 인사이트 확보
#   - GPT 활용 자동화 보고서로 보고 품질 및 생산성 향상
# -----------------------------------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import io

# 🌱 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🤖 GPT 모델 설정
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# 🎯 Streamlit 설정
st.set_page_config(page_title="📊 GPT 데이터 마스터", page_icon="🧠")
st.title("🧠 GPT 데이터 분석 통합 시스템")
st.markdown("데이터 업로드, 시각화, 인사이트, 보고서까지 한 번에!")

# 📁 엑셀 파일 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("🔍 데이터 미리보기")
    st.dataframe(df.head())

    # 📊 시각화 옵션 선택
    st.markdown("---")
    chart_type = st.selectbox("📊 시각화 종류 선택", ["바 차트", "선 차트", "원형 차트"])
    x_col = st.selectbox("🔠 X축 컬럼 선택", df.columns)
    y_col = st.selectbox("🔢 Y축 컬럼 선택", df.columns)

    # 🖼️ 시각화 실행
    if st.button("📈 시각화 및 GPT 분석"):
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

        # 💬 GPT 프롬프트 생성
        chart_prompt = PromptTemplate(
            input_variables=["x", "y", "type"],
            template="""
너는 데이터 분석가야. 다음은 사용자로부터 선택된 시각화 정보야:
- 차트 종류: {type}
- X축 항목: {x}
- Y축 항목: {y}
이 정보를 바탕으로 사용자가 어떤 인사이트를 얻을 수 있을지 간단히 요약해줘.
"""
        )
        prompt = chart_prompt.format(x=x_col, y=y_col, type=chart_type)
        gpt_response = llm.predict(prompt)

        st.markdown("🧠 **GPT 분석 결과:**")
        st.info(gpt_response)

        # 📝 보고서 저장
        report_text = f"[GPT 자동 보고서]\n차트 종류: {chart_type}\nX축: {x_col}\nY축: {y_col}\n\n[해석 결과]\n{gpt_response}"
        buffer = io.StringIO()
        buffer.write(report_text)

        st.download_button(
            label="📩 분석 보고서 다운로드",
            data=buffer.getvalue(),
            file_name="GPT_report.txt",
            mime="text/plain"
        )
