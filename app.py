import streamlit as st
import pandas as pd
import time
import datetime

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="Career Map Dashboard", page_icon="🧭", layout="wide")

# 세션 상태 관리
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1:로그인 -> 2:트랙선택 -> 3:상세입력 -> 4:대시보드
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

# 스타일링 (서핏 느낌의 카드 UI)
st.markdown("""
    <style>
    .main {background-color: #F8F9FA;}
    h1, h2, h3 {color: #1A237E; font-family: 'Pretendard', sans-serif;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 8px; width: 100%; height: 45px;}
    
    /* 대시보드 카드 스타일 */
    .feed-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #E0E0E0;
        transition: transform 0.2s;
    }
    .feed-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .tag {
        background-color: #E3F2FD;
        color: #1565C0;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    .sidebar-menu {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
        cursor: pointer;
    }
    .sidebar-menu:hover {
        background-color: #E8EAF6;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# STEP 1: 로그인 및 개인정보 (Onboarding)
# ==========================================
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; margin-top: 50px;'>🧭 Career Map</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>나만의 커리어 네비게이션을 시작하세요.</p>", unsafe_allow_html=True)
        st.divider()
        
        with st.container(border=True):
            name = st.text_input("이름", placeholder="예: 김연세")
            dob = st.date_input("생년월일", min_value=datetime.date(1990, 1, 1))
            univ = st.text_input("학교/전공", placeholder="예: 연세대학교 경제학과")
            
            if st.button("다음으로 →"):
                if name and univ:
                    st.session_state.user_info['name'] = name
                    st.session_state.user_info['univ'] = univ
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.warning("정보를 입력해주세요.")

# ==========================================
# STEP 2: 트랙 선택 (Track Selection)
# ==========================================
elif st.session_state.step == 2:
    st.title(f"{st.session_state.user_info['name']}님, 반갑습니다! 👋")
    st.subheader("현재 어떤 상황인지 알려주세요.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🐣 저학년 (1~2학년)")
            st.write("아직 구체적인 진로를 정하지 못했어요.")
            st.info("🎯 **제공 서비스:** 커리어 로드맵, 적성 검사, 대외활동 추천")
            if st.button("저학년 트랙 선택"):
                st.session_state.user_info['track'] = 'Junior'
                st.session_state.step = 3
                st.rerun()
                
    with col2:
        with st.container(border=True):
            st.markdown("### 🦅 고학년 (3~4학년/취준)")
            st.write("목표 직무가 있고, 합격이 목표예요.")
            st.info("🎯 **제공 서비스:** 스펙/자소서 분석, 합격 확률 예측, 부족한 점 진단")
            if st.button("고학년 트랙 선택"):
                st.session_state.user_info['track'] = 'Senior'
                st.session_state.step = 3
                st.rerun()

# ==========================================
# STEP 3: 상세 진단 & 파일 업로드 (Deep Dive)
# ==========================================
elif st.session_state.step == 3:
    track = st.session_state.user_info['track']
    st.title("🧩 맞춤형 설계를 위한 추가 정보")
    
    # 공통 질문
    target_job = st.text_input("관심 직무/분야 (필수)", placeholder="예: 마케팅, 데이터 분석, 금융권 등")
    
    st.write("")
    st.markdown("### 🕵️ 정밀 진단 (선택 사항)")
    st.caption("입력하시면 분석 정확도가 **200%** 올라갑니다.")
    
    # 인성/성향 검사 (간소화)
    with st.expander("🧠 간단 성향/인성 검사 진행하기"):
        st.radio("1. 새로운 문제를 마주했을 때 나는?", ["논리적으로 분석한다", "직관적으로 해결책을 찾는다", "주변에 조언을 구한다"])
        st.radio("2. 선호하는 업무 환경은?", ["체계적이고 안정적인 곳", "자율적이고 도전적인 곳", "팀워크가 중요한 곳"])
        st.checkbox("진단 결과 반영하기")

    # 파일 업로드
    uploaded_file = st.file_uploader("📂 이력서/자소서/포트폴리오 업로드 (PDF, Word)", type=['pdf', 'docx'])
    
    st.write("")
    if st.button("🚀 나만의 커리어 대시보드 생성하기"):
        if target_job:
            st.session_state.user_info['target_job'] = target_job
            
            # 로딩 연출 (Wizard of Oz)
            progress_text = "AI가 회원님의 성향과 스펙을 분석 중입니다..."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.02)
                my_bar.progress(percent_complete + 1)
            
            st.session_state.step = 4
            st.rerun()
        else:
            st.warning("관심 직무는 필수 입력 사항입니다.")

# ==========================================
# STEP 4: 메인 대시보드 (Surfit Style)
# ==========================================
elif st.session_state.step == 4:
    
    # [사이드바] 네비게이션
    with st.sidebar:
        st.title("🧭 Career Map")
        st.write(f"**{st.session_state.user_info['name']}**님")
        st.caption(f"{st.session_state.user_info['univ']} | {st.session_state.user_info['track']}")
        st.divider()
        
        # 메뉴 선택 (라디오 버튼을 메뉴처럼 활용)
        menu = st.radio("MENU", ["🏠 홈 (Feed)", "🗺️ 나의 로드맵/전략", "📂 내 서류함", "⚙️ 설정"])
        
        st.divider()
        st.info("💡 **Premium 기능**\n현직자 1:1 멘토링 매칭")

    # [메인 화면 1] 홈 (뉴스피드)
    if menu == "🏠 홈 (Feed)":
        st.header(f"🔥 {st.session_state.user_info['target_job']} 분야 트렌드")
        
        # 상단 추천 배너
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #4A90E2 0%, #00E676 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
            <h3>📢 {st.session_state.user_info['name']}님을 위한 추천 공고</h3>
            <p>회원님의 스펙과 <b>92% 일치</b>하는 인턴 공고가 떴어요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Today's Pick")
            # 피드 아이템 1 (카드 UI)
            st.markdown(f"""
            <div class="feed-card">
                <span class="tag">인턴십</span>
                <h4>[카카오] {st.session_state.user_info['target_job']} 채용 연계형 인턴 모집</h4>
                <p style="color:#666; font-size:14px;">서류 마감까지 D-3 | 예상 합격률: <span style="color:#4CAF50; font-weight:bold;">높음</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # 피드 아이템 2
            st.markdown("""
            <div class="feed-card">
                <span class="tag">꿀팁</span>
                <h4>합격 자소서 50개 뜯어보고 발견한 공통점 (PDF 무료 배포)</h4>
                <p style="color:#666; font-size:14px;">조회수 1.2k | 좋아요 450</p>
            </div>
            """, unsafe_allow_html=True)

            # 피드 아이템 3
            st.markdown(f"""
            <div class="feed-card">
                <span class="tag">멘토링</span>
                <h4>{st.session_state.user_info['target_job']} 현직자 커피챗 모집 (선착순)</h4>
                <p style="color:#666; font-size:14px;">무료 신청 가능</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("실시간 랭킹")
            st.write("1. 🥇 삼성전자 DS부문")
            st.write("2. 🥈 SK하이닉스")
            st.write("3. 🥉 네이버 웹툰")
            st.divider()
            st.write("📅 **이번 달 일정**")
            st.success("2/14: 토익 시험 접수")
            st.warning("2/20: 삼성전자 공채 시작(예상)")

    # [메인 화면 2] 나의 로드맵 / 전략 (분석 결과)
    elif menu == "🗺️ 나의 로드맵/전략":
        track = st.session_state.user_info['track']
        
        # --- 저학년용 로드맵 ---
        if track == 'Junior':
            st.title("🗺️ 커리어 가이드라인 (Roadmap)")
            st.info(f"{st.session_state.user_info['target_job']} 전문가가 되기 위한 최적의 경로입니다.")
            
            tab1, tab2, tab3 = st.tabs(["1~2학년 (현재)", "3학년 (준비)", "4학년 (실전)"])
            
            with tab1:
                st.markdown("### 🌱 Foundation Phase")
                st.markdown("""
                - [x] **학점 관리:** 전공 기초 과목 3.8 이상 유지
                - [ ] **동아리:** 교내 마케팅/창업 동아리 가입 (이번 달 리크루팅!)
                - [ ] **자격증:** 컴퓨터활용능력 1급 (여름방학 추천)
                """)
                st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=100, caption="성장 중")
            
            with tab2:
                st.markdown("### 🌿 Experience Phase")
                st.write("직무 경험을 쌓아야 하는 시기입니다.")
                st.write("- 산학협력 인턴십 도전")
                st.write("- 교외 공모전 1회 수상 목표")

        # --- 고학년용 전략 분석 ---
        else:
            st.title("📊 Gap Analysis & Strategy")
            st.info(f"{st.session_state.user_info['target_job']} 직무 합격을 위한 전략 리포트입니다.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("나의 강점/약점")
                st.success("👍 **강점:** 관련 인턴 경험 1회, 높은 어학 성적")
                st.error("👎 **약점:** 직무 관련 자격증 부재, 프로젝트 포트폴리오 미흡")
            
            with col2:
                # 레이더 차트 (가상 데이터)
                chart_data = pd.DataFrame({
                    "항목": ["학점", "어학", "직무경험", "자격증", "수상"],
                    "나의 점수": [80, 90, 70, 40, 50],
                    "합격자 평균": [85, 85, 60, 80, 60]
                })
                st.bar_chart(chart_data.set_index("항목"))

            st.divider()
            st.markdown("### 💡 AI 전략 제안")
            st.markdown(f"""
            1. **단기 전략 (1개월):** 부족한 자격증(ADsP, SQLD)을 최우선으로 취득하세요.
            2. **자소서 전략:** 인턴 경험에서 있었던 '문제 해결 에피소드'를 강조하세요. (키워드: 데이터, 협업)
            3. **추천 기업:** {st.session_state.user_info['target_job']} 직무를 수시 채용 중인 **원티드, 토스**에 지원해보세요.
            """)

    elif menu == "📂 내 서류함":
        st.title("📂 내 서류함")
        st.write("업로드한 이력서와 자소서 관리 페이지입니다. (준비 중)")

    elif menu == "⚙️ 설정":
        st.title("설정")
        if st.button("로그아웃"):
            st.session_state.step = 1
            st.rerun()
