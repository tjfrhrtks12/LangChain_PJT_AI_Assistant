import streamlit as st
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=api_key)

# 웹 UI 설정
st.set_page_config(page_title="성주의 GPT 챗봇", page_icon="🤖")
st.title("📘 성주의 GPT 어시스턴트")
st.markdown("GPT에게 무엇이든 물어보세요!")

# 사용자 입력 받기
user_input = st.text_input("질문을 입력하세요 🤔")

# 버튼을 눌렀을 때만 실행
if st.button("질문하기"):
    if user_input:
        with st.spinner("생각 중...🧠"):
            response = llm(user_input)
        st.success("✨ GPT의 답변:")
        st.write(response)
    else:
        st.warning("질문을 입력해 주세요!")

#실행 명령어 : streamlit run Chat_GPT_webQa.py
