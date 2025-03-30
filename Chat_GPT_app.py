from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

# 환경변수 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# LLM 세팅
llm = OpenAI(openai_api_key=api_key)

# 사용자 입력
while True:
    user_input = input("성주의 질문 🤖:")
    if user_input.lower() in ["exit", "quit"]:
        print("종료합니다.")
        break
    response = llm(user_input)
    print("AI 어시스턴트 ✨:", response)

##########평상시의 CHAT GPT 와의 대화###########

# 실행 명령어: python Chat_GPT_app.py 