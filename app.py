import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1. 페이지 설정 (탭 이름, 아이콘)
st.set_page_config(
    page_title="Career Map - 불확실성을 확신으로",
    page_icon="🧭",
    layout="wide"
)

# 2. 스타일링 (커스텀 CSS - Sky & Lemon 테마 적용)
st.markdown("""
    <style>
    .main {background-color: #F5F7FA;}
    h1 {color: #1A237E;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 10px;}
    .highlight {background-color: #FFD54F; padding: 5px; border-radius: 5px; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바: 사용자 기본 정보 입력
with st.sidebar:
    st.title("🧭 Career Map")
    st.write("내 커리어의 네비게이션")
    user_name = st.text_input("이름/닉네임", "연세인")
    major = st.selectbox("전공", ["경제학과", "경영학과", "응용통계학과", "기타"])
    grade = st.radio("현재 학년", ["1~2학년 (저학년)", "3~4학년 (고학년/취준)"])

# 4. 메인 화면 로직 (Dual Track)
st.title(f"반갑습니다, {user_name}님! 👋")

# --- Track A: 고학년 (시뮬레이터) ---
if grade == "3~4학년 (고학년/취준)":
    st.header("📊 합격 확률 시뮬레이터")
    st.info("목표 기업 합격을 위해 무엇을 더 채워야 할까요? 슬라이더를 움직여보세요!")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("나의 스펙 입력")
        gpa = st.slider("학점 (4.3 만점)", 2.0, 4.3, 3.5)
        toeic = st.slider("토익 점수", 500, 990, 800)
        speaking = st.selectbox("스피킹 (OPIc)", ["None", "IM1", "IM2", "IM3", "IH", "AL"])
        license_count = st.slider("직무 관련 자격증 수", 0, 5, 1)

    with col2:
        st.subheader("예측 결과")
        
        # (간단한 가상 로직 - 실제로는 엑셀 데이터 연동 가능)
        base_score = 40 # 기본 점수
        score = base_score + (gpa * 5) + ((toeic-500)/10) + (license_count * 10)
        if speaking in ["IH", "AL"]: score += 15
        elif speaking in ["IM3"]: score += 10
        
        final_prob = min(score, 99) # 99% 넘지 않게

        # 결과 시각화
        st.metric(label="예상 합격 확률", value=f"{int(final_prob)}%", delta=f"평균 대비 {int(final_prob - 50)}%p")
        
        # 차트 그리기
        chart_data = pd.DataFrame({
            "구분": ["나의 현재 위치", "합격 안정권"],
            "점수": [final_prob, 85]
        })
        st.bar_chart(chart_data.set_index("구분"))

        if final_prob < 60:
            st.warning("🚨 비상! 토익을 900점까지 올리면 확률이 15% 오릅니다.")
        elif final_prob < 80:
            st.success("✅ 안정권 진입 직전! 자격증 1개만 더 따면 완벽해요.")
        else:
            st.balloons()
            st.success("🎉 합격 안정권입니다! 자소서에 집중하세요.")

# --- Track B: 저학년 (로드맵) ---
else:
    st.header("🗺️ 학년별 성장 로드맵")
    st.info("막막한 대학 생활, 이 순서대로만 따라오세요.")

    tab1, tab2, tab3 = st.tabs(["1학년: 탐색", "2학년: 경험", "3학년: 직무"])

    with tab1:
        st.markdown("### 🐣 1학년: 나를 알아가는 시간")
        st.checkbox("학점 3.5 이상 유지하기 (재수강 방지)")
        st.checkbox("중앙 동아리 1개 가입하기 (인맥)")
        st.checkbox("다양한 교양 수업 듣기")

    with tab2:
        st.markdown("### 🦅 2학년: 경험을 쌓는 시간 (Golden Time)")
        st.write(f"{major} 전공생에게 추천하는 활동입니다.")
        st.success("💡 **추천 학회:** Y.E.S (경제학회), MARP (마케팅)")
        st.checkbox("컴활 1급 / 한능검 취득하기 (방학)")
        st.checkbox("전공 기초 과목(미시/거시) A학점 받기")

    with tab3:
        st.markdown("### 🚀 3학년: 직무를 정하는 시간")
        st.warning("이제는 '진로'를 좁혀야 합니다.")
        st.checkbox("인턴십 지원하기 (여름방학)")
        st.checkbox("오픽/토스 점수 미리 만들어두기")

# 5. 하단 푸터
st.divider()
st.caption("© 2026 Career Map. All rights reserved. | Powered by Yonsei Univ. Startup Team")
