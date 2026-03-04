import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.prompts import ChatPromptTemplate
from app.config import MODEL_NAME, SYSTEM_PROMPT

load_dotenv()

def analyze_log_content(log_text):
    """로그 텍스트를 LLM에 전송하여 분석 결과 반환"""
    llm = ChatOpenAI(model=MODEL_NAME, reasoning_effort="low")

    # 로그가 너무 길 경우를 대비해 토큰 절약 (마지막 3000자만 분석, 원래는 Vector DB를 쓰거나 전체 청킹)
    truncated_log = log_text[-3000:] if len(log_text) > 3000 else log_text

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", """
        [서버 로그 데이터 (일부 발췌)]
        {log_data}
        """)
    ])

    chain = prompt | llm

    result_text = chain.invoke({"log_data": truncated_log}).content

    try:
        return json.loads(result_text)
    except:
        return {"error": "분석 실패", "raw": result_text}
