# 📄 GPT_excelInsightSaverPro.py - GPT 인사이트 저장 시스템 (Pro 버전)
# 기능:
# - 엑셀 데이터 GPT 분석
# - 인사이트 저장 + 리스트 출력 + TXT 다운로드 기능 포함

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

# 🖥️ Streamlit 설정
st.set_page_config(page_title="GPT 인사이트 저장기 Pro", page_icon="📘")
st.title("📘 GPT 인사이트 저장기 (Pro 버전)")
st.markdown("GPT 분석 결과를 저장하고 텍스트 파일로 다운로드할 수 있어요!")

# 📁 인사이트 저장 리스트 (세션 상태 사용)
if "insights" not in st.session_state:
    st.session_state.insights = []

# 📤 엑셀 파일 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📄 데이터 미리보기")
    st.dataframe(df.head())

    # 컬럼 선택
    x_col = st.selectbox("🔠 X축 컬럼", df.columns)
    y_col = st.selectbox("🔢 Y축 컬럼", df.columns)

    if st.button("🧠 GPT 분석 실행"):
        # GPT 프롬프트 구성
        prompt = PromptTemplate(
            input_variables=["x", "y"],
            template="""
            너는 데이터 분석가야. 다음 두 컬럼을 분석해줘:
            - X축: {x}
            - Y축: {y}
            간결하고 직관적인 분석 결과를 작성해줘.
            """
        ).format(x=x_col, y=y_col)

        gpt_result = llm.predict(prompt)

        st.markdown("### 🧠 GPT 분석 결과")
        st.info(gpt_result)

        # 저장 버튼
        if st.button("💾 인사이트 저장"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result_text = f"[{now}] 🔹 {x_col} vs {y_col} → {gpt_result}"
            st.session_state.insights.append(result_text)
            st.success("✅ 인사이트 저장 완료!")

# 저장된 인사이트 리스트 출력 및 선택
if st.session_state.insights:
    st.markdown("---")
    st.subheader("📚 저장된 인사이트")
    selected = st.selectbox("🔍 저장된 인사이트 선택", st.session_state.insights[::-1])
    st.text_area("📋 인사이트 내용", selected, height=100)

    # 다운로드 버튼
    if st.button("📩 인사이트 TXT로 다운로드"):
        txt_data = "\n".join(st.session_state.insights)
        st.download_button(
            label="📥 다운로드 (GPT_saved_insights.txt)",
            data=txt_data,
            file_name="GPT_saved_insights.txt",
            mime="text/plain"
        )

# 실행 명령어:
# streamlit run csv_app/GPT_excel/GPT_excelInsightSaverPro.py
