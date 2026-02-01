import streamlit as st
import time

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="Career Map v4.5", page_icon="🧭", layout="wide")

# 세션 상태 관리
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'career_type' not in st.session_state:
    st.session_state.career_type = ""
if 'final_prob' not in st.session_state:
    st.session_state.final_prob = 0

# 스타일링
st.markdown("""
    <style>
    .main {background-color: #F8F9FA;}
    h1 {color: #1A237E;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 8px; width: 100%; height: 50px; font-size: 18px; font-weight: bold;}
    .card {background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px;}
    .big-number {font-size: 40px; font-weight: bold; color: #1E88E5;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# [STEP 1] 로그인
# ==========================================
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.markdown("<h1 style='text-align: center;'>🧭 Career Map</h1>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;'>데이터 기반 대학생 커리어 네비게이션</h5>", unsafe_allow_html=True)
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
# [STEP 2] 트랙 선택 (Main Hub)
# ==========================================
elif st.session_state.step == 2:
    st.title(f"반갑습니다, {st.session_state.user_name}님! 👋")
    st.subheader("현재 상황에 맞는 솔루션을 선택하세요.")
    
    col1, col2 = st.columns(2)
    
    # Track A: 저학년 (진로 탐색)
    with col1:
        with st.container(border=True):
            st.markdown("### 🐣 진로 탐색 (저학년)")
            st.info("나에게 맞는 직무가 무엇인지 모르겠다면?")
            st.write("- 커리어 성향/적성 진단")
            st.write("- 전공 기반 유망 직무 추천")
            st.write("- 학년별 필수 로드맵 제공")
            if st.button("나의 커리어 성향 찾기 👉"):
                st.session_state.grade_mode = "Junior"
                st.session_state.step = 21 # Junior 진단
                st.rerun()

    # Track B: 고학년 (실전 취업)
    with col2:
        with st.container(border=True):
            st.markdown("### 🦅 실전 취업 (고학년)")
            st.info("목표 기업 합격 확률이 궁금하다면?")
            st.write("- 스펙 정밀 진단 (Gap 분석)")
            st.write("- 합격 확률 시뮬레이션")
            st.write("- 부족한 스펙 보완 전략")
            if st.button("합격 확률 진단하기 👉"):
                st.session_state.grade_mode = "Senior"
                st.session_state.step = 31 # Senior 입력
                st.rerun()

# ==========================================
# [STEP 2-1] Junior: 성향 진단
# ==========================================
elif st.session_state.step == 21:
    st.title("🧩 커리어 성향 진단 (Career DNA)")
    st.write("간단한 질문을 통해 본인에게 딱 맞는 직무 스타일을 찾아드립니다.")
    
    with st.container(border=True):
        q1 = st.radio("Q1. 팀 프로젝트를 할 때 나는?", 
                      ["자료 조사를 하고 논리적인 근거를 찾는 게 편하다.", 
                       "발표 자료를 만들거나 아이디어를 내는 게 즐겁다.",
                       "팀원들의 의견을 조율하고 이끄는 게 좋다."])
        st.write("")
        q2 = st.radio("Q2. 내가 선호하는 과제 유형은?", 
                      ["정해진 답이 있는 수학/통계/분석 과제", 
                       "나만의 생각을 펼치는 에세이/기획 과제",
                       "사람들과 토론하고 결과를 도출하는 과제"])
    
    st.write("")
    if st.button("진단 결과 확인하기"):
        with st.spinner('AI가 성향을 분석하고 있습니다...'):
            time.sleep(1.5)
        
        # 진단 로직
        if "자료" in q1 or "수학" in q2:
            st.session_state.career_type = "분석가형 (Analyst)"
        elif "아이디어" in q1 or "에세이" in q2:
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
    st.title("💎 진단 결과 리포트")
    
    st.markdown(f"""
    <div class="card" style="background-color:#E3F2FD; border-left: 5px solid #2196F3;">
        <h3>{st.session_state.user_name}님의 커리어 유형은 <b>'{st.session_state.career_type}'</b> 입니다.</h3>
        <p>꼼꼼한 데이터 분석과 논리적인 사고에 강점이 있습니다. <br>
        단순 사무보다는 <b>전문성을 요하는 직무</b>에서 두각을 나타낼 가능성이 높습니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚀 추천 직무")
        if "분석가" in st.session_state.career_type:
            st.success("1. 데이터 분석가 (Data Analyst)")
            st.info("2. 금융/투자 심사역")
        elif "창작자" in st.session_state.career_type:
            st.success("1. 서비스 기획 (PM/PO)")
            st.info("2. 마케팅/브랜드 매니저")
        else:
            st.success("1. 영업/영업관리")
            st.info("2. 인사(HR) 매니저")
            
    with col2:
        st.subheader("🗺️ 학년별 액션 플랜")
        st.warning("⚠️ **Foundation 단계 (1~2학년)**")
        st.checkbox("학점 3.8 이상 유지 (성실성 증명)", value=True)
        st.checkbox("관련 분야 학회/동아리 가입")
        st.checkbox("컴활/한국사 자격증 취득")
    
    st.divider()
    if st.button("처음으로"):
        st.session_state.step = 1
        st.rerun()

# ==========================================
# [STEP 3-1] Senior: 스펙 상세 입력 (추가됨!)
# ==========================================
elif st.session_state.step == 31:
    st.title("📊 합격 확률 진단")
    st.info("보유하고 계신 스펙을 입력해주세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("학업 및 어학")
        gpa = st.slider("학점 (4.3)", 2.0, 4.3, 3.5, 0.1)
        toeic = st.slider("토익", 500, 990, 800, 10)
    with col2:
        st.subheader("실무 및 경험")
        intern = st.number_input("인턴 경험 (개월)", 0, 24, 0)
        awards = st.number_input("공모전 수상 (회)", 0, 10, 0)

    st.write("")
    if st.button("AI 분석 시작 🚀"):
        with st.spinner("합격 데이터와 대조 중..."):
            time.sleep(1.5)
            # 가상 점수 계산
            score = (gpa * 10) + (intern * 5) + (awards * 3)
            if toeic >= 850: score += 10
            st.session_state.final_prob = min(int(score), 98)
            st.session_state.intern_months = intern
            st.session_state.step = 32
            st.rerun()

# ==========================================
# [STEP 3-2] Senior: 분석 결과 (추가됨!)
# ==========================================
elif st.session_state.step == 32:
    st.title("📈 AI 합격 예측 리포트")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <p style="color:#666; margin:0;">예상 합격 확률</p>
            <div class="big-number">{st.session_state.final_prob}%</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        gap = 100 - st.session_state.final_prob
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <p style="color:#666; margin:0;">부족한 점수(Gap)</p>
            <div class="big-number" style="color:#FF5252;">-{gap}</div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("💡 AI 분석 코멘트")
    if st.session_state.intern_months == 0:
        st.error("🚨 **Critical:** 실무 경험(인턴)이 부족합니다.")
        st.write("가장 시급한 것은 '직무 관련 경험'을 만드는 것입니다.")
    elif st.session_state.final_prob < 80:
        st.warning("⚠️ **Warning:** 스펙이 평범합니다. 차별화 포인트가 필요합니다.")
    else:
        st.success("🎉 **Excellent:** 아주 훌륭한 상태입니다.")

    st.divider()
    if st.button("처음으로 돌아가기"):
        st.session_state.step = 1
        st.rerun()
