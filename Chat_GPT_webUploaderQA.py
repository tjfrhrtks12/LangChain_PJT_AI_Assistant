import streamlit as st
from dotenv import load_dotenv
import os

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

import tempfile

# 🔐 API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(openai_api_key=api_key)
embedding = OpenAIEmbeddings(openai_api_key=api_key)

# 🌐 웹 UI
st.set_page_config(page_title="📎 업로드 문서 GPT", page_icon="📄")
st.title("📎 성주의 업로드 문서 GPT 챗봇")
st.markdown("파일을 업로드하고 질문하면, GPT가 문서 내용 기반으로 대답해줍니다!")

# 📁 파일 업로드
uploaded_file = st.file_uploader("문서를 업로드하세요 (.txt)", type=["txt"])

if uploaded_file is not None:
    # 📄 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    # 📑 문서 로딩 & 분할
    loader = TextLoader(tmp_file_path, encoding='utf-8')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # 🧠 벡터 임베딩
    db = FAISS.from_documents(docs, embedding)
    retriever = db.as_retriever()

    # 💬 사용자 질문
    query = st.text_input("문서 기반 질문을 입력하세요 📎")

    if st.button("질문하기"):
        if query:
            with st.spinner("문서를 분석 중입니다...📚"):
                matched_docs = retriever.get_relevant_documents(query)
                context = "\n".join([doc.page_content for doc in matched_docs]) if matched_docs else "문서에서 찾을 수 없음."

                # 🧠 프롬프트 생성
                prompt = f"""
                아래 문서를 참고해서 질문에 답변해줘.
                문서에 없으면 모른다고 말해줘.

                [문서 내용]
                {context}

                [질문]
                {query}

                [답변]
                """

                response = llm(prompt)
            st.success("✅ GPT의 답변:")
            st.write(response)
        else:
            st.warning("질문을 입력해 주세요!")
else:
    st.info("문서를 먼저 업로드해 주세요.")
