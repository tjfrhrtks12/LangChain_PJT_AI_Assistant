import streamlit as st
from dotenv import load_dotenv
import os

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

# 🔐 환경 변수 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🧠 GPT, 임베딩 모델 준비
llm = OpenAI(openai_api_key=api_key)
embedding = OpenAIEmbeddings(openai_api_key=api_key)

# 📄 문서 불러오기
loader = TextLoader("data/sample.txt", encoding="utf-8")
documents = loader.load()

# 📑 문서 분할
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# 🧠 벡터 임베딩 저장
db = FAISS.from_documents(docs, embedding)
retriever = db.as_retriever()

# 🌐 Streamlit UI 시작
st.set_page_config(page_title="📄 문서 기반 GPT", page_icon="📘")
st.title("📄 성주의 문서 기반 GPT 어시스턴트")
st.markdown("문서를 기반으로 GPT가 대답해드립니다!")

# 🤔 사용자 질문 입력
query = st.text_input("문서 기반 질문을 입력하세요 📎")

# ✅ 버튼 클릭 시 응답 실행
if st.button("질문하기"):
    if query:
        with st.spinner("문서를 분석 중입니다...📚"):
            # 문서 기반 검색
            docs = retriever.get_relevant_documents(query)
            context = "\n".join([doc.page_content for doc in docs]) if docs else "관련 문서 없음."

            # 프롬프트 구성
            prompt = f"""
            너는 문서 기반 AI야.
            아래 문서를 참고해서 질문에 최대한 정확하게 답변해줘.

            [문서]
            {context}

            [질문]
            {query}

            [답변]
            """

            # GPT 응답 생성
            response = llm(prompt)

        st.success("✅ 문서 기반 GPT의 답변:")
        st.write(response)
    else:
        st.warning("질문을 입력해 주세요!")

# 실행 명령어 : streamlit run Chat_GPT_webaDocQA.py