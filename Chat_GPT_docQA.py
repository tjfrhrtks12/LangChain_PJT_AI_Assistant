from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

# 🔐 API 키 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🧠 LLM + 임베딩 준비
llm = OpenAI(openai_api_key=api_key)
embedding = OpenAIEmbeddings(openai_api_key=api_key)

# 📄 문서 불러오기
loader = TextLoader("data/sample.txt", encoding='utf-8')
documents = loader.load()

# 📑 문서 분할
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# 🧠 문서 -> 벡터 저장소
db = FAISS.from_documents(docs, embedding)

# 🔄 질의 응답 체인 구성
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever()
)

# 💬 질문 루프
while True:
    query = input("성주의 문서 질문 🤖: ")
    if query.lower() in ["exit", "quit"]:
        print("문서 QA 종료합니다 👋")
        break
    result = qa.run(query)
    print("📄 문서 기반 AI:", result)

# 💡 답변부터 말하자면:
# 👉 현재 우리가 만들고 있는 문서 기반 AI 시스템은
# 🔹 문서 안의 내용만 바탕으로 답변하는 시스템이야!

# 즉, 성주가 sample.txt에 써준 내용만 보고
# 그 안에서 관련 정보를 벡터로 검색해서 답변해줘.
# → 문서에 없는 내용은 모르거나 뻔뻔하게 “없는 얘기”를 할 수도 있어! 😅

# 즉,

# 검색할 문서가 없다 → 답 못 함

# 문서에 정보가 부실하다 → GPT도 부실하게 대답함

# 문서에 거짓이 있다 → GPT도 거짓을 따라 말함 😅

