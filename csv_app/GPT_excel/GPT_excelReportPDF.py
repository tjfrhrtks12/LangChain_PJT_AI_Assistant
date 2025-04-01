# 📄 GPT 기반 엑셀 자동 PDF 보고서 생성기 (날짜 정리 + X축 겹침 개선버전)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from fpdf import FPDF
from datetime import datetime

# 🌱 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🤖 GPT 모델 설정
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# 🖥️ Streamlit UI 설정
st.set_page_config(page_title="📑 GPT PDF 보고서 생성기", page_icon="📄")
st.title("📄 GPT PDF 자동 보고서 생성기")
st.markdown("엑셀 데이터를 시각화하고 GPT가 인사이트를 분석해 PDF 보고서를 생성합니다!")

# 📁 엑셀 파일 업로드
uploaded_file = st.file_uploader("📂 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    # 🎨 시각화 옵션 선택
    chart_type = st.selectbox("📊 시각화 유형 선택", ["바 차트", "선 차트", "원형 차트"])
    x_col = st.selectbox("🔠 X축 컬럼", df.columns)
    y_col = st.selectbox("🔢 Y축 컬럼", df.columns)

    if st.button("📈 시작 + GPT 분석 + PDF 저장"):
        # 📅 날짜 포맷 처리 (선택적으로 적용)
        if '일' in x_col or '날짜' in x_col:
            try:
                df[x_col] = pd.to_datetime(df[x_col])
                df[x_col] = df[x_col].dt.strftime("%Y-%m-%d")
            except Exception:
                pass

        # 📊 차트 생성 및 저장
        fig, ax = plt.subplots()
        if chart_type == "바 차트":
            sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "선 차트":
            sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "원형 차트":
            df_grouped = df.groupby(x_col)[y_col].sum()
            ax.pie(df_grouped, labels=df_grouped.index, autopct="%1.1f%%")
            ax.set_ylabel("")

        # ⬅️ X축 글자 겹침 방지
        plt.xticks(rotation=45)
        chart_img_path = "chart.png"
        plt.tight_layout()
        plt.savefig(chart_img_path)

        # 🔮 GPT 분석
        prompt_template = PromptTemplate(
            input_variables=["x", "y", "type"],
            template="""
너는 데이터 분석가야. 아래는 시각화 조건이야:
- 차트 종류: {type}
- X축 항목: {x}
- Y축 항목: {y}
이 정보를 바탕으로 분석 요약을 간단히 해줘.
"""
        )
        prompt = prompt_template.format(x=x_col, y=y_col, type=chart_type)
        gpt_result = llm.predict(prompt)

        # 📝 PDF 저장
        pdf = FPDF()
        pdf.add_font("Nanum", "", "csv_app/fonts/NanumGothic-Regular.ttf", uni=True)
        pdf.set_font("Nanum", size=12)
        pdf.add_page()

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf.cell(200, 10, f"[GPT 자동 보고서 생성 시간: {now}]", ln=True)
        pdf.cell(200, 10, f"차트 유형: {chart_type}", ln=True)
        pdf.cell(200, 10, f"X축: {x_col}", ln=True)
        pdf.cell(200, 10, f"Y축: {y_col}", ln=True)

        pdf.ln(10)
        pdf.set_font("Nanum", size=11)
        pdf.multi_cell(0, 10, "[GPT 분석 결과]\n" + gpt_result)

        pdf.image(chart_img_path, x=10, w=180)
        pdf_path = f"GPT_Report_{now}.pdf"
        pdf.output(pdf_path)

        st.success("✅ PDF 보고서가 성공적으로 저장되었습니다!")
        with open(pdf_path, "rb") as f:
            st.download_button("📩 PDF 다운로드", f, file_name=pdf_path, mime="application/pdf")

# ▶ 실행 명령어 (터미널에서 입력)
# streamlit run csv_app/GPT_excel/GPT_excelReportPDF.py
