# 📊 GPT 기반 엑셀 질문 분석 + 인사이트 저장 시스템
# 엑셀 업로드 → 질문 입력 → GPT 분석 → 분석 결과 저장까지 가능한 고급 시스템입니다.

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent

# 🌱 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🤖 LLM 설정
llm = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo", temperature=0)

# 🖥️ Streamlit 앱 설정
st.set_page_config(page_title="📌 GPT 엑셀 인사이트 저장기", page_icon="📌")
st.title("📌 GPT 엑셀 질문 분석기 + 인사이트 저장")
st.markdown("엑셀 데이터를 분석하고 궁금한 점을 질문해보세요! GPT가 인사이트를 추출하고 저장까지 도와줍니다.")

# 📤 엑셀 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📄 데이터 미리보기")
    st.dataframe(df.head())

    # 질문 입력
    question = st.text_input("❓ 궁금한 점을 질문해보세요")

    if st.button("🔍 분석 및 인사이트 저장"):
        # 🧠 LangChain Agent 생성
        agent = create_pandas_dataframe_agent(llm, df, verbose=True)
        response = agent.run(question)

        # 📎 인사이트 저장
        insight_filename = "GPT_Insight_Result.txt"
        with open(insight_filename, "a", encoding="utf-8") as f:
            f.write(f"[질문]\n{question}\n[GPT 응답]\n{response}\n\n")

        st.success("✅ GPT 분석 및 인사이트 저장 완료!")
        st.markdown("🧠 **GPT 응답 결과:**")
        st.info(response)

        with open(insight_filename, "rb") as f:
            st.download_button("📥 인사이트 다운로드", f, file_name=insight_filename)

# ✅ 실행 명령어 (터미널에 입력)
# streamlit run GPT_excelInsightSaver.py
