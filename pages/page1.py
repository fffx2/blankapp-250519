import streamlit as st
import openai
from openai import OpenAI

# OpenAI 설정
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# 시스템 역할 정의
system_prompt = """
너는 웹 접근성 전문가야. 사용자가 제공하는 텍스트, 색상 정보, 또는 HTML 구조에 대해 
WCAG 2.1 기준을 기반으로 피드백을 제공해야 해. 주요 항목은 색상 대비, 텍스트 크기, 의미 구조, 
가독성, 자동 재생 등이고, 사용자의 질문에 간단하면서도 실질적인 개선점을 알려줘.
"""

# 대화 이력 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

st.title("💬 웹콘텐츠 접근성 챗봇 (WCAG 기반)")

# 사용자 입력
user_input = st.chat_input("웹 접근성 관련 질문을 입력하세요...")

# 사용자 입력 처리
if user_input:
    # 대화 이력에 추가
    st.session_state.messages.append({"role": "user", "content": user_input})

    # GPT 응답 호출
    response = client.chat.completions.create(
        model="gpt-4",
        messages=st.session_state.messages
    )

    bot_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# 전체 대화 출력
for msg in st.session_state.messages[1:]:  # system 제외
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
