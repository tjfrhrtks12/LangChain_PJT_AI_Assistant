##질문형 GPT

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from langchain.llms import OpenAI
import os

# 환경변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=api_key)

st.set_page_config(page_title="CSV 분석 GPT", page_icon="📊")
st.title("📊 성주의 CSV 기반 GPT 어시스턴트")
st.markdown("CSV 데이터를 업로드하고 질문하면 GPT가 답변해줘요!")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 업로드한 데이터 미리보기")
    st.dataframe(df)

    # GPT에게 넘길 CSV 요약
    df_summary = df.describe(include='all').to_string()
    df_head = df.head().to_string()

    # 질문 입력
    user_input = st.text_input("CSV에 대해 궁금한 점을 입력하세요 🤔")

    if st.button("질문하기"):
        if user_input:
            prompt = f"""
            아래는 판매 기록이 담긴 표입니다.

            [데이터 요약]
            {df_summary}

            [데이터 일부 미리보기]
            {df_head}

            사용자의 질문:
            {user_input}

            위 표를 참고해서, 질문에 대해 정확하고 분석적으로 답변해주세요.
            """

            with st.spinner("분석 중입니다...📊"):
                response = llm(prompt)

            st.success("✅ GPT의 답변:")
            st.write(response)
        else:
            st.warning("질문을 입력해 주세요!")
else:
    st.info("먼저 CSV 파일을 업로드 해주세요.")

#실행 명령어 : streamlit run csv_app/Chat_GPT_csvQA.py

#용도 예시
# 🔥 1. 판매/재고/마케팅 데이터 분석
# 활용 예시	질문 예시
# 🛒 판매기록 분석	"가장 많이 팔린 제품은 뭐야?"
# 📦 재고 모니터링	"머스탱은 몇 대 팔렸고 평균 단가는 얼마야?"
# 💰 수익성 확인	"총 판매량과 총 매출액은?"
# ➡ 기업 내부 엑셀(CSV) 파일 업로드만 하면 분석됨!

# 🔍 2. 연구 실험 데이터 요약
# 활용 예시	질문 예시
# 🧪 실험 결과 요약	"이 실험에서 평균 값은 어떻게 돼?"
# 📉 측정값 비교	"가장 높은 수치는 몇이고 언제야?"
# 🧠 데이터 품질 확인	"이상치로 보이는 값이 있니?"
# ➡ CSV로 저장된 실험결과 파일을 넣기만 하면 분석됨!

# 👥 3. 비개발자용 AI 분석툴 제공
# 성주의 시스템은 엑셀만 다룰 줄 알면 누구나 AI 분석 가능!

# 기획자, 마케터, 경영진에게 분석툴 제공

# 사용자는 데이터만 넣고 질문만 하면 OK

# "AI 분석 비서"처럼 사용 가능함
#
