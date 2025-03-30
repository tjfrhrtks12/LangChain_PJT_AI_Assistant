from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

# 🔐 API 키
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 모델 설정
llm = OpenAI(openai_api_key=api_key)
embedding = OpenAIEmbeddings(openai_api_key=api_key)

# 문서 불러오기 및 분할
loader = TextLoader("data/sample.txt", encoding='utf-8')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# 벡터 저장소
db = FAISS.from_documents(docs, embedding)
retriever = db.as_retriever()

# 💬 질의 루프
while True:
    query = input("성주의 하이브리드 질문 🤖: ")
    if query.lower() in ["exit", "quit"]:
        print("AI 종료합니다 👋")
        break

    # 1. 문서에서 관련 정보 찾기
    docs = retriever.get_relevant_documents(query)

    # 2. 관련 문서 내용 추출 (없으면 빈 문자열)
    doc_context = "\n".join([doc.page_content for doc in docs]) if docs else "문서에 해당 정보 없음."

    # 3. 프롬프트 생성 (문서 + 질문 같이 전달)
    prompt = f"""
    너는 똑똑한 AI야. 아래는 참고 문서이고, 아래 질문에 답해야 해.
    문서에 관련 내용이 있으면 문서를 기반으로, 없으면 네 일반 지식으로 대답해줘.

    [문서 내용]
    {doc_context}

    [질문]
    {query}

    [답변]
    """

    # 4. GPT에 전달
    answer = llm(prompt)
    print("🧠 하이브리드 AI:", answer)
