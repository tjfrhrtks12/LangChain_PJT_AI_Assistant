# 📄 GPT_excelInsightQA.py - 질문 기반 GPT 분석 + 인사이트 저장기
# 기능:
# - 엑셀 데이터 기반 GPT 질문 응답
# - 사용자가 질문 → GPT가 답변 → 인사이트 저장 및 다운로드

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from io import StringIO
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# 🌱 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🤖 GPT 모델 연결
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2)

# 🖥️ Streamlit 설정
st.set_page_config(page_title="GPT 질문 인사이트 저장기", page_icon="💬")
st.title("💬 GPT 질문 기반 분석 & 인사이트 저장기")
st.markdown("엑셀 데이터를 기반으로 자유롭게 질문하고, 답변을 저장할 수 있어요!")

# 세션 상태 초기화
if "qa_insights" not in st.session_state:
    st.session_state.qa_insights = []

# 📁 엑셀 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    # 질문 입력
    question = st.text_input("❓ GPT에게 질문하세요")

    if st.button("🔍 분석 실행") and question:
        # LangChain Pandas Agent 실행
        agent = create_pandas_dataframe_agent(
            llm, df,
            verbose=False,
            agent_type="openai-tools",
            handle_parsing_errors=True,
            allow_dangerous_code=True
        )
        answer = agent.run(question)

        st.markdown("### 🧠 GPT의 답변")
        st.success(answer)

        # 인사이트 저장 버튼
        if st.button("💾 이 인사이트 저장"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted = f"[{now}] 질문: {question}\n→ 답변: {answer}"
            st.session_state.qa_insights.append(formatted)
            st.success("인사이트가 저장되었습니다!")

# 저장된 Q&A 인사이트 출력 및 다운로드
if st.session_state.qa_insights:
    st.markdown("---")
    st.subheader("📚 저장된 질문/답변 인사이트")
    selected = st.selectbox("🔎 인사이트 선택", st.session_state.qa_insights[::-1])
    st.text_area("📄 내용", selected, height=150)

    if st.button("📥 전체 저장된 인사이트 다운로드"):
        txt_data = "\n\n".join(st.session_state.qa_insights)
        st.download_button(
            label="📩 다운로드 (GPT_QA_insights.txt)",
            data=txt_data,
            file_name="GPT_QA_insights.txt",
            mime="text/plain"
        )

# ✅ 실행 명령어:
# streamlit run csv_app/GPT_excel/GPT_excelInsightQA.py
