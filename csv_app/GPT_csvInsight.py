import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
import os
import io

# ✅ 한글 깨짐 방지
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 🔐 OpenAI API Key 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=api_key)

# 🌐 페이지 설정
st.set_page_config(page_title="CSV 자동 분석 GPT", page_icon="📈")
st.title("📈 성주의 GPT 데이터 분석가")
st.markdown("CSV 업로드 → 자동 그래프 생성 → GPT가 그래프 해석까지!")

# 📁 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 데이터 미리보기")
    st.dataframe(df)

    # 🎯 시각화: 단가 vs 판매량
    st.subheader("📊 단가 vs 판매량 산점도")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="단가", y="판매량", hue="제품명", s=100, ax=ax)
    plt.title("제품별 단가 vs 판매량")
    st.pyplot(fig)

    # 🧠 GPT에게 그래프 해석 요청
    # 📌 그래프 요약용 데이터를 문자열로 추출
    description_text = df.describe(include='all').to_string()
    head_text = df.head().to_string()

    st.subheader("🧠 GPT의 그래프 해석")

    gpt_prompt = f"""
    아래는 제품 판매 기록입니다. 데이터 요약과 미리보기 정보를 참고해서,
    '단가'와 '판매량'의 관계를 중심으로 그래프를 해석해줘.
    제품별 특징도 분석해서 설명해줘.

    [데이터 요약]
    {description_text}

    [데이터 미리보기]
    {head_text}

    친절하고 분석적으로 설명해줘.
    """

    with st.spinner("GPT가 그래프를 해석하는 중입니다...🧠"):
        response = llm(gpt_prompt)

    st.success("✅ 해석 결과:")
    st.write(response)

else:
    st.info("📁 CSV 파일을 먼저 업로드해주세요.")

##실행명령어 : streamlit run csv_app/Chat_GPT_csvInsight.py
