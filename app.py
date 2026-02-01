import streamlit as st
import time

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="Career Map v4.0", page_icon="🧭", layout="wide")

# 세션 상태 관리 (단계 이동 및 데이터 저장)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'career_type' not in st.session_state:
    st.session_state.career_type = "" # 진단 결과 저장

# 스타일링
st.markdown("""
    <style>
    .main {background-color: #F5F7FA;}
    h1 {color: #1A237E;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 8px; width: 100%; height: 50px; font-size: 18px; font-weight: bold;}
    .big-font {font-size: 20px !important;}
    .card {background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# --- STEP 1: 로그인 ---
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.markdown("<h1 style='text-align: center;'>🧭 Career Map</h1>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;'>데이터 기반 대학생 커리어 네비게이션</h5>", unsafe_allow_html=True)
        st.divider()
        
        name_input = st.text_input("이름을 입력해주세요", placeholder="예: 연세인")
        password = st.text_input("비밀번호 (아무거나 입력)", type="password")
        
        if st.button("시작하기"):
            if name_input:
                st.session_state.user_name = name_input
                st.session_state.step = 2
                st.rerun()
            else:
                st.warning("이름을 입력해주세요.")

# --- STEP 2: 트랙 선택 ---
elif st.session_state.step == 2:
    st.title(f"반갑습니다, {st.session_state.user_name}님! 👋")
    st.subheader("현재 상황에 맞는 솔루션을 선택하세요.")
    
    col1, col2 = st.columns(2)
    
    # [저학년 트랙] - 여기를 누르면 진단 검사로 이동 (Step 2-1)
    with col1:
        with st.container(border=True):
            st.markdown("### 🐣 진로 탐색 (저학년)")
            st.info("나에게 맞는 직무가 무엇인지 모르겠다면?")
            st.write("- 커리어 성향/적성 진단")
            st.write("- 전공 기반 유망 직무 추천")
            st.write("- 학년별 필수 로드맵 제공")
            if st.button("나의 커리어 성향 찾기 👉"):
                st.session_state.grade_mode = "Junior"
                st.session_state.step = 21 # 저학년 전용 진단 스텝
                st.rerun()

    # [고학년 트랙] - 기존 유지 (Step 3)
    with col2:
        with st.container(border=True):
            st.markdown("### 🦅 실전 취업 (고학년)")
            st.info("목표 기업 합격 확률이 궁금하다면?")
            st.write("- 이력서/자소서 AI 분석")
            st.write("- 합격 확률 시뮬레이션")
            st.write("- 부족한 스펙(Gap) 분석")
            if st.button("합격 확률 진단하기 👉"):
                st.session_state.grade_mode = "Senior"
                st.session_state.step = 3
                st.rerun()

# --- STEP 2-1: 저학년 성향 진단 (New!) ---
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
        q3 = st.radio("Q3. 나중에 일하고 싶은 환경은?", 
                      ["조용히 내 전문성을 쌓을 수 있는 곳", 
                       "트렌디하고 변화가 빠른 곳",
                       "사람들과 부대끼며 성과를 내는 곳"])

    st.write("")
    if st.button("진단 결과 확인하기"):
        # 로딩 연출
        with st.spinner('AI가 성향을 분석하고 있습니다...'):
            time.sleep(2)
        
        # 간단한 로직 (실제로는 더 복잡하겠지만 MVP용)
        if "자료" in q1 or "수학" in q2:
            st.session_state.career_type = "분석가형 (Analyst)"
        elif "아이디어" in q1 or "에세이" in q2:
            st.session_state.career_type = "창작자형 (Creator)"
        else:
            st.session_state.career_type = "리더형 (Manager)"
            
        st.session_state.step = 22 # 결과 화면으로 이동
        st.rerun()

# --- STEP 2-2: 저학년 진단 결과 및 로드맵 ---
elif st.session_state.step == 22:
    st.balloons()
    st.title("💎 진단 결과 리포트")
    
    # 1. 성향 분석 결과
    st.markdown(f"""
    <div class="card" style="background-color:#E3F2FD; border-left: 5px solid #2196F3;">
        <h3>{st.session_state.user_name}님의 커리어 유형은 <b>'{st.session_state.career_type}'</b> 입니다.</h3>
        <p>꼼꼼한 데이터 분석과 논리적인 사고에 강점이 있습니다. <br>
        단순 사무보다는 <b>전문성을 요하는 직무</b>에서 두각을 나타낼 가능성이 높습니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # 2. 추천 직무
    with col1:
        st.subheader("🚀 추천 직무 (Top 3)")
        if "분석가" in st.session_state.career_type:
            st.success("1. 데이터 분석가 (Data Analyst)")
            st.info("2. 금융/투자 심사역")
            st.info("3. 전략 기획 (Strategy)")
        elif "창작자" in st.session_state.career_type:
            st.success("1. 서비스 기획 (PM/PO)")
            st.info("2. 마케팅/브랜드 매니저")
            st.info("3. UX 리서처")
        else:
            st.success("1. 영업/영업관리")
            st.info("2. 인사(HR) 매니저")
            st.info("3. 프로젝트 매니저")

    # 3. 맞춤형 로드맵 (여기가 핵심)
    with col2:
        st.subheader("🗺️ 학년별 액션 플랜")
        tab1, tab2 = st.tabs(["1~2학년 (지금 할 일)", "3~4학년 (미리 보기)"])
        
        with tab1:
            st.warning("⚠️ **Foundation 단계**")
            st.checkbox("학점 3.8 이상 유지 (성실성 증명)", value=True)
            if "분석가" in st.session_state.career_type:
                st.checkbox("통계학 입문 / 파이썬 기초 수강")
                st.checkbox("교내 학회 (경제/투자/데이터) 지원")
            else:
                st.checkbox("교내 공모전 1회 이상 참여")
                st.checkbox("연합 동아리 가입 (네트워킹)")

        with tab2:
            st.info("🔜 **Build-up 단계**")
            st.write("- 인턴십 1회 이상 (방학)")
            st.write("- 직무 관련 자격증 취득")
    
    st.divider()
    if st.button("다시 처음으로"):
        st.session_state.step = 1
        st.rerun()

# --- STEP 3: 고학년 (기존과 동일하지만 간단히 유지) ---
elif st.session_state.step == 3:
    st.title("📄 이력서/포트폴리오 분석")
    st.info("고학년 트랙입니다. (이전 단계 로직과 동일하게 구현)")
    # (고학년 코드는 이전 답변의 v3.0 내용을 그대로 쓰시면 됩니다. 
    #  너무 길어져서 여기서는 저학년 기능 위주로 보여드렸습니다.)
    if st.button("돌아가기"):
        st.session_state.step = 2
        st.rerun()
