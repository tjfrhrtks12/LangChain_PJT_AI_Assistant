# 지금 이 코드는 업로드한 엑셀 데이터를 요약 분석해서 
# GPT가 자동으로 보고서를 생성해주는 전체 시스템입니다.
# 다른 파일과 연동될것임.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import tempfile

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# GPT 모델 설정
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# Streamlit UI 설정
st.set_page_config(page_title="📄 GPT 자동 보고서 생성기", page_icon="📝")
st.title("📄 GPT 자동 보고서 생성기")
st.markdown("엑셀 데이터 업로드 후, 분석 보고서를 자동으로 생성해보세요!")

# 파일 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📊 데이터 미리보기")
    st.dataframe(df.head())

    # 통계 요약
    st.markdown("---")
    st.subheader("📌 기본 통계 요약")
    st.dataframe(df.describe(include="all"))

    # GPT 분석 요청
    if st.button("🧠 GPT에게 보고서 생성 요청"):
        # 데이터 요약 문자열로 구성
        summary = df.describe(include="all").to_string()

        # 프롬프트 템플릿 설정
        report_prompt = PromptTemplate(
            input_variables=["summary"],
            template="""
너는 데이터 분석 전문가야. 다음은 엑셀 데이터의 통계 요약 정보야:

{summary}

이 내용을 기반으로 다음과 같은 보고서를 작성해줘:
1. 데이터 전반에 대한 개요 요약
2. 주요 수치들의 의미 분석
3. 특이값, 이상치 또는 주목할 만한 패턴
4. 추가적으로 추천할 분석 방향

각 항목은 번호를 붙여서 간결하고 명확하게 작성해줘.
"""
        )

        prompt = report_prompt.format(summary=summary)
        report = llm.predict(prompt)

        st.markdown("---")
        st.subheader("📄 GPT 분석 보고서")
        st.info(report)

        # 보고서를 txt로 저장할 수 있도록 처리
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmp_file:
            tmp_file.write(report)
            tmp_path = tmp_file.name

        with open(tmp_path, "rb") as file:
            st.download_button(
                label="📥 분석 보고서 다운로드 (.txt)",
                data=file,
                file_name="GPT_분석_보고서.txt",
                mime="text/plain"
            )
