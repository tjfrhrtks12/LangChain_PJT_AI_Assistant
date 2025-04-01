# 📄 GPT_excelInsightSaver.py - GPT 분석 인사이트 저장 시스템
# 기능:
# - 엑셀 데이터 시각화 및 GPT 분석 결과를 저장
# - 저장된 인사이트 목록 관리 및 선택 출력
# - 텍스트 파일로 다운로드 기능

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from io import StringIO
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# 🌱 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🤖 GPT 모델 세팅
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2)

# 📁 인사이트 저장 리스트
insight_list = []

# 🖥️ Streamlit 기본 설정
st.set_page_config(page_title="GPT 인사이트 저장기", page_icon="🧠")
st.title("🧠 GPT 분석 인사이트 저장기")

# 📤 엑셀 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    # 📊 분석할 X, Y 컬럼 선택
    x_col = st.selectbox("🔠 X축 컬럼 선택", df.columns)
    y_col = st.selectbox("🔢 Y축 컬럼 선택", df.columns)

    if st.button("🧠 GPT 분석 실행"):
        # GPT 요약 프롬프트
        prompt = PromptTemplate(
            input_variables=["x", "y"],
            template="""
            너는 데이터 분석가야. 사용자는 다음 두 컬럼을 분석하고 싶어 해:
            - X축: {x}
            - Y축: {y}
            간결하게 핵심 인사이트를 요약해줘.
            """
        ).format(x=x_col, y=y_col)

        gpt_response = llm.predict(prompt)

        st.markdown("### 🔍 GPT 분석 결과")
        st.success(gpt_response)

        # 📝 인사이트 저장 기능
        if st.button("💾 인사이트 저장"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insight_list.append(f"[{now}] {x_col} vs {y_col} ➤ {gpt_response}")
            st.info("인사이트가 메모리에 저장되었습니다!")

# 📚 저장된 인사이트 출력
if insight_list:
    st.markdown("---")
    st.subheader("📂 저장된 인사이트")
    selected = st.selectbox("🔎 저장된 인사이트 중 선택", insight_list[::-1])
    st.text_area("💬 선택한 인사이트", value=selected, height=100)

    # 💾 텍스트 파일 다운로드
    if st.button("📥 전체 인사이트 저장 (TXT)"):
        txt_buffer = StringIO("\n".join(insight_list))
        st.download_button(
            label="📩 저장된 인사이트 다운로드",
            data=txt_buffer.getvalue(),
            file_name="GPT_saved_insights.txt",
            mime="text/plain"
        )

# ✅ 실행 명령어 (터미널)
# streamlit run csv_app/GPT_excel/GPT_excelInsightSaver.py
