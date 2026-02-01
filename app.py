import streamlit as st
import pandas as pd
import time
import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Career Map", page_icon="🧭", layout="wide")

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

# 스타일링
st.markdown("""
    <style>
    .main {background-color: #F8F9FA;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 8px; width: 100%; height: 50px; font-size: 16px;}
    .title-text {color: #1A237E; text-align: center; font-family: 'Pretendard';}
    .sub-text {color: #666; text-align: center; margin-bottom: 30px;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# STEP 1: 로그인 (Splash Screen)
# ==========================================
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.write("")
        st.markdown("<h1 class='title-text'>🧭 Career Map</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-text'>불확실한 커리어, 데이터로 길을 찾다.</p>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2910/2910791.png", width=150) # 지도 아이콘 예시
        
        st.write("")
        st.write("")
        
        # 소셜 로그인 흉내
        if st.button("카카오로 3초 만에 시작하기"):
            st.session_state.step = 2
            st.rerun()
        st.markdown("<p style='text-align: center; font-size: 12px; color: #999;'>이메일로 시작하기 | 아이디 찾기</p>", unsafe_allow_html=True)

# ==========================================
# STEP 2: 개인정보 입력 (Onboarding)
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<h2 style='text-align: center;'>반갑습니다! 👋<br>정확한 분석을 위해 정보를 알려주세요.</h2>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("info_form"):
            name = st.text_input("이름", placeholder="실명 입력")
            dob = st.date_input("생년월일", min_value=datetime.date(1995, 1, 1), max_value=datetime.date(2006, 12, 31))
            univ = st.text_input("대학교 / 전공", placeholder="예: 연세대학교 경제학과")
            gender = st.radio("성별", ["남성", "여성"], horizontal=True)
            
            submitted = st.form_submit_button("다음으로 →")
            
            if submitted:
                if name and univ:
                    st.session_state.user_info['name'] = name
                    st.session_state.user_info['univ'] = univ
                    st.session_state.step = 3
                    st.rerun()
                else:
                    st.warning("이름과 학교 정보를 모두 입력해주세요.")

# ==========================================
# STEP 3: 트랙 선택 (Branching)
# ==========================================
elif st.session_state.step == 3:
    st.title(f"{st.session_state.user_info['name']}님의 현재 상황은?")
    st.progress(33) # 진행률 표시
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.subheader("🐣 저학년 (1~2학년)")
            st.write("아직 구체적인 진로가 없어요.")
            st.markdown("- 적성/성향 검사\n- 로드맵 설계\n- 대외활동 추천")
            if st.button("저학년 트랙 선택"):
                st.session_state.user_info['track'] = 'Junior'
                st.session_state.step = 4
                st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("🦅 고학년 (3~4학년/취준)")
            st.write("취업 준비를 본격적으로 시작해요.")
            st.markdown("- 합격 확률 예측\n- 자소서/스펙 진단\n- 부족한 점 분석")
            if st.button("고학년 트랙 선택"):
                st.session_state.user_info['track'] = 'Senior'
                st.session_state.step = 4
                st.rerun()

# ==========================================
# STEP 4: 상세 진단 (Deep Dive)
# ==========================================
elif st.session_state.step == 4:
    track = st.session_state.user_info['track']
    st.title("🎯 맞춤형 분석 시작")
    st.progress(66)
    
    target_job = st.text_input("관심 직무/분야 (필수)", placeholder="예: 마케팅, 데이터 분석, 금융권 등")
    
    st.write("")
    with st.expander("🧠 성향/역량 정밀 진단 (선택)", expanded=True):
        if track == 'Junior':
            st.write("나에게 맞는 일을 찾기 위한 질문입니다.")
            st.radio("Q1. 선호하는 과제 유형은?", ["팀플/발표", "개인 리포트/분석", "창작/만들기"])
        else:
            st.write("직무 적합도를 판단하기 위한 질문입니다.")
            st.radio("Q1. 보유 중인 어학 성적은?", ["없음", "기본(IH/800)", "상위(AL/900+)"])
        
        st.file_uploader("기존 이력서/포트폴리오가 있다면 업로드하세요 (PDF)", type=['pdf'])

    st.write("")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("건너뛰기"):
             st.session_state.user_info['target_job'] = target_job if target_job else "미정"
             st.session_state.step = 5
             st.rerun()
    with col2:
        if st.button("분석 결과 보러가기 (완료)"):
            if target_job:
                st.session_state.user_info['target_job'] = target_job
                # 로딩 연출
                with st.spinner('AI가 커리어 로드맵을 생성 중입니다...'):
                    time.sleep(2)
                st.session_state.step = 5
                st.rerun()
            else:
                st.warning("관심 직무를 입력해주세요.")

# ==========================================
# STEP 5: 대시보드 (Dashboard)
# ==========================================
elif st.session_state.step == 5:
    st.sidebar.title("🧭 Career Map")
    st.sidebar.write(f"**{st.session_state.user_info['name']}**님")
    menu = st.sidebar.radio("메뉴", ["홈 (대시보드)", "나의 로드맵", "설정"])
    
    if menu == "홈 (대시보드)":
        st.header(f"🔥 {st.session_state.user_info['target_job']} 커리어 대시보드")
        
        #  - 여기서는 이미지를 넣지 않고 텍스트로 대체합니다.
        # 실제 앱에서는 이 위치에 그래프나 배너가 들어갑니다.
        
        st.success(f"**{st.session_state.user_info['name']}**님을 위한 추천 전략이 생성되었습니다.")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("📢 추천 공고")
            st.info("[인턴] 카카오 채용연계형 인턴 (D-5)")
            st.info("[신입] 삼성전자 DS부문 공채 (D-12)")
            
        with col2:
            st.subheader("⚡ 나의 상태")
            st.metric("준비도", "65%", "+10%")
            st.metric("합격 확률", "42%", "부족")

    elif menu == "나의 로드맵":
        st.header("🗺️ 커리어 가이드라인")
        if st.session_state.user_info['track'] == 'Junior':
            st.write("1~2학년을 위한 기초 다지기 로드맵입니다.")
            st.checkbox("학점 3.5 이상 만들기", value=True)
            st.checkbox("중앙 동아리 가입하기")
        else:
            st.write("취업 합격을 위한 실전 로드맵입니다.")
            st.checkbox("오픽 IH 취득", value=False)
            st.checkbox("인턴 지원하기", value=False)
