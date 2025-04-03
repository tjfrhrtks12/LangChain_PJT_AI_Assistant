# 활용해보자!

# 📊 streamlit run GPT_DataMasterProPlus_Upgrade.py - 전문가형 보고서 생성기 (8단 구성 포함)

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_experimental.agents import create_pandas_dataframe_agent

# ✅ 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ GPT 모델 연결
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.3, model_name="gpt-3.5-turbo")

# ✅ 폰트 설정 (Matplotlib + PDF용)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ✅ Streamlit UI 설정
st.set_page_config(page_title="📊 GPT 전문가형 보고서", page_icon="📘")
st.title("📘 GPT 전문가형 자동 보고서 생성기")
st.markdown("엑셀 데이터를 분석하여 타이틀, 목차, 예측 및 전략까지 포함된 보고서를 자동 생성합니다.")

# ✅ 엑셀 파일 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    # 👉 숫자 컬럼 추출
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    st.markdown("---")
    chart_type = st.selectbox("📊 차트 유형", ["바 차트", "선 차트", "원형 차트"])
    x_col = st.selectbox("🔠 X축 컬럼", df.columns)
    y_col = st.selectbox("🔢 Y축 컬럼", numeric_cols)

    if st.button("📈 전문가형 보고서 생성"):
        # ✅ 시각화 생성
        fig, ax = plt.subplots()
        if chart_type == "바 차트":
            sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "선 차트":
            sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "원형 차트":
            grouped = df.groupby(x_col)[y_col].sum()
            ax.pie(grouped, labels=grouped.index, autopct="%1.1f%%")
            ax.set_ylabel("")
        st.pyplot(fig)

        # ✅ 일변량 EDA
        st.subheader("📊 일변량 EDA")
        st.dataframe(df.describe(include="all"))

        # ✅ 산점도 시각화
        st.subheader("🔗 다변량 분석 (산점도)")
        scatter_x = st.selectbox("📍 산점도 X축", numeric_cols, key="scatter_x")
        scatter_y = st.selectbox("📍 산점도 Y축", numeric_cols, key="scatter_y")
        fig2, ax2 = plt.subplots()
        sns.scatterplot(data=df, x=scatter_x, y=scatter_y, ax=ax2)
        st.pyplot(fig2)

        # ✅ GPT 프롬프트 구성
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        eda_text = df.describe().to_string()

        prompt = PromptTemplate(
            input_variables=["chart", "x", "y", "eda", "sx", "sy", "timestamp"],
            template="""
📘 GPT 전문가형 분석 보고서

1. 📌 보고서 타이틀  
   - 생성일시: {timestamp}

2. 📚 목차  
   1. 데이터 개요  
   2. 시각화 분석  
   3. 관계 분석  
   4. 인사이트 요약  
   5. 미래 예측  
   6. 개선 방안  
   7. 결론 요약  

3. 📊 데이터 개요  
- 주요 통계값 요약:  
{eda}

4. 📈 시각화 분석  
- 차트 유형: {chart}  
- X축: {x}, Y축: {y}

5. 🔗 관계 분석 (산점도)  
- 비교 항목: {sx} vs {sy}  
- 상관 및 경향성 해석

6. 💡 인사이트 요약  
- 주요 수치 또는 경향성 기반 핵심 요약

7. 🔮 미래 예측 분석  
- 트렌드 기반 향후 전망 예측  
- 중요 KPI 예측 또는 변화 예상

8. 🛠 개선 방안 및 전략  
- 실무자가 바로 적용 가능한 전략 제시  
- 개선 포인트, 주의사항 포함

9. 📌 결론 요약  
- 전체 요약 및 의사결정 지원 포인트 정리
"""
        ).format(chart=chart_type, x=x_col, y=y_col, eda=eda_text, sx=scatter_x, sy=scatter_y, timestamp=now)

        gpt_report = llm.predict(prompt)

        # ✅ PDF 저장
        pdf_path = f"GPT_Expert_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("batang", fname="./csv_app/fonts/batang.ttc", uni=True)
        pdf.set_font("batang", size=12)
        pdf.multi_cell(0, 10, gpt_report)
        pdf.output(pdf_path)

        st.success("📄 전문가형 보고서(PDF) 저장 완료!")
        with open(pdf_path, "rb") as f:
            st.download_button("📥 PDF 다운로드", data=f, file_name=pdf_path)

    # 💬 질문 기반 분석
    st.markdown("---")
    st.subheader("💬 질문 기반 분석")
    question = st.text_input("궁금한 분석 질문을 입력하세요:")
    if st.button("🔍 GPT 분석 실행"):
        agent = create_pandas_dataframe_agent(llm, df, verbose=False, allow_dangerous_code=True)
        st.info(agent.run(question))

# ✅ 실행 명령어
# streamlit run GPT_DataMasterProPlus_Upgrade.py
