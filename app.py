import streamlit as st
import pandas as pd
import time
import datetime
import random
import graphviz

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="Career Map v7.5 (Wayble Update)", page_icon="🧭", layout="wide")

# 세션 상태 관리
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

# [회원가입 상태 관리용 변수]
if 'signup_status' not in st.session_state:
    st.session_state.signup_status = {
        'phone_verified': False,
        'id_checked': False,
        'auth_sent': False
    }

if 'diary_logs' not in st.session_state:
    st.session_state.diary_logs = [
        {"date": "2026-02-01", "q": "오늘 가장 뿌듯했던 일은?", "a": "사수님께 엑셀 정리 잘했다고 칭찬받음! VLOOKUP 드디어 마스터했다."},
        {"date": "2026-02-02", "q": "오늘 실수한 점이 있다면?", "a": "메일 참조(CC)에 팀장님을 빼먹었다... 다음엔 꼭 더블체크 하자."}
    ]
if 'diary_streak' not in st.session_state:
    st.session_state.diary_streak = 3

# ==============================================================================
# 🎨 Design System (Clubmate Theme: Soft Azure & Sunny Yellow) - [유지]
# ==============================================================================
st.markdown("""
    <style>
    /* 1. 폰트 및 기본 배경 */
    @import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard.css");
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
        color: #333333; /* Text Black */
    }
    
    /* 전체 배경: 아주 연한 블루 그레이 */
    .stApp {
        background-color: #F7F9FC;
    }

    /* 2. 타이포그래피 */
    h1, h2, h3 {
        color: #2C3E50;
        font-weight: 700;
    }
    p {
        color: #546E7A;
        line-height: 1.6;
    }

    /* 3. 버튼 (Primary: Soft Azure) */
    .stButton > button {
        background-color: #4A90E2 !important; /* Clubmate Blue */
        color: #FFFFFF !important; /* 텍스트 완전 흰색 강제 */
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 10px rgba(74, 144, 226, 0.2);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #357ABD !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(74, 144, 226, 0.3);
    }
    .stButton > button:active {
        color: #FFFFFF !important;
        background-color: #2a65a0 !important;
    }
    .stButton > button p {
        color: #FFFFFF !important;
    }
    
    /* 로그인 페이지용 작은 버튼 스타일 */
    .small-btn > button {
        background-color: #ECEFF1 !important;
        color: #546E7A !important;
        border: 1px solid #CFD8DC !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-size: 14px !important;
        box-shadow: none !important;
        height: auto !important;
    }
    .small-btn > button:hover {
        background-color: #CFD8DC !important;
        color: #37474F !important;
        transform: none !important;
    }
    
    /* 4. 카드 디자인 */
    .feed-card, .metric-box, .ai-box, .generator-box {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E3F2FD;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .feed-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(74, 144, 226, 0.15);
        border-color: #4A90E2;
        cursor: pointer;
    }

    /* 5. 다이어리 카드 */
    .diary-card {
        background-color: #FFFDE7;
        padding: 20px;
        border-radius: 16px;
        border-left: 5px solid #FFD54F;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* 6. 태그 및 뱃지 */
    .tag {
        display: inline-block;
        background-color: #E3F2FD;
        color: #4A90E2;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    
    /* 7. 그라데이션 배너 */
    .banner-gradient {
        background: linear-gradient(135deg, #4A90E2 0%, #64B5F6 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(74, 144, 226, 0.25);
    }
    .banner-gradient h2 { color: white !important; }
    .banner-gradient p { color: rgba(255,255,255, 0.95) !important; }

    /* 8. 입력창 스타일 */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #CFD8DC;
        padding: 10px 12px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4A90E2;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
    }
    
    /* 9. 사이드바 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E1E8EE;
    }
    
    /* 10. 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #4A90E2 !important;
        border-color: #4A90E2 !important;
    }
    
    /* 11. 기타 포인트 컬러 */
    .success-text {
        color: #2E7D32;
        font-size: 13px;
        font-weight: 500;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# STEP 1: 로그인 및 회원가입 (유지)
# ==========================================
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("")
        st.write("")
        st.markdown("<h1 style='text-align: center; font-size: 50px;'>🧭</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color:#4A90E2;'>Career Map</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #78909C;'>대학생을 위한 데이터 기반 커리어 네비게이션</p>", unsafe_allow_html=True)
        st.write("")
        
        tab1, tab2 = st.tabs(["로그인", "회원가입"])
        
        # [Tab 1] 로그인
        with tab1:
            with st.container(border=True):
                login_id = st.text_input("아이디", key="login_id", placeholder="ID를 입력하세요")
                login_pw = st.text_input("비밀번호", type="password", key="login_pw", placeholder="비밀번호를 입력하세요")
                st.write("")
                if st.button("시작하기"):
                    if login_id:
                        # 로그인 성공 시 기존 회원 데이터 로드 시뮬레이션 -> 바로 Step 4로 이동
                        st.session_state.user_info = {
                            'id': login_id,
                            'name': login_id + "님",
                            'track': 'Senior', # 기본값 (테스트용)
                            'univ': '연세대학교',
                            'major': '경영학과',
                            'target_job': 'PM/서비스기획',
                            'test_keyword': '전략가형 (Strategic)',
                            'visa_type': 'D-2',
                            'topik': 'Level 5'
                        }
                        st.session_state.step = 4 # 대시보드로 직행
                        st.rerun()
                    else:
                        st.warning("아이디를 입력해주세요.")

        # [Tab 2] 회원가입
        with tab2:
            st.markdown("#### 환영합니다! 👋\n**당신의 취업을 진심으로 응원해요**")
            st.write("")
            
            with st.container(border=True):
                st.caption("이름")
                name = st.text_input("이름", label_visibility="collapsed", placeholder="실명을 입력해주세요")
                st.write("")
                
                col_birth, col_gender = st.columns([2, 1])
                with col_birth:
                    st.caption("생년월일 8자리 (예: 20020922)")
                    dob_input = st.text_input("생년월일", label_visibility="collapsed", placeholder="2002.09.22")
                with col_gender:
                    st.caption("성별")
                    gender = st.radio("성별", ["남자", "여자"], label_visibility="collapsed", horizontal=True)

                st.write("")
                st.caption("휴대폰 번호")
                c_p1, c_p2 = st.columns([3, 1])
                with c_p1:
                    phone = st.text_input("휴대폰 번호", label_visibility="collapsed", placeholder="010-0000-0000")
                with c_p2:
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("인증"):
                          st.session_state.signup_status['auth_sent'] = True
                          st.toast("인증번호가 발송되었습니다. (1234)", icon="📩")
                    st.markdown('</div>', unsafe_allow_html=True)

                if st.session_state.signup_status['auth_sent']:
                    c_a1, c_a2 = st.columns([3, 1])
                    with c_a1:
                        auth_code = st.text_input("인증번호", placeholder="인증번호 4자리", label_visibility="collapsed")
                    with c_a2:
                        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                        if st.button("확인"):
                            if auth_code == "1234":
                                st.session_state.signup_status['phone_verified'] = True
                            else:
                                st.error("인증번호가 틀렸습니다.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    if st.session_state.signup_status['phone_verified']:
                        st.markdown('<p class="success-text">✅ 인증이 완료되었어요.</p>', unsafe_allow_html=True)
                
                st.write("")
                st.caption("이메일")
                email = st.text_input("이메일", label_visibility="collapsed", placeholder="example@yonsei.ac.kr")
                st.caption("* 입사제안, 전형안내 등 중요한 메일 수신에 사용되므로 정확히 입력해주세요.")

                st.write("")
                st.divider()
                st.write("")

                st.caption("아이디")
                c_id1, c_id2 = st.columns([3, 1])
                with c_id1:
                    new_id = st.text_input("아이디 입력", label_visibility="collapsed", placeholder="영문, 숫자 포함 6-12자")
                with c_id2:
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("중복확인"):
                        if len(new_id) > 0:
                            st.session_state.signup_status['id_checked'] = True
                        else:
                            st.warning("입력필요")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if st.session_state.signup_status['id_checked']:
                    st.markdown('<p class="success-text">✅ 사용 가능한 아이디에요.</p>', unsafe_allow_html=True)

                st.write("")
                st.caption("비밀번호")
                new_pw = st.text_input("비밀번호", type="password", label_visibility="collapsed", placeholder="비밀번호 입력")
                st.caption("비밀번호 재확인")
                new_pw2 = st.text_input("비밀번호 재확인", type="password", label_visibility="collapsed", placeholder="비밀번호 다시 입력")

                if new_pw and new_pw2:
                    if new_pw == new_pw2:
                        st.markdown('<p class="success-text">✅ 비밀번호가 일치해요.</p>', unsafe_allow_html=True)
                    else:
                        st.markdown('<p style="color:#D32F2F; font-size:13px;">❌ 비밀번호가 일치하지 않습니다.</p>', unsafe_allow_html=True)

                st.write("")
                st.divider()
                
                agree_all = st.checkbox("모든 약관 사항에 전체 동의합니다.")
                val_serv = True if agree_all else False
                val_priv = True if agree_all else False
                
                if not agree_all:
                    c_t1, c_t2 = st.columns([0.1, 0.9])
                    agree_service = st.checkbox("서비스 이용약관 동의 (필수)")
                    agree_privacy = st.checkbox("개인정보 수집 및 이용 동의 (필수)")
                    agree_marketing = st.checkbox("마케팅 정보 수신 동의 (선택)")
                    val_serv = agree_service
                    val_priv = agree_privacy

                st.write("")
                st.write("")
                
                submit_btn = st.button("가입하고 진단 시작하기 🚀")
                
                if submit_btn:
                    if not name or not phone or not new_id or not new_pw:
                        st.error("필수 정보를 모두 입력해주세요.")
                    elif not st.session_state.signup_status['phone_verified']:
                        st.error("휴대폰 인증을 완료해주세요.")
                    elif not st.session_state.signup_status['id_checked']:
                        st.error("아이디 중복확인을 해주세요.")
                    elif new_pw != new_pw2:
                        st.error("비밀번호가 일치하지 않습니다.")
                    elif not (val_serv and val_priv):
                        st.error("필수 약관에 동의해주세요.")
                    else:
                        st.session_state.user_info = {
                            'id': new_id, 'name': name, 'gender': gender, 
                            'dob': dob_input, 'phone': phone, 'email': email
                        }
                        st.success("가입이 완료되었습니다!")
                        time.sleep(1)
                        st.session_state.step = 2 # 신규 가입자는 Step 2로 이동
                        st.rerun()

# ==========================================
# STEP 2: 트랙 선택 (유지)
# ==========================================
elif st.session_state.step == 2:
    user_name = st.session_state.user_info.get('name', '사용자')
    st.title(f"반가워요, {user_name}! 👋")
    st.subheader("어떤 도움이 필요하신가요?")
    
    tab_kor, tab_glo = st.tabs(["🇰🇷 내국인 (Korean)", "🌏 외국인 유학생 (Global)"])
    
    # 1. 내국인 트랙
    with tab_kor:
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.markdown("### 🐣 저학년 (1~2학년)")
                st.write("아직 구체적인 진로를 정하지 못했어요.")
                st.write("")
                st.markdown("""
                <div style='background-color:#F5F5F5; padding:15px; border-radius:12px; font-size:14px; color:#546E7A;'>
                ✅ <b>커리어 성향(DNA) 진단</b><br>
                ✅ <b>학년별 필수 로드맵</b><br>
                ✅ <b>대외활동 추천</b>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
                if st.button("저학년 트랙 시작", key="btn_junior"):
                    st.session_state.user_info['track'] = 'Junior'
                    st.session_state.step = 2.5 
                    st.rerun()
        with col2:
            with st.container(border=True):
                st.markdown("### 🦅 고학년 (3~4학년/취준)")
                st.write("목표 직무가 있고, 합격이 목표예요.")
                st.write("")
                st.markdown("""
                <div style='background-color:#F5F5F5; padding:15px; border-radius:12px; font-size:14px; color:#546E7A;'>
                ✅ <b>이력서/자소서 AI 분석</b><br>
                ✅ <b>합격 확률 시뮬레이션</b><br>
                ✅ <b>부족한 스펙(Gap) 진단</b>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
                if st.button("고학년 트랙 시작", key="btn_senior"):
                    st.session_state.user_info['track'] = 'Senior'
                    st.session_state.step = 2.5 
                    st.rerun()

    # 2. 외국인 트랙
    with tab_glo:
        st.write("")
        st.markdown("""
        <div style="background-color:#E3F2FD; border: 1px solid #4A90E2; padding: 15px; border-radius: 12px; color: #1565C0; margin-bottom: 20px;">
        💡 <b>For International Students:</b> Visa(E-7) & Career Solution
        </div>
        """, unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns([1, 2])
        with col_g1:
            st.markdown("<div style='font-size:100px; text-align:center;'>🌏</div>", unsafe_allow_html=True)
        with col_g2:
            st.markdown("### Global Talent Track")
            st.write("한국 취업을 목표로 하는 유학생을 위한 비자 & 커리어 통합 솔루션입니다.")
            st.markdown("""
            - 🛂 **Visa Roadmap:** D-2 $\rightarrow$ D-10 $\rightarrow$ E-7 비자 취득 확률 분석
            - 🗣️ **Korean Skill:** TOPIK 점수 기반 직무 추천
            - 🏢 **Company Match:** 외국인 채용 우대 기업 매칭
            """)
            st.write("")
            if st.button("Start Global Track 🚀", key="btn_global"):
                st.session_state.user_info['track'] = 'Global'
                st.session_state.step = 2.5 
                st.rerun()

# ==========================================
# STEP 2.5: 상세 정보 수집 (유지)
# ==========================================
elif st.session_state.step == 2.5:
    st.title("📝 상세 정보 입력")
    st.markdown("나에게 **딱 맞는 맞춤 포지션**을 제안받기 위해 정보를 입력해주세요.")
    st.write("")
    st.progress(50) 

    with st.form("onboarding_form"):
        
        st.subheader("1. 소속 정보")
        col_univ, col_major = st.columns(2)
        with col_univ:
            univ = st.text_input("소속 대학", placeholder="예: 연세대학교")
        with col_major:
            major = st.text_input("전공", placeholder="예: 경제학과")
        
        st.write("")

        st.subheader("2. 학적 상태")
        col_ac1, col_ac2, col_ac3 = st.columns(3)
        with col_ac1:
            grade = st.selectbox("현재 학년", ["1학년", "2학년", "3학년", "4학년", "졸업유예/수료", "졸업"])
        with col_ac2:
            semester = st.selectbox("현재 학기", ["1학기", "2학기", "휴학 중"])
        with col_ac3:
            status = st.selectbox("학적 상태", ["재학", "휴학", "수료", "졸업"])
            
        col_cr1, col_cr2 = st.columns(2)
        with col_cr1:
            earned_credits = st.number_input("현재 이수 학점", min_value=0, max_value=200, value=0)
        with col_cr2:
            goal_credits = st.number_input("졸업 기준 학점", min_value=0, max_value=200, value=130)

        st.divider()

        st.subheader("3. 희망 직군")
        st.caption("관심있는 직무 분야를 선택해주세요. (복수 선택 가능)")
        
        job_categories = [
            "경영기획·지원", "홍보·마케팅", "영업", 
            "생산·유통·품질", "건설 엔지니어", "연구·개발", 
            "IT 서비스", "디자인", "금융·보험",
            "서비스·고객지원", "의료·보건", "개발"
        ]
        
        selected_categories = st.multiselect("희망 직군 선택", job_categories, placeholder="직군을 선택해주세요")
        
        detailed_job = ""
        if selected_categories:
            st.caption("선택한 직군 내 상세 직무 (예시)")
            detailed_job = st.text_input("상세 희망 직무 (직접 입력)", placeholder="예: 콘텐츠 마케터, 백엔드 개발자")

        st.divider()

        st.subheader("4. 근무 조건")
        
        st.markdown("##### 경력 여부")
        career_type = st.radio("경력 여부", 
                 ["신입 (인턴 포함)", "경력 (1년 이상)"], 
                 horizontal=True, label_visibility="collapsed")
        
        st.write("")
        
        st.markdown("##### 희망 근무 지역")
        locations = ["전체", "서울", "경기", "인천", "대전", "부산", "대구", "광주", "울산", "세종", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]
        selected_loc = st.multiselect("지역 선택", locations, default=["서울"])
        
        st.write("")
        
        st.markdown("##### 희망 근무 조건 (자유 입력)")
        st.caption("금융, IT 등 선호 업종이나 기업 형태(스타트업, 대기업), 연봉 조건 등을 자유롭게 적어주세요.")
        work_cond = st.text_area("조건 입력", height=150, 
                                 placeholder="(예시)\n'스타트업에서 일하는 것도 괜찮아요.'\n'경기남부와 서울 강남권을 선호해요.'\n'최소 연봉은 4천 이상이면 좋겠어요.'")

        st.write("")
        submit_onboarding = st.form_submit_button("입력 완료 및 진단 시작하기")
        
        if submit_onboarding:
            st.session_state.user_info.update({
                'univ': univ,
                'major': major,
                'grade': grade,
                'semester': semester,
                'status': status,
                'earned_credits': earned_credits,
                'job_categories': selected_categories,
                'target_job': detailed_job if detailed_job else "미정",
                'career_type': career_type,
                'locations': selected_loc,
                'work_cond': work_cond
            })
            st.success("정보가 저장되었습니다!")
            time.sleep(1)
            st.session_state.step = 3
            st.rerun()

# ==========================================
# STEP 3: 상세 진단 (유지)
# ==========================================
elif st.session_state.step == 3:
    track = st.session_state.user_info.get('track', 'Senior')
    st.title("🧩 데이터 연동 및 진단")
    st.write("더 정확한 분석을 위해 역량 데이터를 연동합니다.")
    st.write("")

    # [Branch] 외국인 트랙
    if track == 'Global':
        st.info("🌏 **Global User Additional Info**")
        col1, col2 = st.columns(2)
        with col1:
            visa_type = st.selectbox("Current Visa (현재 비자)", ["D-2 (유학)", "D-10 (구직)", "E-7 (취업)", "F-series"])
        with col2:
            topik = st.selectbox("TOPIK Level (한국어 급수)", ["Level 1~2 (Basic)", "Level 3~4 (Intermediate)", "Level 5~6 (Advanced)"])
        
        st.write("")
        st.markdown("### 🧬 Soft Skill Analysis (AI Test)")
        has_test = st.radio("Do you have AI Competency Test results?", ["Yes, I have.", "No, I don't."], horizontal=True)
        test_keyword = "Global Talent"
        
        if has_test == "Yes, I have.":
            st.file_uploader("Upload Result (PDF)", type=['pdf'])
        else:
            st.write("Simple Diagnosis:")
            st.radio("Your Work Style", ["Individual Focus", "Team Collaboration"])
            
        st.write("")
        if st.button("🚀 Analyze Visa & Career"):
            st.session_state.user_info.update({
                'test_keyword': test_keyword,
                'visa_type': visa_type, 'topik': topik
            })
            time.sleep(1)
            st.session_state.step = 4
            st.rerun()

    # [Branch] 내국인 트랙
    else: 
        st.markdown("### 1. 성향/역량 분석 (Soft Skill)")
        
        # 1-1. AI 정밀 진단 여부 확인 (Yes/No)
        st.write("#### Q. Career Map AI 정밀 진단을 받아보시겠어요?")
        
        current_test_key = st.session_state.user_info.get('test_keyword', '미입력')
        is_done = current_test_key not in ['미입력', '선택해주세요']
        
        if is_done:
             st.success(f"✅ Career Map AI 진단 완료: **{current_test_key}**")
             if st.button("🔄 다시 진단하기", key="retake_btn"):
                 st.session_state.user_info['test_keyword'] = '미입력'
                 st.rerun()
        
        else:
            diagnosis_decision = st.radio("진단 여부 선택", 
                                          ["선택해주세요", "네, 받아볼래요. (추천)", "아니요, 괜찮습니다."], 
                                          index=0, horizontal=True, label_visibility="collapsed")
            
            if diagnosis_decision == "네, 받아볼래요. (추천)":
                st.markdown("""
                <div style="background-color:#E3F2FD; padding:20px; border-radius:12px; border:1px solid #90CAF9; margin-top:10px;">
                    <h4 style="color:#1565C0; margin-top:0;">🤖 AI 커리어 성향 진단</h4>
                    <p style="color:#424242; font-size:14px;">
                    20개의 문항을 통해 나의 <b>업무 스타일, 소통 방식, 강점</b>을 정밀하게 분석합니다.<br>
                    진단 결과는 로드맵 설계에 자동으로 반영됩니다. (소요시간: 약 3분)
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
                if st.button("👉 AI 진단 시작하기 (새 페이지로 이동)"):
                    st.session_state.step = 3.5 
                    st.rerun()

        st.write("")
        st.divider()
        st.write("")

        # 1-2. 외부 결과 업로드
        st.markdown("#### Q. 외부 역량검사(마이다스, 잡다 등) 결과표가 있으신가요? (선택)")
        st.caption("결과표(PDF)를 업로드하면 해당 데이터를 기반으로 더 정교하게 분석합니다.")
        
        st.file_uploader("검사 결과표 업로드", type=['pdf', 'jpg', 'png'])
        st.selectbox("결과표의 핵심 성향 키워드를 선택해주세요", 
                         ["선택해주세요", "전략가형 (Strategic)", "분석가형 (Analytical)", "소통가형 (Social)", "개척자형 (Challenger)"], key="external_key")

        st.write("")
        st.divider()
        st.write("")

        # 2. 이력서/자소서 분석
        st.markdown("### 2. 이력서/경험 분해 (Hard Skill)")
        st.markdown("""
        <div style="border: 2px solid #4A90E2; border-radius: 12px; padding: 20px; background-color: #FDFEFF;">
            <h4 style="color: #4A90E2; margin-top: 0;">✨ New Feature: AI 이력서 분석</h4>
            <p style="font-size: 14px; color: #555;">
            이미 작성해둔 <b>이력서</b>나 <b>자기소개서</b>가 있으신가요?<br>
            파일을 업로드하면 AI가 <b>직무 역량(Hard Skill)</b>과 <b>프로젝트 경험</b>을 자동으로 추출하여 내 프로필에 등록합니다.
            </p>
            <div style="margin-top: 15px;">
        """, unsafe_allow_html=True)
        
        uploaded_resume = st.file_uploader("이력서/자소서 파일 업로드", type=['pdf', 'docx', 'hwp'], key="resume_upload")
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        
        if st.button("🚀 AI 통합 분석 시작하기", type="primary"):
            final_key = st.session_state.user_info.get('test_keyword', '미입력')
            external_key_val = st.session_state.get('external_key', '선택해주세요')
            
            if final_key in ['미입력', '선택해주세요']:
                if external_key_val != '선택해주세요':
                    st.session_state.user_info['test_keyword'] = external_key_val
                else:
                    st.session_state.user_info['test_keyword'] = "전략가형 (Strategic)" # Default
            
            progress_text = "성향(Soft Skill)과 이력서(Hard Skill) 데이터를 결합 중입니다..."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.02)
                my_bar.progress(percent_complete + 1)
            
            st.session_state.step = 4
            st.rerun()

# ==========================================
# STEP 3.5: AI 성향 진단 페이지 (유지)
# ==========================================
elif st.session_state.step == 3.5:
    st.title("🧬 AI 커리어 성향 진단")
    st.markdown("**솔직하게 답변해주세요.** 정답은 없습니다.")
    
    questions = [
        ("Q1. 새로운 프로젝트를 시작할 때, 나는?", ["철저하게 계획을 세우고 시작한다.", "일단 부딪혀보며 수정해 나간다."]),
        ("Q2. 팀원과 의견이 충돌할 때, 나는?", ["논리적인 근거를 들어 설득한다.", "상대방의 감정을 먼저 살핀다."]),
        ("Q3. 내가 더 선호하는 업무 환경은?", ["조용하고 독립적인 공간", "활발하게 소통하는 개방된 공간"]),
        ("Q4. 예상치 못한 문제가 발생했을 때?", ["원인을 분석하여 근본 해결책을 찾는다.", "빠르게 대안을 찾아 수습부터 한다."]),
        ("Q5. 리더로서 나의 스타일은?", ["명확한 지시와 방향성을 제시한다.", "팀원의 의견을 수렴하여 함께 결정한다."])
    ]
    
    responses = {}
    
    for i, (q, opts) in enumerate(questions):
        st.write("")
        with st.container(border=True):
            st.markdown(f"#### {q}")
            responses[f"q{i+1}"] = st.radio(f"{q} 선택", opts, label_visibility="collapsed", key=f"q_{i}")
            
    st.write("")
    st.write("")
    
    if st.button("진단 결과 제출하기", type="primary"):
        with st.spinner("AI가 성향을 분석 중입니다..."):
            time.sleep(2.0)
            
            count_opt1 = 0
            for i in range(len(questions)):
                if responses[f"q{i+1}"] == questions[i][1][0]:
                    count_opt1 += 1
            
            result_type = "전략가형 (Strategic)" if count_opt1 >= 3 else "소통가형 (Social)"
            
            st.session_state.user_info['test_keyword'] = result_type
            st.success("분석이 완료되었습니다!")
            time.sleep(1)
            st.session_state.step = 3 
            st.rerun()

# ==========================================
# STEP 4: 메인 대시보드
# ==========================================
elif st.session_state.step == 4:
    
    user_name = st.session_state.user_info.get('name', 'User')
    target_job = st.session_state.user_info.get('target_job', 'Business')
    test_key = st.session_state.user_info.get('test_keyword', '미입력')
    track = st.session_state.user_info.get('track', 'Type')
    
    # [사이드바]
    with st.sidebar:
        st.title("🧭 Career Map")
        st.write(f"Hello, **{user_name}**!")
        
        # 트랙에 따른 메뉴 분기
        if track == 'Global':
            st.caption(f"Yonsei Univ. | {track} Track")
            st.info(f"🛂 **Visa Status**\nCurrent: {st.session_state.user_info.get('visa_type', 'D-2')}")
            
            st.divider()
            
            # Global 전용 메뉴
            menu = st.radio("MENU", [
                "🏠 Dashboard", 
                "🛂 Visa Calculator (F-2-7)", 
                "🗺️ Visa Roadmap", 
                "🏢 Visa-Sponsored Jobs", 
                "📝 AI Resume Builder (Eng to Kor)",
                "⚙️ Settings"
            ])
            
        else:
            # 기존 내국인 메뉴 (유지)
            st.caption(f"{st.session_state.user_info.get('univ')} | {track}")
            
            # 뱃지 스타일 (Clubmate Blue)
            if "분석가" in test_key or "전략가" in test_key:
                st.markdown(f"<span class='tag'>🧬 {test_key}</span>", unsafe_allow_html=True)
            elif "소통가" in test_key or "개척자" in test_key:
                st.markdown(f"<span class='tag'>🧬 {test_key}</span>", unsafe_allow_html=True)
            
            st.divider()
            menu = st.radio("MENU", ["🏠 홈 (Feed)", "🗺️ 나의 로드맵/전략", "📝 업무 다이어리", "✍️ AI 자소서 작성", "📂 내 서류함", "⚙️ 설정"])
            st.divider()
            st.info("💡 **Premium**\n현직자 1:1 멘토링 매칭")

    # ----------------------------------------------------------------
    # [Branch 1] Global Track Features (Wayble Benchmarked Upgrade)
    # ----------------------------------------------------------------
    if track == 'Global':
        
        # 1. Dashboard (Main)
        if menu == "🏠 Dashboard":
            st.title(f"Hello, {user_name}! 👋")
            st.caption("Your personalized Visa & Career Dashboard")
            
            # [SECTION A] Status Summary (Wayble Style: Confidence Building)
            # 현재 비자 상태와 목표(E-7/F-2-7)까지의 거리를 시각화
            current_points = 65 # 예시 점수
            target_points = 80
            gap = target_points - current_points
            
            st.markdown(f"""
            <div class="banner-gradient" style="padding: 25px;">
                <h2 style='color:white; margin:0; font-size:24px;'>🛂 Visa Probability: <span style="color:#FFF176;">Safe Zone (85%)</span></h2>
                <p style='margin:5px 0 15px 0; font-size:15px;'>You are currently holding <b>D-2 Visa</b>. Your F-2-7 Point is <b>{current_points} pts</b>.</p>
                <div style="background-color:rgba(255,255,255,0.3); border-radius:10px; height:8px; width:100%;">
                    <div style="background-color:#FFF176; width:{current_points/target_points*100}%; height:100%; border-radius:10px;"></div>
                </div>
                <p style='margin:5px 0 0 0; font-size:12px; text-align:right;'>Target: 80 pts (Gap: {gap})</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_d1, col_d2 = st.columns([1.2, 0.8])
            
            # [SECTION B] Weekly Quests (Action Items)
            with col_d1:
                st.subheader("✅ Weekly Quests")
                st.caption("Complete these to boost your visa points.")
                
                quests = [
                    {"title": "Take TOPIK Mock Test", "desc": "Aim for Level 5 to get +5 pts", "done": False, "tag": "Korean"},
                    {"title": "Complete KIIP Level 4", "desc": "Social Integration Program", "done": True, "tag": "Visa Point"},
                    {"title": "Update Resume (Kor)", "desc": "Use AI Builder for E-7 Jobs", "done": False, "tag": "Career"}
                ]
                
                for q in quests:
                    icon = "✅" if q['done'] else "⬜"
                    opacity = "0.6" if q['done'] else "1.0"
                    st.markdown(f"""
                    <div class="feed-card" style="padding:15px; display:flex; align-items:center; opacity:{opacity};">
                        <div style="font-size:20px; margin-right:15px;">{icon}</div>
                        <div style="flex-grow:1;">
                            <span class="tag" style="font-size:11px;">{q['tag']}</span>
                            <h4 style="margin:5px 0; font-size:16px;">{q['title']}</h4>
                            <p style="margin:0; font-size:13px; color:#666;">{q['desc']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # [SECTION C] Recommended Jobs (Visa Filtered)
            with col_d2:
                st.subheader("🔥 Top Pick for You")
                st.markdown(f"""
                <div class="feed-card" style="border:1px solid #4A90E2;">
                    <span class="tag" style="background-color:#E3F2FD; color:#1565C0;">Visa Sponsored</span>
                    <h4 style="margin: 10px 0;">Global Strategist</h4>
                    <p style="font-weight:600; color:#333; margin-bottom:5px;">Kakao Mobility</p>
                    <p style="color:#546E7A; font-size:13px; margin:0;">
                    • F-series Visa preferred<br>
                    • English Native level
                    </p>
                    <button style="width:100%; margin-top:10px; background-color:#4A90E2; color:white; border:none; padding:8px; border-radius:6px;">View Details</button>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="metric-box" style="padding:15px;">
                    <p style="font-size:14px; font-weight:bold;">📢 Visa News</p>
                    <p style="font-size:12px; margin-bottom:0;">E-7-4 Quota has been increased by 20% this year...</p>
                </div>
                """, unsafe_allow_html=True)

        # 2. Visa Calculator (Interactive & Detailed)
        elif menu == "🛂 Visa Calculator (F-2-7)":
            st.title("🧮 F-2-7 Visa Point Calculator")
            st.caption("Check your eligibility for the Points-Based Resident Visa (F-2-7). You need **80 points** out of 100.")
            
            # Interactive Input Section
            with st.container(border=True):
                st.subheader("1. Base Points")
                c1, c2 = st.columns(2)
                with c1:
                    age_opt = st.selectbox("Age", 
                        ["20-24 (+23)", "25-29 (+25)", "30-34 (+23)", "35-39 (+20)"], index=1)
                    edu_opt = st.selectbox("Education", 
                        ["Bachelor (+10)", "Bachelor(STEM) (+12)", "Master (+15)", "Master(STEM) (+17)", "Ph.D (+20)"], index=0)
                with c2:
                    topik_opt = st.selectbox("Korean (TOPIK/KIIP)", 
                        ["Level 1 (+0)", "Level 2 (+5)", "Level 3 (+10)", "Level 4 (+15)", "Level 5+ (+20)"], index=3)
                    income_opt = st.selectbox("Yearly Income (Expected)", 
                        ["None (Student) (+0)", "Over 30M KRW (+10)", "Over 40M KRW (+20)", "Over 50M KRW (+30)"], index=1)
                
                # Dynamic Calculation Logic
                score = 0
                score += int(age_opt.split('+')[1].replace(')', ''))
                score += int(edu_opt.split('+')[1].replace(')', ''))
                score += int(topik_opt.split('+')[1].replace(')', ''))
                score += int(income_opt.split('+')[1].replace(')', ''))
                
                st.divider()
                
                st.subheader("2. Bonus Points")
                c3, c4 = st.columns(2)
                with c3:
                    kiip = st.checkbox("KIIP Completion (+10)")
                    top_uni = st.checkbox("Times Top 500 Univ. (+15)")
                with c4:
                    korea_edu = st.checkbox("Study in Korea (3yr+) (+10)")
                    volunteer = st.checkbox("Social Volunteer (>1yr) (+3)")
                
                if kiip: score += 10
                if top_uni: score += 15
                if korea_edu: score += 10
                if volunteer: score += 3

                # Result Visualization
                st.write("")
                st.write("")
                st.markdown(f"<h3 style='text-align:center;'>Total Score: <span style='color:#4A90E2;'>{score}</span> / 100</h3>", unsafe_allow_html=True)
                
                # Progress Bar Color Logic
                bar_color = "#4CAF50" if score >= 80 else "#FF9800"
                st.markdown(f"""
                <div style="background-color:#EEE; border-radius:15px; height:20px; width:100%; margin-bottom:10px;">
                    <div style="background-color:{bar_color}; width:{min(score, 100)}%; height:100%; border-radius:15px; transition: width 0.5s;"></div>
                </div>
                """, unsafe_allow_html=True)

                if score >= 80:
                    st.success("🎉 Congratulations! You are eligible to apply for F-2-7.")
                else:
                    needed = 80 - score
                    st.error(f"🚨 You need {needed} more points.")
                    
                    # Gap Analysis (Wayble Style)
                    st.markdown("#### 💡 How to fill the Gap?")
                    st.markdown(f"""
                    <div class="feed-card">
                        <b>Recommendations:</b>
                        <ul>
                            <li>📚 <b>KIIP Program:</b> Easiest way to get +10 points. (Takes 6 months)</li>
                            <li>💰 <b>Income Strategy:</b> Negotiate salary over 30M KRW.</li>
                            <li>🎓 <b>Education:</b> A Master's degree gives you +5 more points.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

        # 3. Visa Roadmap (Graphviz Visualization)
        elif menu == "🗺️ Visa Roadmap":
            st.title("🗺️ Visa Roadmap")
            st.caption("Your strategic timeline from Student to Resident.")
            
            col_r1, col_r2 = st.columns([3, 1])
            with col_r1:
                # Graphviz Flowchart
                visa_map = graphviz.Digraph()
                visa_map.attr(rankdir='LR')
                visa_map.attr('node', shape='box', style='rounded,filled', fontname="sans-serif")
                
                # Nodes
                visa_map.node('D2', 'D-2\n(Student)', fillcolor='#E3F2FD', color='#1565C0')
                visa_map.node('D10', 'D-10\n(Job Seeker)', fillcolor='#FFF9C4', color='#FBC02D')
                visa_map.node('E7', 'E-7\n(Professional)', fillcolor='#C8E6C9', color='#2E7D32')
                visa_map.node('F2', 'F-2-7\n(Resident)', fillcolor='#FFCCBC', color='#D84315', shape='doubleoctagon')
                
                # Edges with Labels
                visa_map.edge('D2', 'D10', label='Graduation')
                visa_map.edge('D10', 'E7', label='Job Contract\n(Matching Major)')
                visa_map.edge('E7', 'F2', label='80 Points\n(After 1-3 yrs)')
                visa_map.edge('D2', 'F2', label='Direct Apply\n(Master + Job)', style='dashed')
                
                st.graphviz_chart(visa_map)
                
            with col_r2:
                st.markdown("#### Current Stage")
                st.markdown("""
                <div class="metric-box" style="border-left:5px solid #1565C0;">
                    <b>STEP 1: D-2</b><br>
                    <span style="font-size:12px;">Maintain GPA & Learn Korean</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("⬇️ Next")
                st.markdown("""
                <div class="metric-box" style="opacity:0.6;">
                    <b>STEP 2: D-10</b><br>
                    <span style="font-size:12px;">Need 60pts to apply</span>
                </div>
                """, unsafe_allow_html=True)

        # 4. Visa-Sponsored Job Board
        elif menu == "🏢 Visa-Sponsored Jobs":
            st.title("🏢 Visa-Sponsored Jobs")
            st.caption("Positions that actively support **E-7 Visa Sponsorship**.")
            
            # Smart Filter
            c_f1, c_f2, c_f3 = st.columns(3)
            with c_f1:
                st.selectbox("Job Function", ["All", "Sales", "IT/Dev", "Marketing"])
            with c_f2:
                st.selectbox("Visa Type", ["E-7 Sponsored", "F-Visa Only"])
            with c_f3:
                st.checkbox("Korean Not Required", value=True)
            
            st.write("")
            
            # Job Listing 1
            st.markdown(f"""
            <div class="feed-card">
                <div style="display:flex; justify-content:space-between;">
                    <span class="tag" style="background-color:#E8F5E9; color:#2E7D32;">✅ E-7 Sponsorship</span>
                    <span style="font-size:12px; color:#888;">D-5</span>
                </div>
                <h3 style="margin:5px 0;">Overseas Sales Manager (Vietnam)</h3>
                <p style="font-weight:bold; color:#555;">Samsung C&T</p>
                <div style="font-size:13px; color:#546E7A; margin-top:5px;">
                    <span>📍 Seoul, Gangnam</span> | <span>💰 45M+ KRW</span>
                </div>
                <hr style="margin:10px 0; border:0; border-top:1px solid #EEE;">
                <p style="font-size:13px; color:#333;">
                <b>Requirements:</b><br>
                • Native Vietnamese speaker<br>
                • TOPIK Level 4 or higher<br>
                • Major in Business/Economics preferred
                </p>
                <button style="width:100%; background-color:#4A90E2; color:white; border:none; padding:8px; border-radius:6px;">Apply Now</button>
            </div>
            """, unsafe_allow_html=True)

            # Job Listing 2
            st.markdown(f"""
            <div class="feed-card">
                <div style="display:flex; justify-content:space-between;">
                    <span class="tag" style="background-color:#FFF3E0; color:#EF6C00;">⚡ Urgent Hiring</span>
                    <span style="font-size:12px; color:#888;">D-1</span>
                </div>
                <h3 style="margin:5px 0;">Content Marketer (English)</h3>
                <p style="font-weight:bold; color:#555;">HyperConnect</p>
                <div style="font-size:13px; color:#546E7A; margin-top:5px;">
                    <span>📍 Seoul, Gangnam</span> | <span>💰 Negotiable</span>
                </div>
                <hr style="margin:10px 0; border:0; border-top:1px solid #EEE;">
                <p style="font-size:13px; color:#333;">
                <b>Requirements:</b><br>
                • Native English speaker<br>
                • Experience in Social Media Marketing<br>
                • F-series Visa holders preferred (E-7 possible for high skilled)
                </p>
                <button style="width:100%; background-color:#4A90E2; color:white; border:none; padding:8px; border-radius:6px;">Apply Now</button>
            </div>
            """, unsafe_allow_html=True)

        # 5. AI Resume Builder (Eng to Kor) - (Existing Logic Kept)
        elif menu == "📝 AI Resume Builder (Eng to Kor)":
            st.title("📝 AI Resume Converter")
            st.write("Convert your English experience into a **Perfect Korean Resume**.")
            
            col_r1, col_r2 = st.columns(2)
            
            with col_r1:
                st.subheader("🇺🇸 Input (English)")
                eng_input = st.text_area("Paste your bullet points here:", height=300, 
                                         placeholder="- Managed social media accounts with 10k followers\n- Analyzed marketing data using Google Analytics")
            
            with col_r2:
                st.subheader("🇰🇷 Output (Korean)")
                if eng_input:
                    if st.button("🔄 Translate & Polish"):
                        with st.spinner("AI is professionalizing your resume..."):
                            time.sleep(2)
                            kor_output = """
- **소셜 미디어 채널 운영 및 성과 관리**: 팔로워 10,000명 규모의 계정을 전담 운영하며 브랜드 인지도 제고
- **데이터 기반 마케팅 성과 분석**: Google Analytics를 활용하여 유입 경로 및 전환율 분석, 마케팅 효율 15% 개선
                            """
                            st.text_area("Korean Result", value=kor_output, height=300)
                            st.success("Done! Copy this to your Korean resume.")
                else:
                    st.info("Waiting for input...")
                    st.text_area("Korean Result", height=300, disabled=True)

        # 6. Settings
        elif menu == "⚙️ Settings":
             st.title("Settings")
             if st.button("Log out"):
                 st.session_state.step = 1
                 st.rerun()

    # ----------------------------------------------------------------
    # [Branch 2] Korean Track Features (기존 코드 유지)
    # ----------------------------------------------------------------
    else:
        
        # [1] 홈 (Feed)
        if menu == "🏠 홈 (Feed)":
            st.header(f"🔥 {target_job} 분야 트렌드")
            
            recomm_text = "회원님의 스펙"
            if "분석가" in test_key or "전략가" in test_key:
                recomm_text = f"회원님의 **{test_key} 성향**과 **스펙**"
            
            # 그라데이션 배너 (Clubmate Blue)
            st.markdown(f"""
            <div class="banner-gradient">
                <h2 style='color:white; margin:0;'>📢 AI 성향/역량 데이터 분석 완료!</h2>
                <p style='margin:5px 0 0 0;'>{recomm_text}을 결합하여 <b>{target_job} 직무 적합도 95%</b>로 확인되었습니다.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("Today's Pick")
                
                st.markdown(f"""
                <div class="feed-card">
                    <span class="tag">인턴십</span> <span class="tag" style="background-color:#E8F5E9; color:#2E7D32;">채용연계</span>
                    <h4 style="margin: 10px 0;">[LG CNS] {target_job} 신입/인턴 채용</h4>
                    <p style="color:#546E7A; font-size:14px; margin:0;">
                    🧬 <b>{test_key}</b> 인재를 선호하는 공고입니다! (성향 매칭됨)</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="feed-card">
                    <span class="tag">꿀팁</span>
                    <h4 style="margin: 10px 0;">현직자가 말하는 "이런 자소서는 바로 탈락합니다"</h4>
                    <p style="color:#546E7A; font-size:14px; margin:0;">조회수 2.1k | 좋아요 520</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="feed-card">
                    <span class="tag">멘토링</span>
                    <h4 style="margin: 10px 0;">{target_job} 3년차 현직자 무료 커피챗 (선착순 5명)</h4>
                    <p style="color:#546E7A; font-size:14px; margin:0;">신청 마감 임박</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.subheader("실시간 랭킹")
                st.markdown("""
                <div class="metric-box">
                    <p>🥇 <b>삼성전자</b> <span style="color:#D32F2F; float:right;">▲ 2</span></p>
                    <p>🥈 <b>SK하이닉스</b> <span style="color:#78909C; float:right;">-</span></p>
                    <p>🥉 <b>네이버</b> <span style="color:#1976D2; float:right;">▼ 1</span></p>
                    <p>4. <b>현대자동차</b></p>
                    <p>5. <b>LG에너지솔루션</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                st.subheader("📅 주요 일정")
                st.markdown("""
                <div class="metric-box">
                    <p>✅ <b>2/14</b> 상반기 공채 설명회</p>
                    <p>⚠️ <b>2/20</b> 토익 시험 접수 마감</p>
                    <p>📅 <b>2/28</b> 삼성전자 서류 오픈(예상)</p>
                </div>
                """, unsafe_allow_html=True)

        # [2] 로드맵/전략
        elif menu == "🗺️ 나의 로드맵/전략":
            
            # --- [Option 1] Korean Junior ---
            if track == 'Junior':
                st.title(f"🗺️ {target_job} 커리어 로드맵")
                st.caption("선배들의 데이터를 기반으로 생성된 최적의 성장 경로입니다.")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    graph = graphviz.Digraph()
                    graph.attr(rankdir='TB') 
                    graph.attr('node', shape='box', style='rounded,filled', fillcolor='#E3F2FD', color='#1565C0', fontname="sans-serif")
                    
                    graph.node('Start', '🏁 입학 (1학년)', fillcolor='#FFF9C4')
                    graph.node('GPA', '📚 학점 관리 (3.8+)', fillcolor='#C8E6C9')
                    graph.node('Eng', '🗣️ 어학 기초 (토익)', fillcolor='#E3F2FD')
                    graph.node('Club', '🤝 교내 학회/동아리', fillcolor='#E3F2FD')
                    graph.node('Cert', '💳 직무 자격증', fillcolor='#FFCCBC')
                    graph.node('Intern', '💼 인턴십 (3학년)', fillcolor='#FFAB91')
                    graph.node('Job', f'🏆 {target_job} 취업', fillcolor='#FFD54F', shape='doubleoctagon')

                    if "분석가" in test_key:
                        graph.node('Cert', '💳 데이터 자격증 (필수)', fillcolor='#FF8A65', penwidth='3') 
                    elif "소통가" in test_key:
                        graph.node('Club', '🤝 연합 동아리 (강추)', fillcolor='#FF8A65', penwidth='3')

                    graph.edge('Start', 'GPA')
                    graph.edge('Start', 'Eng')
                    graph.edge('GPA', 'Club')
                    graph.edge('Eng', 'Club')
                    graph.edge('Club', 'Cert')
                    graph.edge('Cert', 'Intern')
                    graph.edge('Intern', 'Job')
                    
                    st.graphviz_chart(graph)
                
                with col2:
                    st.markdown("""
                    <div class="feed-card">
                        <h4>📊 선배들의 경로 분석</h4>
                        <p style="font-size:14px;"><b>{0}</b> 합격자의 <b>65%</b>는<br>
                        2학년 때 <b>데이터 분석 학회</b>를 경험했습니다.</p>
                    </div>
                    """.format(target_job), unsafe_allow_html=True)
                    st.write("🚀 **추천 활동**")
                    st.checkbox("SQLD 자격증 따기")

            # --- [Option 2] Korean Senior ---
            else: 
                st.title("📊 합격 전략 리포트")
                st.info(f"{target_job} 직무 합격자 데이터와 내 스펙을 비교 분석합니다.")
                
                st.subheader("1. 나의 합격 경쟁력")
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    st.metric(label="예상 합격 확률", value="72%", delta="안정권 진입 중")
                with col_b:
                    st.progress(72)
                    st.caption("합격 안정권(85%)까지 13% 남았습니다.")

                st.divider()
                st.subheader("2. 합격자 vs 나 (Gap 분석)")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### ✅ 내가 가진 강점")
                    st.success("• **인턴 경험 (6개월)**: 경쟁자 평균(3개월)보다 높음")
                with col2:
                    st.markdown("##### 🚨 보완이 필요한 점")
                    st.error("• **비즈니스 영어**: OPIc IH 이상이 필요함 (현재 IM2)")

                st.divider()
                st.subheader("3. Next Step Recommendation")
                st.markdown(f"""
                <div style="background-color:#E8F5E9; padding:15px; border-radius:10px; color:#2E7D32;">
                    <h4>🚀 {target_job} 합격을 위한 최단 경로</h4>
                    <ul>
                        <li><b>[1개월 내]</b> 오픽 IH 취득하기</li>
                        <li><b>[2개월 내]</b> 포트폴리오에 '데이터 기반 성과' 챕터 추가</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        # [3] 업무 다이어리 (Sunny Yellow 포인트)
        elif menu == "📝 업무 다이어리":
            st.title("📝 인턴 업무 다이어리 (Career Log)")
            st.caption("매일 3분, 질문에 답하며 나만의 업무 자산을 쌓아보세요.")
            
            st.markdown(f"""
            <div style="background-color:#FFFDE7; padding:20px; border-radius:16px; margin-bottom:20px; text-align:center; border:1px solid #FFF59D;">
                <h3 style="color:#FBC02D; margin:0;">🔥 {st.session_state.diary_streak}일째 기록 중!</h3>
            </div>
            """, unsafe_allow_html=True)
            
            today_questions = ["오늘 사수님이나 동료에게 들은 피드백이 있나요?", "오늘 업무 중 가장 뿌듯했던 순간은 언제인가요?"]
            if 'today_q' not in st.session_state:
                st.session_state.today_q = random.choice(today_questions)
                
            col1, col2 = st.columns([1.5, 1])
            with col1:
                st.markdown(f"""<div class="question-box">Q. {st.session_state.today_q}</div>""", unsafe_allow_html=True)
                diary_input = st.text_area("답변을 입력하세요", height=100)
                
                if st.button("오늘의 기록 저장하기 ✨"):
                    if diary_input:
                        new_log = {"date": datetime.date.today().strftime("%Y-%m-%d"), "q": st.session_state.today_q, "a": diary_input}
                        st.session_state.diary_logs.insert(0, new_log)
                        st.session_state.diary_streak += 1
                        st.success("저장되었습니다!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("내용을 입력해주세요.")
                        
            with col2:
                st.markdown("### 📅 지난 기록")
                for log in st.session_state.diary_logs:
                    st.markdown(f"""
                    <div class="diary-card">
                        <span style="font-size:12px; color:#9E9E9E;">{log['date']}</span><br>
                        <b>Q. {log['q']}</b><br>
                        <span style="color:#5D4037;">{log['a']}</span>
                    </div>
                    """, unsafe_allow_html=True)

        # [4] AI 자소서 생성
        elif menu == "✍️ AI 자소서 작성":
            st.title("✍️ AI 자기소개서 생성")
            st.caption("지금까지 쌓아온 '다이어리(경험)', '역량검사(성향)', '스펙'을 모두 결합해 최적의 초안을 작성합니다.")
            
            st.markdown("##### 📡 사용되는 내 데이터 자산 (Assets)")
            st.markdown(f"""
            <div class="generator-box">
                <span class="source-badge">✅ 다이어리 기록 {len(st.session_state.diary_logs)}건</span>
                <span class="source-badge">✅ 성향 키워드: {test_key}</span>
                <span class="source-badge">✅ 목표 직무: {target_job}</span>
                <span class="source-badge">✅ 업로드 서류: 이력서_v1.pdf</span>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                apply_company = st.text_input("지원 기업명", placeholder="예: 삼성전자, 카카오")
            with col2:
                question_type = st.selectbox("질문 유형", ["지원동기", "성격의 장단점", "직무상 강점 (문제해결)", "입사 후 포부"])
                
            if st.button("✨ AI 초안 생성하기"):
                if apply_company:
                    with st.status("AI가 데이터를 분석하고 있습니다...", expanded=True) as status:
                        st.write("📂 업무 다이어리에서 관련 에피소드 추출 중...")
                        time.sleep(1)
                        st.write(f"🧬 '{test_key}' 성향 키워드와 매칭 중...")
                        time.sleep(1)
                        status.update(label="생성 완료!", state="complete", expanded=False)
                    
                    generated_content = f"""
[소제목: {test_key}의 치밀함으로 {target_job} 업무의 효율을 높이겠습니다]

저는 {apply_company}의 {target_job} 직무에서 저의 강점인 '{test_key}' 기질을 발휘하고자 지원했습니다. 평소 업무 다이어리를 통해 매일의 성과를 기록하며 부족한 점을 보완해왔습니다.

특히, 인턴 기간 동안 "{st.session_state.diary_logs[0]['a']}"와 같은 경험을 통해 실무 역량을 길렀습니다.

이러한 저의 '{test_key}' 성향과 꾸준한 기록 습관은 {apply_company}에서 데이터를 분석하고 업무 프로세스를 최적화하는 데 크게 기여할 것입니다.
                    """
                    st.subheader("📄 생성된 초안")
                    st.text_area("복사해서 수정해 보세요!", value=generated_content, height=300)
                else:
                    st.warning("지원하실 기업명을 입력해주세요.")

        elif menu == "📂 내 서류함":
            st.title("📂 내 서류함")
            st.write("업로드된 파일 목록:")
            st.markdown("- 📄 `AI_역량검사_결과표.pdf`")
            st.markdown("- 📄 `이력서_v1.pdf`")
            st.button("파일 추가하기")

        elif menu == "⚙️ 설정":
            st.title("설정")
            st.write(f"ID: {st.session_state.user_info.get('id', '-')}")
            if st.button("로그아웃"):
                st.session_state.step = 1
                st.rerun()
