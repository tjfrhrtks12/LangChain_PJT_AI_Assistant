# translator.py (openai 최신 버전용)
import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 입력 언어 자동 감지
def detect_language(text):
    if all(ord(c) < 128 for c in text):
        return "en"
    else:
        return "ko"

# GPT로 번역 수행
def translate_with_gpt(text):
    src_lang = detect_language(text)
    dest_lang = "en" if src_lang == "ko" else "ko"
    prompt = f"다음 문장을 '{dest_lang}' 언어로 번역해줘:\n\n{text}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# 메인 실행 루프
if __name__ == "__main__":
    while True:
        user_input = input("번역할 문장을 입력하세요 (종료: q): ")
        if user_input.lower() == 'q':
            break

        translated = translate_with_gpt(user_input)
        print(f"👉 번역 결과: {translated}\n")
