# ✅ 우리가 지금 목표로 하는 기능
# 엑셀 데이터 업로드 → 사용자가 질문 입력
# → GPT가 엑셀 내용을 읽고 자연어로 분석 결과를 답변! 🤖💬

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document

# 환경 변수 로딩
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# GPT 모델 초기화
llm = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo")
chain = load_qa_chain(llm, chain_type="stuff")

# Streamlit 설정
st.set_page_config(page_title="📊 GPT 분석", page_icon="📈")
st.title("🧠 더존비즈온 Q4 GPT 데이터 분석기")
st.markdown("엑셀 파일 업로드 후 질문하면 GPT가 답해줘요!")

# 파일 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일 업로드", type=["xlsx"])
question = st.text_input("🤔 궁금한 점을 입력해 주세요")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df.head())

    # 💡 데이터 요약을 위해 일부 행만 텍스트로 변환
    short_df = df.head(100)  # 필요한 만큼 조정 가능
    full_text = short_df.to_csv(index=False)
    doc = Document(page_content=full_text)

    if question:
        with st.spinner("GPT가 분석 중입니다..."):
            result = chain.run(input_documents=[doc], question=question)
            st.success("✅ GPT의 답변:")
            st.write(result)

# 실행 명령어 : streamlit run csv_app/Chat_GPT_excelQA_Q4.py

# 💡 질문 예시

# 가장 많이 팔린 제품은?	AIX Pro입니다 (예시)
# 평균 단가는 얼마인가요?	약 91,200원
# 영업1팀은 어디서 많이 팔았나요?	주로 부산, 대전 등
# 단가가 높은 제품 중 판매량도 높은 건?	AIX Enterprise 등