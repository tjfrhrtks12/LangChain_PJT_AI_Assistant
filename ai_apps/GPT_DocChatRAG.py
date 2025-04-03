# 📚 GPT_DocChatRAG.py: GPT 기반 문서 분석 및 질의응답 시스템 (RAG)

import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# 🌱 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🚀 GPT 모델 로드
gpt_model = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model_name="gpt-3.5-turbo")

# 🌐 Streamlit 앱 설정
st.set_page_config(page_title="📖 GPT 문서 분석 시스템", page_icon="📚")
st.title("📖 GPT 문서 분석 시스템")
st.markdown("업로드된 문서를 분석하여 GPT 기반의 정확한 답변을 제공합니다.")

# 📂 파일 업로드 (TXT)
uploaded_file = st.file_uploader("📤 분석할 문서 파일을 업로드하세요", type=["txt"])

if uploaded_file:
    # 업로드된 파일을 임시로 저장
    temp_file_path = "temp_doc.txt"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # 📄 문서 로드 (경로 문제 해결)
    loader = TextLoader(temp_file_path, encoding='utf-8')
    docs = loader.load()

    # 📑 문서 분할
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(docs)

    # 🔍 벡터DB 생성
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db = FAISS.from_documents(split_docs, embeddings)

    # 🗨️ 질의응답 체인 생성
    qa = RetrievalQA.from_chain_type(llm=gpt_model, chain_type="stuff", retriever=db.as_retriever())

    # 📌 사용자 질문 입력
    question = st.text_input("🔎 문서에 관해 궁금한 점을 입력하세요")

    if st.button("🧠 GPT 분석"):
        if question:
            response = qa.run(question)
            st.success(response)
        else:
            st.error("질문을 입력해주세요!")

# 🛠 실행 명령어
# streamlit run GPT_DocChatRAG.py
