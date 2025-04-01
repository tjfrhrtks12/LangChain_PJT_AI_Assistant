##CSV파일을 분석해서 그래프로 표현한다.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from dotenv import load_dotenv
from langchain.llms import OpenAI
import os

# ✅ 한글 폰트 설정 (Windows 기준)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

# 🌍 환경 변수 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=api_key)

# 🌐 웹 UI 설정
st.set_page_config(page_title="CSV 시각화 GPT", page_icon="📊")
st.title("📊 단가 vs 판매량 산점도")
st.markdown("CSV 데이터를 업로드하고 GPT에게 질문하고, 자동 시각화도 확인해보세요!")

# 📁 CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 🔎 데이터 읽기
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 데이터 미리보기")
    st.dataframe(df)

    # 📈 시각화
    st.subheader("📊 단가 vs 판매량 산점도")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="단가", y="판매량", hue="제품명", s=100, ax=ax)
    plt.title("제품별 단가 vs 판매량")
    st.pyplot(fig)

    # 💬 GPT 질문
    df_summary = df.describe(include='all').to_string()
    df_head = df.head().to_string()
    user_input = st.text_input("GPT에게 질문해보세요 🤖")

    if st.button("질문하기"):
        if user_input:
            prompt = f"""
            아래는 제품 판매 기록이 담긴 데이터입니다.

            [데이터 요약]
            {df_summary}

            [데이터 미리보기]
            {df_head}

            사용자의 질문:
            {user_input}

            위 데이터를 참고해서, 친절하고 분석적인 답변을 해줘.
            """
            with st.spinner("GPT가 분석 중입니다...🧠"):
                response = llm(prompt)

            st.success("✅ GPT의 답변:")
            st.write(response)
        else:
            st.warning("질문을 입력해 주세요.")
else:
    st.info("먼저 CSV 파일을 업로드해주세요.")


#실행 명령어 : streamlit run csv_app/Chat_GPT_csvViz.py