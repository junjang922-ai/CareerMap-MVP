import streamlit as st
import pandas as pd
import time
import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Career Map Final", page_icon="🧭", layout="wide")

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 'input' # input -> result -> dashboard 순서
if 'user_name' not in st.session_state:
    st.session_state.user_name = "연세인"
if 'streak' not in st.session_state:
    st.session_state.streak = 1

# 스타일링
st.markdown("""
    <style>
    .main {background-color: #F8F9FA;}
    h1 {color: #1A237E;}
    .stButton>button {border-radius: 10px; height: 50px; font-weight: bold;}
    .metric-card {background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center;}
    .big-score {font-size: 48px; font-weight: bold; color: #4A90E2;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# [STEP 1] 데이터 입력 및 진단 (Diagnosis)
# ==========================================
if st.session_state.step == 'input':
    st.title("🧭 Career Map : AI 정밀 진단")
    st.info("현재 스펙을 입력하시면, 목표 기업 합격 확률을 분석하고 맞춤형 관리 플랜을 짜드립니다.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1️⃣ 기본 정보")
        st.session_state.user_name = st.text_input("이름", "김연세")
        target_corp = st.text_input("목표 기업/직무", "삼성전자 / 마케팅")
        grade = st.radio("현재 학년", ["1~2학년 (저학년)", "3~4학년 (고학년/취준)"])

    with col2:
        st.subheader("2️⃣ 정량 스펙 입력")
        gpa = st.slider("학점 (4.3 만점)", 2.0, 4.3, 3.6, step=0.1)
        toeic = st.slider("토익 점수", 500, 990, 800, step=10)
        intern = st.number_input("인턴 경험 (개월)", 0, 24, 0)
        awards = st.number_input("공모전/수상 (회)", 0, 10, 0)

    st.write("")
    if st.button("🚀 AI 분석 시작하기 (Click)"):
        with st.spinner("빅데이터와 대조하여 합격 확률 계산 중..."):
            time.sleep(1.5) # 로딩 연출
            
            # 점수 계산 로직 (가상)
            score = (gpa * 10) + (intern * 5) + (awards * 5)
            if toeic > 850: score += 10
            final_prob = min(int(score), 95)
            
            # 세션에 결과 저장
            st.session_state.final_prob = final_prob
            st.session_state.step = 'result'
            st.rerun()

# ==========================================
# [STEP 2] 분석 결과 및 로드맵 처방 (Prescription)
# ==========================================
elif st.session_state.step == 'result':
    st.title(f"📊 {st.session_state.user_name}님의 진단 리포트")
    
    # 1. 합격 확률 대시보드
    col1, col2, col3 = st.columns([1, 1, 1.5])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #666;">현재 합격 확률</div>
            <div class="big-score">{st.session_state.final_prob}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        gap = 100 - st.session_state.final_prob
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #666;">부족한 점수(Gap)</div>
            <div class="big-score" style="color: #FF5252;">-{gap}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("### 💡 AI 분석 코멘트")
        if st.session_state.final_prob < 60:
            st.error("🚨 **위험:** 실무 경험(인턴) 보완이 시급합니다.")
            st.write("경쟁자들은 평균 1.5회의 인턴 경험을 보유하고 있습니다.")
        elif st.session_state.final_prob < 80:
            st.warning("⚠️ **보통:** 정량 스펙은 평균이나, 차별점이 부족합니다.")
            st.write("직무 관련 자격증이나 프로젝트 경험을 하나 더 추가하세요.")
        else:
            st.success("🎉 **안정:** 아주 훌륭한 스펙입니다. 자소서에 집중하세요.")

    st.divider()

    # 2. 처방된 로드맵 (Roadmap)
    st.subheader("🗺️ 합격 확률 90% 달성을 위한 솔루션")
    st.info("AI가 분석한 부족한 점을 채우기 위해, 아래 로드맵을 제안합니다.")
    
    with st.container(border=True):
        st.write("**(1개월차) 기초 다지기:** OPIc IH 달성, 컴활 1급 필기")
        st.write("**(2개월차) 경험 쌓기:** 데이터 분석 프로젝트 수행 (포트폴리오용)")
        st.write("**(3개월차) 실전 투입:** 하계 인턴 지원서 10곳 제출")

    st.write("")
    st.markdown("### ⚡ 이 로드맵을 실행하시겠습니까?")
    st.write("지금 **'데일리 관리 모드'**를 시작하면, 위 로드맵을 매일의 퀘스트로 쪼개서 관리해드립니다.")
    
    if st.button("🔥 데일리 관리 모드 시작하기 (Start)"):
        st.balloons()
        time.sleep(1)
        st.session_state.step = 'dashboard'
        st.rerun()
    
    if st.button("⬅️ 다시 진단하기"):
        st.session_state.step = 'input'
        st.rerun()

# ==========================================
# [STEP 3] 데일리 퀘스트 관리 (Management - Duolingo Style)
# ==========================================
elif st.session_state.step == 'dashboard':
    # 상단바
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("🔥 오늘의 커리어 퀘스트")
        st.caption(f"{st.session_state.user_name}님의 합격 확률 {st.session_state.final_prob}%를 유지/상승 시키기 위한 미션입니다.")
    with c2:
        st.markdown(f"<h3 style='color:#FF9100; text-align:right;'>🔥 {st.session_state.streak}일째 연속</h3>", unsafe_allow_html=True)
    
    st.divider()

    col_q, col_p = st.columns([1.5, 1])

    with col_q:
        st.subheader("✅ Today's Action Items")
        
        # 퀘스트 리스트 (로드맵 기반 생성)
        with st.container(border=True):
            st.markdown("**[어학] 아침 30분 영어 루틴**")
            q1 = st.checkbox("OPIc 스크립트 1개 암기하기")
            
        with st.container(border=True):
            st.markdown("**[직무] 산업 트렌드 파악**")
            q2 = st.checkbox("관심 직무(마케팅) 뉴스 기사 1개 스크랩")
            
        with st.container(border=True):
            st.markdown("**[멘탈] 합격 후기 분석**")
            q3 = st.checkbox("합격자 자소서 1개 읽고 키워드 뽑기")

        # 달성 축하
        if q1 and q2 and q3:
            st.success("🎉 훌륭합니다! 오늘의 경험치(+50XP)를 획득했습니다.")
            st.button("내일 미션 미리보기")

    with col_p:
        st.subheader("📈 나의 성장 그래프")
        st.write("지난주보다 활동량이 **15% 증가**했습니다.")
        # 가상의 차트
        chart_data = pd.DataFrame({'Activity': [20, 40, 60, 50, 80, 90, 100]}, index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        st.line_chart(chart_data)
        
        st.info("💡 **알림:** 내일 오전 9시에 다음 퀘스트가 도착합니다.")

    st.divider()
    if st.button("📋 분석 결과 다시 보기"):
        st.session_state.step = 'result'
        st.rerun()
