import streamlit as st
import pandas as pd
import time
import datetime

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="Career Map v5.1", page_icon="🧭", layout="wide")

# 세션 상태 관리
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1:입력 -> 2:트랙선택 -> 3:상세 -> 4:대시보드
if 'user_info' not in st.session_state:
    st.session_state.user_info = {} # 유저 정보를 담을 딕셔너리

# 스타일링 (카드 UI 및 폼 스타일)
st.markdown("""
    <style>
    .main {background-color: #F8F9FA;}
    h1, h2, h3 {color: #1A237E; font-family: 'Pretendard', sans-serif;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 8px; width: 100%; height: 45px;}
    
    /* 대시보드 카드 스타일 */
    .feed-card {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px;
        border: 1px solid #E0E0E0; transition: transform 0.2s;
    }
    .feed-card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .tag { background-color: #E3F2FD; color: #1565C0; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# STEP 1: 로그인 및 회원가입 (Personal Info)
# ==========================================
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; margin-top: 50px;'>🧭 Career Map</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>불확실한 미래를 데이터로 확신하다.</p>", unsafe_allow_html=True)
        st.write("")
        
        # 탭 분리 (로그인 / 회원가입)
        tab1, tab2 = st.tabs(["로그인", "회원가입 (필수)"])
        
        # [Tab 1] 로그인 (기존 회원용 - MVP에선 시늉만)
        with tab1:
            with st.container(border=True):
                login_id = st.text_input("아이디", key="login_id")
                login_pw = st.text_input("비밀번호", type="password", key="login_pw")
                if st.button("로그인"):
                    if login_id:
                        st.session_state.user_info['name'] = login_id + "님" # 임시 이름
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.warning("아이디를 입력해주세요.")

        # [Tab 2] 회원가입 (신규 유저용 - 여기가 메인)
        with tab2:
            st.info("👋 정확한 진단을 위해 기본 정보를 입력해주세요.")
            with st.form("signup_form"):
                # 1. 계정 정보
                st.markdown("##### 1️⃣ 계정 정보")
                new_id = st.text_input("아이디 (ID)")
                new_pw = st.text_input("비밀번호 (Password)", type="password")
                
                # 2. 인적 사항
                st.markdown("##### 2️⃣ 인적 사항")
                col_a, col_b = st.columns(2)
                with col_a:
                    name = st.text_input("성명")
                    gender = st.selectbox("성별", ["남성", "여성", "기타"])
                with col_b:
                    dob = st.date_input("생년월일", min_value=datetime.date(1990, 1, 1), value=datetime.date(2002, 1, 1))
                    phone = st.text_input("휴대폰 번호", placeholder="010-0000-0000")
                
                email = st.text_input("이메일 (결과 리포트 발송용)")
                
                st.markdown("---")
                submit_btn = st.form_submit_button("가입하고 진단 시작하기 🚀")
                
                if submit_btn:
                    if new_id and new_pw and name and phone:
                        # 정보 저장 (Session State)
                        st.session_state.user_info = {
                            'id': new_id,
                            'name': name,
                            'gender': gender,
                            'dob': str(dob),
                            'phone': phone,
                            'email': email
                        }
                        st.success("가입이 완료되었습니다!")
                        time.sleep(1)
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error("필수 정보를 모두 입력해주세요.")

# ==========================================
# STEP 2: 트랙 선택 (Track Selection)
# ==========================================
elif st.session_state.step == 2:
    # 저장된 이름 불러오기
    user_name = st.session_state.user_info.get('name', '사용자')
    
    st.title(f"{user_name}님, 환영합니다! 👋")
    st.subheader("현재 상황에 맞는 트랙을 선택하세요.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🐣 저학년 (1~2학년)")
            st.write("진로 탐색 및 로드맵 설계")
            if st.button("저학년 트랙 선택"):
                st.session_state.user_info['track'] = 'Junior'
                st.session_state.step = 3
                st.rerun()
                
    with col2:
        with st.container(border=True):
            st.markdown("### 🦅 고학년 (3~4학년/취준)")
            st.write("취업 합격 예측 및 스펙 진단")
            if st.button("고학년 트랙 선택"):
                st.session_state.user_info['track'] = 'Senior'
                st.session_state.step = 3
                st.rerun()

# ==========================================
# STEP 3: 상세 진단 & 파일 업로드
# ==========================================
elif st.session_state.step == 3:
    track = st.session_state.user_info.get('track', 'Senior')
    st.title("🧩 맞춤형 설계를 위한 추가 정보")
    
    # 공통 질문
    col1, col2 = st.columns(2)
    with col1:
        univ = st.text_input("소속 대학", placeholder="예: 연세대학교")
    with col2:
        major = st.text_input("전공", placeholder="예: 경제학과")

    target_job = st.text_input("관심 직무/분야 (필수)", placeholder="예: 마케팅, 데이터 분석, 금융권 등")
    
    st.write("")
    st.markdown("### 🕵️ 정밀 진단 (선택 사항)")
    
    # 인성/성향 검사
    with st.expander("🧠 간단 성향/인성 검사 진행하기"):
        st.radio("1. 새로운 문제를 마주했을 때 나는?", ["논리적으로 분석한다", "직관적으로 해결책을 찾는다", "주변에 조언을 구한다"])
        st.radio("2. 선호하는 업무 환경은?", ["체계적이고 안정적인 곳", "자율적이고 도전적인 곳", "팀워크가 중요한 곳"])
        st.checkbox("진단 결과 반영하기")

    # 파일 업로드
    uploaded_file = st.file_uploader("📂 이력서/자소서 업로드 (PDF)", type=['pdf'])
    
    st.write("")
    if st.button("🚀 나만의 커리어 대시보드 생성하기"):
        if target_job:
            # 추가 정보 업데이트
            st.session_state.user_info.update({
                'univ': univ,
                'major': major,
                'target_job': target_job
            })
            
            # 로딩 연출
            progress_text = "AI가 회원님의 성향과 스펙을 분석 중입니다..."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)
            
            st.session_state.step = 4
            st.rerun()
        else:
            st.warning("관심 직무는 필수 입력 사항입니다.")

# ==========================================
# STEP 4: 메인 대시보드
# ==========================================
elif st.session_state.step == 4:
    
    user_name = st.session_state.user_info.get('name', 'User')
    target_job = st.session_state.user_info.get('target_job', '마케팅')
    univ = st.session_state.user_info.get('univ', '대학교')
    
    # [사이드바]
    with st.sidebar:
        st.title("🧭 Career Map")
        st.write(f"**{user_name}**님")
        st.caption(f"{univ} | {st.session_state.user_info.get('track', 'Type')}")
        st.divider()
        menu = st.radio("MENU", ["🏠 홈 (Feed)", "🗺️ 나의 로드맵/전략", "📂 내 서류함", "⚙️ 설정"])

    # [메인 화면 1] 홈 (뉴스피드)
    if menu == "🏠 홈 (Feed)":
        st.header(f"🔥 {target_job} 분야 트렌드")
        
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #4A90E2 0%, #00E676 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
            <h3>📢 {user_name}님을 위한 추천 공고</h3>
            <p>회원님의 스펙과 <b>92% 일치</b>하는 인턴 공고가 떴어요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Today's Pick")
            st.markdown(f"""
            <div class="feed-card">
                <span class="tag">인턴십</span>
                <h4>[채용연계] {target_job} 직무 인턴 모집</h4>
                <p style="color:#666; font-size:14px;">마감 D-3 | 적합도: <span style="color:#4CAF50; font-weight:bold;">매우 높음</span></p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="feed-card">
                <span class="tag">꿀팁</span>
                <h4>현직자가 말하는 자소서 필승 키워드 5가지</h4>
                <p style="color:#666; font-size:14px;">조회수 1.5k</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("실시간 랭킹")
            st.write("1. 🥇 삼성전자")
            st.write("2. 🥈 SK하이닉스")
            st.write("3. 🥉 현대자동차")

    # [메인 화면 2] 로드맵/전략
    elif menu == "🗺️ 나의 로드맵/전략":
        track = st.session_state.user_info.get('track', 'Senior')
        
        if track == 'Junior':
            st.title("🗺️ 커리어 로드맵 (1~2학년)")
            st.info(f"{target_job} 직무를 위한 학년별 가이드입니다.")
            tab1, tab2 = st.tabs(["Foundation (기초)", "Experience (경험)"])
            with tab1:
                st.checkbox("학점 3.8+ 관리", value=True)
                st.checkbox("교내 학회/동아리 탐색")
            with tab2:
                st.checkbox("직무 관련 자격증 취득")
                st.checkbox("방학 인턴십 지원")
                
        else: # Senior
            st.title("📊 합격 전략 리포트")
            st.info(f"{target_job} 직무 합격을 위한 Gap 분석입니다.")
            col1, col2 = st.columns(2)
            with col1:
                st.success("👍 **강점:** 관련 경험 보유")
                st.error("👎 **약점:** 자격증 부족")
            with col2:
                chart_data = pd.DataFrame({
                    "항목": ["학점", "어학", "경험", "자격증"],
                    "점수": [80, 85, 70, 40]
                })
                st.bar_chart(chart_data.set_index("항목"))

    elif menu == "📂 내 서류함":
        st.title("📂 내 서류함")
        st.info("준비 중인 기능입니다.")

    elif menu == "⚙️ 설정":
        st.title("설정")
        st.write(f"ID: {st.session_state.user_info.get('id', '-')}")
        st.write(f"Email: {st.session_state.user_info.get('email', '-')}")
        if st.button("로그아웃"):
            st.session_state.step = 1
            st.rerun()
