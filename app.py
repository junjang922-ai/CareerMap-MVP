import streamlit as st
import pandas as pd
import time

# 1. 페이지 기본 설정 및 세션 초기화
st.set_page_config(page_title="Career Map Foundation", page_icon="🧭", layout="wide")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'grade_mode' not in st.session_state:
    st.session_state.grade_mode = ""

# 스타일링 (가독성 및 디자인 강화)
st.markdown("""
    <style>
    .main {background-color: #F8F9FA;}
    h1 {color: #1A237E;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 8px; height: 50px; font-weight: bold; font-size: 16px;}
    .card {background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px;}
    .big-number {font-size: 36px; font-weight: bold; color: #1E88E5;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# [STEP 1] 로그인 및 온보딩
# ==========================================
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.markdown("<h1 style='text-align: center;'>🧭 Career Map</h1>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;'>불확실성을 확신으로 바꾸는 커리어 네비게이션</h5>", unsafe_allow_html=True)
        st.divider()
        
        name_input = st.text_input("이름을 입력해주세요", placeholder="예: 연세인")
        
        if st.button("시작하기"):
            if name_input:
                st.session_state.user_name = name_input
                st.session_state.step = 2
                st.rerun()
            else:
                st.warning("이름을 입력해주세요.")

# ==========================================
# [STEP 2] 트랙 선택 (Dual Track)
# ==========================================
elif st.session_state.step == 2:
    st.title(f"반갑습니다, {st.session_state.user_name}님! 👋")
    st.subheader("현재 본인의 상황을 선택해주세요.")
    st.write("상황에 따라 맞춤형 솔루션을 제공합니다.")

    col1, col2 = st.columns(2)
    
    # Track A: 저학년 (진로 탐색)
    with col1:
        with st.container(border=True):
            st.markdown("### 🐣 진로 탐색 트랙 (1~2학년)")
            st.info("아직 구체적인 직무를 정하지 못했나요?")
            st.write("✅ **제공 기능:**")
            st.write("- 커리어 성향(DNA) 진단")
            st.write("- 전공 기반 유망 직무 추천")
            st.write("- 학년별 기초 로드맵")
            if st.button("나의 성향 알아보기 👉"):
                st.session_state.grade_mode = "Junior"
                st.session_state.step = 21 # Junior 진단 페이지
                st.rerun()

    # Track B: 고학년 (실전 취준)
    with col2:
        with st.container(border=True):
            st.markdown("### 🦅 실전 취업 트랙 (3~4학년)")
            st.info("목표 기업 합격 확률이 궁금한가요?")
            st.write("✅ **제공 기능:**")
            st.write("- 정밀 스펙 진단 (Gap 분석)")
            st.write("- 합격 확률 시뮬레이션")
            st.write("- 부족한 점수 보완 전략")
            if st.button("합격 확률 진단하기 👉"):
                st.session_state.grade_mode = "Senior"
                st.session_state.step = 31 # Senior 입력 페이지
                st.rerun()

# ==========================================
# [STEP 2-1] Junior: 성향 진단 (MBTI Style)
# ==========================================
elif st.session_state.step == 21:
    st.title("🧩 커리어 성향 진단")
    st.progress(50)
    st.write("가장 나답다고 생각되는 항목을 선택하세요.")
    
    with st.container(border=True):
        q1 = st.radio("Q1. 프로젝트를 진행할 때 나는?", 
            ["논리적인 근거와 데이터를 찾는 게 편하다.", 
             "새로운 아이디어를 내고 기획하는 게 즐겁다.",
             "사람들을 이끌고 의견을 조율하는 게 좋다."])
        st.write("")
        q2 = st.radio("Q2. 선호하는 과제 유형은?", 
            ["명확한 답이 있는 분석 과제", 
             "창의력이 필요한 에세이/발표",
             "팀워크가 중요한 조별 과제"])

    st.write("")
    if st.button("진단 결과 확인"):
        with st.spinner("성향 분석 중..."):
            time.sleep(1.5)
            # 간단 로직
            if "데이터" in q1 or "분석" in q2:
                st.session_state.career_type = "분석가형 (Analyst)"
            elif "아이디어" in q1 or "창의력" in q2:
                st.session_state.career_type = "창작자형 (Creator)"
            else:
                st.session_state.career_type = "리더형 (Manager)"
            st.session_state.step = 22
            st.rerun()

# ==========================================
# [STEP 2-2] Junior: 결과 및 로드맵
# ==========================================
elif st.session_state.step == 22:
    st.balloons()
    st.title("💎 진단 결과")
    
    st.markdown(f"""
    <div class="card" style="border-left: 5px solid #4A90E2;">
        <h3>{st.session_state.user_name}님의 유형은 <b>'{st.session_state.career_type}'</b> 입니다.</h3>
        <p>본인의 강점을 살릴 수 있는 추천 직무와 로드맵을 확인하세요.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚀 추천 직무")
        if "분석가" in st.session_state.career_type:
            st.success("1. 데이터 분석가 / 비즈니스 분석가")
            st.info("2. 금융권 심사역 / 리스크 관리")
        elif "창작자" in st.session_state.career_type:
            st.success("1. 서비스 기획 (PM)")
            st.info("2. 마케팅 / 콘텐츠 기획")
        else:
            st.success("1. 인사(HR) / 조직문화 담당")
            st.info("2. 영업 관리 / 프로젝트 매니저")
            
    with col2:
        st.subheader("🗺️ 1~2학년 필수 로드맵")
        st.checkbox("학점 3.8 이상 유지하기", value=True)
        st.checkbox("관련 분야 학회/동아리 가입")
        st.checkbox("어학(토익) 기초 점수 확보")
    
    st.divider()
    st.button("처음으로", on_click=lambda: st.session_state.update(step=1))

# ==========================================
# [STEP 3-1] Senior: 스펙 상세 입력
# ==========================================
elif st.session_state.step == 31:
    st.title("📊 스펙 정밀 진단")
    st.info("정확한 합격 확률 계산을 위해 상세 정보를 입력해주세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("학업 및 어학")
        gpa = st.slider("학점 (4.3)", 2.0, 4.3, 3.5, 0.1)
        toeic = st.slider("토익", 500, 990, 800, 10)
        opic = st.selectbox("오픽(OPIc)", ["None", "IM1", "IM2", "IM3", "IH", "AL"])
    
    with col2:
        st.subheader("실무 및 경험")
        intern = st.number_input("인턴 경험 (개월)", 0, 24, 0)
        awards = st.number_input("공모전 수상 (회)", 0, 10, 0)
        license = st.number_input("직무 관련 자격증 (개)", 0, 5, 0)

    st.write("")
    if st.button("AI 분석 시작 🚀"):
        with st.spinner("합격자 데이터와 비교 중..."):
            time.sleep(1.5)
            # 점수 계산 (가상)
            score = (gpa * 10) + (intern * 5) + (awards * 3)
            if toeic >= 900 or opic in ["IH", "AL"]: score += 10
            st.session_state.final_prob = min(int(score), 98)
            st.session_state.intern_months = intern # 진단용 저장
            st.session_state.step = 32
            st.rerun()

# ==========================================
# [STEP 3-2] Senior: 분석 결과 & 처방
# ==========================================
elif st.session_state.step == 32:
    st.title("📈 AI 합격 예측 리포트")
    
    # 1. 점수 대시보드
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <p style="color:#666; margin:0;">예상 합격 확률</p>
            <div class="big-number">{st.session_state.final_prob}%</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        status_color = "#4CAF50" if st.session_state.final_prob >= 80 else "#FF5252"
        status_text = "안정권" if st.session_state.final_prob >= 80 else "보완 필요"
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <p style="color:#666; margin:0;">현재 상태</p>
            <div class="big-number" style="color:{status_color};">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

    # 2. 상세 피드백 (조건부 로직)
    st.subheader("💡 AI 분석 코멘트")
    if st.session_state.intern_months == 0:
        st.error("🚨 **Critical Warning:** 실무 경험(인턴)이 없습니다. 요즘 채용 트렌드에서 가장 치명적입니다.")
        st.write("👉 **솔루션:** 이번 방학에는 무조건 '직무 체험형 인턴'이나 '산학 협력 프로젝트'에 지원하세요.")
    elif st.session_state.final_prob < 80:
        st.warning("⚠️ **Warning:** 평균적인 스펙이나, 확실한 '한 방(Killer Content)'이 부족합니다.")
        st.write("👉 **솔루션:** 직무 관련 공모전 수상이나, 데이터 분석 자격증을 추가하여 차별화하세요.")
    else:
        st.success("🎉 **Excellent:** 스펙 완성도가 높습니다. 이제 자소서와 면접 스킬을 다듬으세요.")

    st.divider()
    
    # 여기가 다음 스텝을 쌓을 공간입니다.
    st.info("이 결과를 바탕으로 **[체계적인 관리]**를 시작하시겠습니까?")
    # (여기에 듀오링고 스타일의 관리 버튼이나, 자소서 업로드 버튼 등을 추가할 예정)
    
    if st.button("처음으로"):
        st.session_state.step = 1
        st.rerun()
