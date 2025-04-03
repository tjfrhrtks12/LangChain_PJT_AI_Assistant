# 활용해보자!!

# 📊 GPT_PortfolioSlideGenerator.py 
# - 프로젝트 발표자료 자동 생성기

import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from datetime import datetime
from io import BytesIO

# 🌱 환경변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🤖 GPT 연결
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.3, model_name="gpt-3.5-turbo")

# 🌐 Streamlit UI
st.set_page_config(page_title="📊 발표자료 생성기", page_icon="🖼️")
st.title("🖼️ GPT 기반 포트폴리오 발표자료 생성기")
st.markdown("분석 프로젝트 개요를 입력하면 GPT가 슬라이드 형태의 발표자료를 자동 생성해드립니다!")

# 📥 사용자 입력
project_title = st.text_input("📌 프로젝트 제목", value="GPT 기반 데이터 통합 분석 시스템")
objective = st.text_area("🎯 프로젝트 목적", placeholder="이 프로젝트의 목적은 무엇인가요?")
tech_stack = st.text_area("🛠️ 사용 기술", placeholder="Streamlit, Pandas, LangChain, GPT 등...")
highlight = st.text_area("📈 핵심 성과 / 인사이트", placeholder="성과 요약 or 자동화된 분석 사례 등...")

if st.button("📑 발표자료 생성"):
    with st.spinner("GPT가 발표자료를 정리 중입니다..."):

        # 프롬프트 구성
        slide_prompt = PromptTemplate(
            input_variables=["title", "goal", "stack", "highlight"],
            template="""
너는 발표 전문가야. 아래는 발표할 GPT 프로젝트 정보야:

[제목]: {title}
[목적]: {goal}
[기술]: {stack}
[성과]: {highlight}

이 정보를 바탕으로 슬라이드 형식의 발표자료를 6~8페이지 정도로 요약해줘.
각 슬라이드는 제목과 간단한 본문으로 구성해줘.
"""
        ).format(title=project_title, goal=objective, stack=tech_stack, highlight=highlight)

        slides = llm.predict(slide_prompt)

        st.subheader("📋 발표자료 요약 결과")
        st.markdown("슬라이드 형식 요약:")
        st.code(slides)

        # 📩 저장 기능
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"GPT_Presentation_{now}.txt"

        buffer = BytesIO()
        buffer.write(slides.encode("utf-8"))
        buffer.seek(0)

        st.download_button("📥 발표자료 다운로드 (TXT)", data=buffer, file_name=file_name, mime="text/plain")

#실행 명령어 :  streamlit run GPT_DataMasterProExpert.py