import streamlit as st
import re
import textstat
from PIL import ImageColor

# ------------------------------
# WCAG 색상 대비 계산 함수
# ------------------------------
def luminance(rgb):
    r, g, b = [x/255.0 for x in rgb]
    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

def contrast_ratio(fg_hex, bg_hex):
    fg_rgb = ImageColor.getrgb(fg_hex)
    bg_rgb = ImageColor.getrgb(bg_hex)
    L1 = luminance(fg_rgb)
    L2 = luminance(bg_rgb)
    ratio = (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)
    return round(ratio, 2)

# ------------------------------
# 글자 크기 권장 여부 (기본값 16px)
# ------------------------------
def is_font_size_accessible(size_px):
    return size_px >= 16

# ------------------------------
# 가독성 점검 함수
# ------------------------------
def readability_score(text):
    score = textstat.flesch_reading_ease(text)
    level = ""
    if score >= 70:
        level = "쉬운 수준 (초등학생 이상)"
    elif 50 <= score < 70:
        level = "보통 수준 (중학생 이상)"
    else:
        level = "어려운 수준 (고등학생 이상)"
    return score, level

# ------------------------------
# Streamlit UI 시작
# ------------------------------
st.set_page_config(page_title="WCAG 텍스트 피드백 시스템", layout="wide")
st.title("🧪 웹 콘텐츠 접근성 피드백 시스템 (WCAG 기반)")

st.markdown("WCAG 2.1 기준에 따라 텍스트의 접근성 여부를 자동으로 점검합니다.")

col1, col2 = st.columns(2)
with col1:
    text = st.text_area("✔️ 분석할 텍스트 입력", height=200)
    text_type = st.selectbox("텍스트 유형", ["본문", "제목", "링크", "버튼"])
    font_size = st.slider("글자 크기 (px)", 10, 30, 16)

with col2:
    fg_color = st.color_picker("텍스트 색상", "#000000")
    bg_color = st.color_picker("배경 색상", "#FFFFFF")

# ------------------------------
# 분석 버튼
# ------------------------------
if st.button("✅ 접근성 분석하기"):
    if not text.strip():
        st.warning("텍스트를 입력해주세요.")
    else:
        st.subheader("📊 접근성 분석 결과")

        # 색상 대비
        ratio = contrast_ratio(fg_color, bg_color)
        if ratio >= 4.5:
            st.success(f"✅ 색상 대비 적절 (대비 비율: {ratio}:1)")
        else:
            st.error(f"❌ 대비 부족 (현재 {ratio}:1, 최소 4.5:1 필요)")

        # 글자 크기
        if is_font_size_accessible(font_size):
            st.success(f"✅ 글자 크기 적절: {font_size}px")
        else:
            st.error(f"❌ 글자 크기 너무 작음: {font_size}px (권장: 16px 이상)")

        # 가독성
        score, level = readability_score(text)
        st.info(f"📘 가독성 점수: {score:.2f} → {level}")

        # 문장 수/단어 수 표시
        sentences = len(re.findall(r'[.!?]', text))
        words = len(text.split())
        st.write(f"📝 문장 수: {sentences}, 단어 수: {words}")

# ------------------------------
# 하단 참고 문구
# ------------------------------
st.markdown("---")
st.caption("※ 본 시스템은 WCAG 2.1 Level AA 기준 중 일부 항목에 대한 자동 분석 도구입니다.")
