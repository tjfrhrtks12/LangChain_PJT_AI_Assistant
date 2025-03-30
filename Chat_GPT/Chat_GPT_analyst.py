from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# 🔐 환경변수 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🤖 LLM 설정
llm = OpenAI(openai_api_key=api_key)

# 📊 역할 프롬프트: 데이터 분석가로 행동
prompt = PromptTemplate(
    input_variables=["question"],
    template="""
    너는 데이터 분석가이며, 사용자 질문에 분석적이고 논리적인 방식으로 대답한다.
    필요한 경우 통계 지표, 그래프 추천, 데이터 전처리 기법도 함께 설명하라.

    질문: {question}
    답변:
    """
)

# 💬 대화 루프
while True:
    user_input = input("성주의 질문 (데이터 분석) 🤖: ")
    if user_input.lower() in ["exit", "quit"]:
        print("분석가 AI 종료합니다 👋")
        break
    full_prompt = prompt.format(question=user_input)
    response = llm(full_prompt)
    print("📊 분석가 AI:", response)

#실행 명령어  python Chat_GPT_analyst.py
