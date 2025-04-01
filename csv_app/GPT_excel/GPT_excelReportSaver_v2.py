# 📄 보고서 자동 저장 + 다운로드 개선 코드
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from io import BytesIO
from datetime import datetime

# 🌱 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🤖 GPT 모델 설정
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# 🖥️ Streamlit UI 설정
st.set_page_config(page_title="📊 GPT 엑셀 자동 보고서 저장기", page_icon="📥")
st.title("📥 GPT 자동 보고서 생성기 (개선판)")
st.markdown("엑셀 데이터를 분석하여 GPT가 자동 보고서를 작성하고 다운로드까지 도와줍니다!")

# 📁 엑셀 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    st.markdown("---")
    chart_type = st.selectbox("📊 시각화 유형", ["바 차트", "선 차트", "원형 차트"])
    x_col = st.selectbox("🔠 X축 컬럼", df.columns)
    y_col = st.selectbox("🔢 Y축 컬럼", df.columns)

    if st.button("📈 분석 및 보고서 생성"):
        # 📊 시각화
        fig, ax = plt.subplots()
        if chart_type == "바 차트":
            sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "선 차트":
            sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
        elif chart_type == "원형 차트":
            df_grouped = df.groupby(x_col)[y_col].sum()
            ax.pie(df_grouped, labels=df_grouped.index, autopct="%1.1f%%")
            ax.set_ylabel("")

        st.pyplot(fig)

        # 🔮 GPT 해석
        prompt_template = PromptTemplate(
            input_variables=["x", "y", "type"],
            template="""
            너는 데이터 분석가야. 다음은 사용자로부터 선택된 시각화 정보야:
            - 차트 종류: {type}
            - X축: {x}
            - Y축: {y}
            위 내용을 바탕으로 유의미한 분석 내용을 간단히 알려줘!
            """
        )
        prompt = prompt_template.format(x=x_col, y=y_col, type=chart_type)
        gpt_result = llm.predict(prompt)

        # 📝 보고서 저장 (줄바꿈 포함)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_text = f"""[GPT 보고서 생성 일시: {now}]

차트 종류: {chart_type}
X축: {x_col}
Y축: {y_col}

[분석 요약]
{gpt_result}
"""
        report_filename = f"GPT_Report_{now}.txt"

        buffer = BytesIO()
        buffer.write(report_text.encode("utf-8"))
        buffer.seek(0)

        # 💾 저장 안내
        st.success("✅ 보고서 생성 완료!")
        st.download_button("📩 텍스트 보고서 다운로드", data=buffer, file_name=report_filename, mime="text/plain")

        st.markdown("---")
        st.markdown(f"📎 **파일명**: `{report_filename}`")
        st.markdown(f"🧠 **GPT 요약:** {gpt_result}")
