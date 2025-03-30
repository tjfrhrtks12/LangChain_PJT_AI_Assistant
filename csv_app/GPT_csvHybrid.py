# 📁 CSV 업로드    	    유저가 데이터 업로드
# 📊 자동 시각화	    단가 vs 판매량 그래프 표시
# 🧠 GPT 자동 해석	    그래프 요약 자동 생성
# 💬 사용자 질문 응답	추가 질문 시 GPT가 데이터 기반 답변

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
import os

# ✅ 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 🔐 API 키 로딩
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=api_key)

# 🌐 페이지 설정
st.set_page_config(page_title="CSV 통합 GPT 분석기", page_icon="🧠")
st.title("🧠 성주의 GPT CSV 분석기")
st.markdown("CSV를 업로드하면 그래프도 그리고 GPT가 설명도 해주고, 질문도 받아요!")

# 📁 CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 데이터 미리보기")
    st.dataframe(df)

    # 📊 자동 시각화
    st.subheader("📈 단가 vs 판매량 산점도")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="단가", y="판매량", hue="제품명", s=100, ax=ax)
    plt.title("제품별 단가 vs 판매량")
    st.pyplot(fig)

    # 🧠 GPT 자동 해석
    st.subheader("📌 GPT의 해석 결과")
    description = df.describe(include='all').to_string()
    head_data = df.head().to_string()

    auto_prompt = f"""
    아래는 제품 판매 데이터입니다.
    [데이터 요약]
    {description}

    [데이터 미리보기]
    {head_data}

    단가와 판매량의 관계를 분석하고, 제품별 특징을 알려줘.
    """
    with st.spinner("GPT가 자동 해석 중..."):
        auto_response = llm(auto_prompt)
    st.success("✅ 자동 해석 결과:")
    st.write(auto_response)

    # 💬 사용자 질문 입력
    st.subheader("💬 궁금한 걸 GPT에게 물어보세요!")
    user_question = st.text_input("질문 입력 (예: 가장 많이 팔린 제품은?)")

    if st.button("질문하기"):
        if user_question:
            full_prompt = f"""
            아래는 제품 판매 데이터입니다.

            [데이터 요약]
            {description}

            [데이터 미리보기]
            {head_data}

            사용자 질문:
            {user_question}

            데이터 기반으로 정리해서 설명해줘.
            """
            with st.spinner("GPT가 생각 중입니다..."):
                answer = llm(full_prompt)
            st.success("💬 GPT의 답변:")
            st.write(answer)
        else:
            st.warning("질문을 입력해 주세요.")
else:
    st.info("먼저 CSV 파일을 업로드해 주세요.")

#실행 방법 : streamlit run csv_app/Chat_GPT_csvHybrid.py
