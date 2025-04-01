# ✅ 목표
# 📂 엑셀 파일 업로드
# 💬 질문 입력
# 🤖 GPT가 엑셀 내용을 읽고 답변!


# ✅ 기능 흐름
# 1.엑셀 업로드
# 2.Pandas로 엑셀 → 데이터프레임 변환
# 3.전체 데이터를 텍스트로 변환
# 4.사용자가 질문 입력
# 5.GPT가 답변 생성 (문서 기반 추론처럼)

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document

# 환경변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# GPT 모델 준비
llm = ChatOpenAI(openai_api_key=api_key)
chain = load_qa_chain(llm, chain_type="stuff")

# 웹 페이지 설정
st.set_page_config(page_title="📊 엑셀 GPT 분석", page_icon="📁")
st.title("📊 엑셀 기반 GPT 분석 어시스턴트")
st.markdown("엑셀 파일을 업로드하고 질문하면 GPT가 답해줘요!")

# 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

# 사용자 질문 입력
question = st.text_input("엑셀 데이터에 대해 궁금한 점을 입력하세요 🤔")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)

    # GPT에 넘길 텍스트로 변환
    full_text = df.to_csv(index=False)
    doc = Document(page_content=full_text)

    if question:
        with st.spinner("답변 생성 중... 🤖"):
            result = chain.run(input_documents=[doc], question=question)
            st.success("GPT의 답변:")
            st.write(result)

# 실행 명령어 : streamlit run csv_app/Chat_GPT_excelQA_QA.py
