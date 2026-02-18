import streamlit as st
import pandas as pd
import time
import datetime
import random
import graphviz

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="Career Map v8.1 (Landing Page)", page_icon="🧭", layout="wide")

# 세션 상태 관리 (랜딩 페이지 추가로 step 0부터 시작)
if 'step' not in st.session_state:
    st.session_state.step = 0  # 0부터 시작!
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
        {"date": "2026-02-01", "q": "Today's achievement?", "a": "Managed to finish the sales report in Korean without errors!"},
        {"date": "2026-02-02", "q": "What was difficult today?", "a": "Business email etiquette is still tricky..."}
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
# [STEP 0] 랜딩 페이지 (Landing Page) - [DESIGN UPGRADED & ALIGNED]
# ==========================================
if st.session_state.step == 0:
    
    # 1. CSS Styles (Clubmate Style + New Hero)
    st.markdown("""
    <style>
    /* 헤더 스타일 */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 20px;
        margin-bottom: 20px;
        border-bottom: 1px solid #F0F2F5;
    }
    .logo-text {
        font-size: 24px;
        font-weight: 900;
        color: #4A90E2; /* Brand Blue */
        font-family: 'Pretendard', sans-serif;
        text-decoration: none;
    }
    /* 네비게이션 링크 컨테이너 정렬 */
    .nav-links-container {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        height: 42px; /* 버튼 높이와 맞춰서 정렬 */
    }
    .nav-link {
        font-size: 15px;
        color: #546E7A;
        margin-left: 25px;
        text-decoration: none;
        font-weight: 500;
        cursor: pointer;
        transition: color 0.2s;
    }
    .nav-link:hover {
        color: #4A90E2;
    }

    /* 히어로 섹션 스타일 (2단 레이아웃) */
    .hero-wrapper {
        padding: 60px 20px;
        background: radial-gradient(50% 50% at 50% 50%, #F5F9FF 0%, #F7F9FC 100%);
        border-radius: 30px;
        margin-bottom: 50px;
    }
    .hero-content-left {
        text-align: left;
        padding-right: 20px;
    }
    .hero-main {
        font-size: 46px;
        font-weight: 800;
        color: #1A2B3C;
        line-height: 1.3;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }
    .hero-highlight {
        color: #4A90E2;
        background: linear-gradient(120deg, rgba(74, 144, 226, 0.1) 0%, rgba(74, 144, 226, 0.3) 100%);
        padding: 0 5px;
        border-radius: 8px;
    }
    .hero-desc {
        font-size: 18px;
        color: #546E7A;
        margin-bottom: 35px;
        line-height: 1.6;
        font-weight: 400;
    }
    .hero-image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    .hero-image {
        max-width: 100%;
        height: auto;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(74, 144, 226, 0.15);
        object-fit: cover;
    }
    
    /* 카드 디자인 */
    .feature-box {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        text-align: center;
        border: 1px solid #F0F2F5;
        height: 100%;
        transition: transform 0.3s ease;
    }
    .feature-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 10px 30px rgba(74, 144, 226, 0.15);
        border-color: #E3F2FD;
    }
    .emoji-icon {
        font-size: 45px;
        margin-bottom: 15px;
        background-color: #F5F9FF;
        width: 80px;
        height: 80px;
        line-height: 80px;
        border-radius: 50%;
        margin: 0 auto 20px auto;
    }
    
    /* 통계 섹션 */
    .stat-box {
        text-align: center;
    }
    .stat-num {
        font-size: 36px;
        font-weight: 800;
        color: #1A2B3C;
    }
    .stat-label {
        font-size: 14px;
        color: #78909C;
        font-weight: 600;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 2. Header (Navigation Bar) - [정렬 수정됨]
    col_h1, col_h2, col_h3 = st.columns([2, 4, 1])
    with col_h1:
        st.markdown('<div class="logo-text">🧭 Career Map</div>', unsafe_allow_html=True)
    with col_h2:
        # Flexbox 컨테이너로 감싸서 수직 중앙 정렬 및 우측 정렬
        st.markdown("""
        <div class="nav-links-container">
            <span class="nav-link">Visa Calculator</span>
            <span class="nav-link">Success Stories</span>
            <span class="nav-link">Pricing</span>
        </div>
        """, unsafe_allow_html=True)
    with col_h3:
        # 버튼 위쪽 여백(margin-top)을 조금 주어 텍스트와 시각적 높이를 맞춤
        st.markdown("""
        <style>
        div.stButton > button {
            margin-top: 5px; /* 미세 조정 */
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("Log in", key="top_login_btn"):
             st.session_state.step = 1
             st.rerun()

    st.write("")
    st.write("")

    # 3. Hero Section (Main Hook) - [2단 레이아웃 적용 및 디자인 개선]
    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    col_hero_left, col_hero_right = st.columns([1.1, 0.9]) # 좌측 텍스트 영역을 조금 더 넓게

    # [좌측] 텍스트 및 메인 CTA 버튼
    with col_hero_left:
        st.markdown("""
        <div class="hero-content-left">
            <div class="hero-main">
                Secure Your <span class="hero-highlight">E-7 Visa</span>,<br>
                Get Hired in Korea.
            </div>
            <div class="hero-desc">
                Stop worrying about visa points & specs.<br>
                We analyze <b>1,240 alumni data</b> to guide your winning path.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # CTA Button (왼쪽 정렬 스타일 적용)
        st.markdown("""
        <style>
        div.stButton > button:first-child {
            height: 56px;
            font-size: 18px;
            font-weight: 700;
            border-radius: 28px;
            background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%) !important;
            box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3);
            border: none;
            padding: 0 32px;
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(74, 144, 226, 0.4);
        }
        </style>
        """, unsafe_allow_html=True)
        # use_container_width=False로 설정하여 버튼 길이를 내용에 맞춤 (왼쪽 정렬 느낌)
        if st.button("🚀 Check My Visa Probability (Free)", use_container_width=False):
            st.session_state.step = 1
            st.rerun()
        
        st.markdown('<p style="font-size: 13px; color: #78909C; margin-top: 15px;">* No credit card required. Takes 2 mins.</p>', unsafe_allow_html=True)

    # [우측] Hero 이미지 (일러스트레이션)
    with col_hero_right:
        # 예시 이미지 URL입니다. 실제 서비스에 맞는 이미지로 교체해주세요.
        st.markdown("""
        <div class="hero-image-container">
            <img src="https://cdn.dribbble.com/users/1355613/screenshots/15631946/media/7f7874209018570b95fa45517452060c.jpg?compress=1&resize=800x600&vertical=top" class="hero-image" alt="Career Success Illustration">
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # hero-wrapper 종료

    st.write("")
    st.write("")
    st.write("")

    # 4. Features Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="emoji-icon">🧮</div>
            <h3 style="font-size:20px; font-weight:700; margin:0;">Smart Calculator</h3>
            <p style="font-size:14px; color:#546E7A; margin-top:10px; line-height:1.5;">
                Calculate your F-2-7 points in 1 minute.
                Simulate future scores with salary & KIIP.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="emoji-icon">🎓</div>
            <h3 style="font-size:20px; font-weight:700; margin:0;">Alumni Data</h3>
            <p style="font-size:14px; color:#546E7A; margin-top:10px; line-height:1.5;">
                "Where did Vietnamese majors go?"
                Unlock the winning path of seniors.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-box">
            <div class="emoji-icon">🗺️</div>
            <h3 style="font-size:20px; font-weight:700; margin:0;">Visa Roadmap</h3>
            <p style="font-size:14px; color:#546E7A; margin-top:10px; line-height:1.5;">
                From D-2 to E-7.
                Manage your timeline and D-day so you never miss a deadline.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.divider()
    st.write("")

    # 5. Social Proof Section
    st.markdown("<div style='text-align:center; margin-bottom:30px; font-size:14px; color:#4A90E2; font-weight:700; letter-spacing:1px;'>PROVEN BY DATA</div>", unsafe_allow_html=True)
    
    c_s1, c_s2, c_s3 = st.columns(3)
    with c_s1:
        st.markdown("<div class='stat-box'><div class='stat-num'>1,240+</div><div class='stat-label'>Successful Alumni</div></div>", unsafe_allow_html=True)
    with c_s2:
        st.markdown("<div class='stat-box'><div class='stat-num'>85%</div><div class='stat-label'>E-7 Approval Rate</div></div>", unsafe_allow_html=True)
    with c_s3:
        st.markdown("<div class='stat-box'><div class='stat-num'>TOP 3</div><div class='stat-label'>Samsung, LG, Kakao</div></div>", unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("")
    
    # 6. Bottom CTA
    st.markdown("""
    <div style="background-color:#F5F9FF; padding:40px; border-radius:20px; text-align:center; border:1px solid #E3F2FD;">
        <h2 style="margin:0 0 10px 0; color:#1A2B3C;">Ready to start your career in Korea?</h2>
        <p style="color:#546E7A; margin-bottom:20px;">Join 4,000+ international students managing their visa & career.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 하단 버튼도 중앙 정렬 (스타일 재사용을 위해 cols 사용 안함)
    c_b1, c_b2, c_b3 = st.columns([1, 1.5, 1])
    with c_b2:
        # 상단 버튼 스타일 재사용 (st.markdown 스타일은 전역 적용됨)
        if st.button("Start Now ✨", key="bottom_cta", use_container_width=True):
            st.session_state.step = 1
            st.rerun()

# ==========================================
# STEP 1: 로그인 및 회원가입
# ==========================================
elif st.session_state.step == 1:
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
                        # [수정됨] 로그인 성공 시 'Global Track'으로 자동 설정
                        st.session_state.user_info = {
                            'id': login_id,
                            'name': login_id, # 영문 느낌을 위해 '님' 제거
                            'track': 'Global', # <--- 여기를 Global로 변경했습니다!
                            'univ': 'Yonsei Univ.',
                            'major': 'Business',
                            'target_job': 'Global Strategy',
                            'test_keyword': 'Strategic',
                            'visa_type': 'D-2',
                            'topik': 'Level 4'
                        }
                        st.session_state.step = 4 # 대시보드로 직행
                        st.rerun()
                    else:
                        st.warning("아이디를 입력해주세요.")

        # [Tab 2] 회원가입 (유지)
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
            
            # Global 전용 메뉴 [NEW: Career Guide Added]
            menu = st.radio("MENU", [
                "🏠 Dashboard", 
                "🎓 Alumni Career Guide",
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
    # [Branch 1] Global Track Features
    # ----------------------------------------------------------------
    if track == 'Global':
        
        # 1. Dashboard (Main)
        if menu == "🏠 Dashboard":
            st.title(f"Hello, {user_name}! 👋")
            st.caption("Your personalized Visa & Career Dashboard")
            
            # [SECTION A] Status Summary
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
            
            # [SECTION B] Weekly Quests
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

            # [SECTION C] Recommended Jobs
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

        # [NEW] Alumni Career Guide (Deep-Dive & Interactive Version)
        elif menu == "🎓 Alumni Career Guide":
            st.title("🎓 Alumni Career Guide")
            st.caption(f"Analyze data from **1,240 successful international alumni** to build your winning strategy.")
            
            # 1. Smart Filter
            with st.container(border=True):
                st.markdown("#### 🔎 Filter Alumni Data")
                c_fil1, c_fil2, c_fil3 = st.columns(3)
                with c_fil1:
                    filter_nation = st.multiselect("Nationality", ["Vietnam", "China", "USA", "France", "Japan"], default=["Vietnam"])
                with c_fil2:
                    filter_major = st.multiselect("Major", ["Business", "Economics", "Computer Sci", "Mechanical Eng"], default=["Business"])
                with c_fil3:
                    filter_company = st.multiselect("Target Company", ["Samsung", "LG", "Kakao", "Hyundai", "Startups"])
                
                st.markdown(f"""
                <div style="background-color:#E3F2FD; padding:10px; border-radius:8px; font-size:14px; color:#1565C0; margin-top:10px;">
                    📊 Found <b>142</b> successful alumni matching your profile (<b>{', '.join(filter_nation)}</b> / <b>{', '.join(filter_major)}</b>).
                </div>
                """, unsafe_allow_html=True)

            st.write("")

            tab_insight, tab_persona, tab_mentoring = st.tabs(["📊 Data Insights", "👤 Success Stories (Role Model)", "☕ Request Coffee Chat"])

            # [TAB 1] 데이터 인사이트 (Deep-Dive)
            with tab_insight:
                # 1. Detailed Spec Analysis
                st.markdown("### 📊 Deep Dive: Specs of Successful Alumni")
                col_i1, col_i2, col_i3 = st.columns(3)
                with col_i1:
                    st.metric("Avg. TOPIK", "Level 5.8", "Higher than applicants (Lv 4.5)")
                with col_i2:
                    st.metric("Avg. GPA", "3.7 / 4.5", "Top 30%")
                with col_i3:
                    st.metric("Avg. Internships", "1.6", "Usually 1 startup + 1 major corp")

                st.write("")
                
                # 2. Company & Job Function Distribution
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.markdown("#### 🏢 Top Employers")
                    # Horizontal bar chart for readability
                    df_comp = pd.DataFrame([['Samsung Electronics', 45], ['LG CNS', 32], ['Kakao', 25], ['Hyundai Motor', 20], ['AmorePacific', 15]], columns=['Company', 'Hires'])
                    st.bar_chart(df_comp.set_index('Company'), color="#4A90E2", horizontal=True)
                with c2:
                    st.markdown("#### 🛠️ Top Job Functions")
                    # Simple breakdown
                    df_job = pd.DataFrame([['Overseas Sales', 40], ['Marketing (Content)', 25], ['Data Analyst', 20], ['PM/Strategy', 15]], columns=['Role', 'Percentage'])
                    st.bar_chart(df_job.set_index('Role'), color="#FFD54F")

                st.divider()
                
                # 3. Enhanced Winning Path (Graphviz)
                st.markdown("### 🛣️ The 'Winning Path' Strategy Map")
                st.caption("A dual-track strategy combining **Visa eligibility** and **Career competency**.")
                
                winning_path = graphviz.Digraph()
                winning_path.attr(rankdir='LR') # Left to Right
                # Global settings
                winning_path.attr('node', shape='box', style='rounded,filled', fontname="sans-serif", fontsize="12")
                
                # Track 1: Visa (Blue)
                winning_path.node('V1', 'KIIP Level 3\n(Year 2)', fillcolor='#E3F2FD', color='#1565C0')
                winning_path.node('V2', 'KIIP Level 4\n(Year 3)', fillcolor='#E3F2FD', color='#1565C0')
                winning_path.node('V3', 'KIIP Completion\n(Year 4)', fillcolor='#BBDEFB', color='#0D47A1', penwidth='2')
                
                # Track 2: Career (Yellow/Orange)
                winning_path.node('C1', 'Biz Korean Class\n(Year 2)', fillcolor='#FFF9C4', color='#FBC02D')
                winning_path.node('C2', 'Startup Intern\n(Year 3 Summer)', fillcolor='#FFF9C4', color='#FBC02D')
                winning_path.node('C3', 'Major Corp Intern\n(Year 4 Winter)', fillcolor='#FFE082', color='#F57F17', penwidth='2')
                
                # Goal
                winning_path.node('Goal', '🏆 Job & E-7 Visa\n(Graduation)', fillcolor='#C8E6C9', color='#2E7D32', shape='doubleoctagon', fontsize="14")

                # Edges
                winning_path.edge('V1', 'V2')
                winning_path.edge('V2', 'V3')
                winning_path.edge('C1', 'C2')
                winning_path.edge('C2', 'C3')
                
                # Cross connections (Synergy)
                winning_path.edge('C2', 'V3', style='dashed', label='Points+', fontsize="10")
                winning_path.edge('V3', 'Goal')
                winning_path.edge('C3', 'Goal')
                
                st.graphviz_chart(winning_path)
                
                st.info("💡 **Strategic Insight:** Completing **KIIP** in Year 3 is crucial. It gives you +10 Visa points, which compensates for lack of full-time experience.")

            # [TAB 2] 성공 사례
            with tab_persona:
                st.subheader("👤 Find your Role Model")
                st.caption("Detailed profiles of anonymous seniors. Clone their strategy!")
                
                with st.expander("🥇 Case 1: Samsung Electronics / Overseas Sales (Vietnam)", expanded=True):
                    c_p1, c_p2 = st.columns([1, 2])
                    with c_p1:
                        st.markdown("**Profile**")
                        st.markdown("- **Nationality:** Vietnam")
                        st.markdown("- **Major:** Business (GPA 3.9)")
                        st.markdown("- **Visa:** D-2 -> E-7")
                    with c_p2:
                        st.markdown("**Core Competencies**")
                        st.info("✅ **TOPIK 6** (Fluent)")
                        st.info("✅ **Internship:** 6 months at Trading Company")
                        st.info("✅ **Extra:** President of Vietnamese Student Association")
                    
                    st.markdown("**💡 Senior's Tip:**")
                    st.write(" > \"For sales roles, speaking is more important than writing. I practiced interview answers 100 times.\"")
                    if st.button("📌 Benchmark this Senior (Save to Roadmap)"):
                        st.toast("Added to your roadmap!", icon="✅")

                with st.expander("🥈 Case 2: Moloco / Data Analyst", expanded=False):
                    c_p3, c_p4 = st.columns([1, 2])
                    with c_p3:
                        st.markdown("**Profile**")
                        st.markdown("- **Nationality:** USA")
                        st.markdown("- **Major:** Applied Statistics")
                        st.markdown("- **Visa:** F-4")
                    with c_p4:
                        st.markdown("**Core Competencies**")
                        st.info("✅ **TOPIK 4** (Business Level)")
                        st.info("✅ **Projects:** 3 Kaggle Competitions")
                        st.info("✅ **Skill:** SQL, Python, Tableau")
                    
                    st.markdown("**💡 Senior's Tip:**")
                    st.write(" > \"Tech companies care less about Korean. Build a strong GitHub portfolio.\"")

            # [TAB 3] 멘토링 연결
            with tab_mentoring:
                st.subheader("☕ Connect with Alumni")
                st.write("Directly ask questions to seniors who are working at your dream company.")
                
                m1, m2 = st.columns(2)
                with m1:
                    st.markdown("""
                    <div class="feed-card">
                        <div style="display:flex; align-items:center; margin-bottom:10px;">
                            <div style="background-color:#E3F2FD; width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">👨‍💼</div>
                            <div>
                                <h4 style="margin:0;">Minh Nguyen</h4>
                                <span style="font-size:12px; color:#555;">Samsung Electronics (3y)</span>
                            </div>
                        </div>
                        <p style="font-size:13px; color:#666;">"I can help with resume reviews for sales roles."</p>
                        <button style="width:100%; background-color:#4A90E2; color:white; border:none; padding:5px; border-radius:5px;">Request Coffee Chat (30min)</button>
                    </div>
                    """, unsafe_allow_html=True)
                with m2:
                    st.markdown("""
                    <div class="feed-card">
                        <div style="display:flex; align-items:center; margin-bottom:10px;">
                            <div style="background-color:#FFF3E0; width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">👩‍💻</div>
                            <div>
                                <h4 style="margin:0;">Sarah Lee</h4>
                                <span style="font-size:12px; color:#555;">Coupang (2y)</span>
                            </div>
                        </div>
                        <p style="font-size:13px; color:#666;">"Ask me anything about F-series visa change."</p>
                        <button style="width:100%; background-color:#4A90E2; color:white; border:none; padding:5px; border-radius:5px;">Request Coffee Chat (30min)</button>
                    </div>
                    """, unsafe_allow_html=True)

        # 2. Visa Calculator (F-2-7 Smart Simulator) - [UPGRADED]
        elif menu == "🛂 Visa Calculator (F-2-7)":
            st.title("🧮 F-2-7 Smart Simulator")
            st.caption("Calculate your points accurately and simulate your future strategy.")
            
            # 탭 분리: 현재 점수 진단 vs 미래 시뮬레이션
            tab_cal, tab_sim = st.tabs(["📊 Current Score", "🔮 Future Simulator"])
            
            # --- [TAB 1] 현재 점수 정밀 진단 ---
            with tab_cal:
                st.info("💡 **Did you know?** You need **80 points** out of 135 to apply for the F-2-7 visa.")
                
                with st.form("visa_form"):
                    col_base1, col_base2 = st.columns(2)
                    
                    with col_base1:
                        st.markdown("##### 1. Age (Max 25)")
                        age_input = st.slider("Select your Age", 18, 60, 24)
                        # 나이 점수 로직 (실제 F-2-7 기준 근사치)
                        if 18 <= age_input <= 24: age_pts = 23
                        elif 25 <= age_input <= 29: age_pts = 25
                        elif 30 <= age_input <= 34: age_pts = 23
                        elif 35 <= age_input <= 39: age_pts = 20
                        else: age_pts = 10
                        st.caption(f"Score: +{age_pts}")

                        st.markdown("##### 2. Education (Max 35)")
                        edu_type = st.selectbox("Degree Type", 
                            ["High School", "Associate (2yr)", "Bachelor (4yr)", "Master", "Ph.D"])
                        is_korean_degree = st.checkbox("Is this a Korean Degree?")
                        is_stem = st.checkbox("Is this a STEM Major?")
                        
                        # 학력 점수 로직
                        edu_pts = 0
                        if edu_type == "Associate (2yr)": edu_pts = 10
                        elif edu_type == "Bachelor (4yr)": edu_pts = 15
                        elif edu_type == "Master": edu_pts = 20
                        elif edu_type == "Ph.D": edu_pts = 25
                        
                        # 가산점 (STEM 등)은 별도 항목이 아닌 학력 안에서 계산되는 경우가 많으나 여기선 Bonus로 뺌
                        
                        st.caption(f"Base Score: +{edu_pts}")

                    with col_base2:
                        st.markdown("##### 3. Korean Ability (Max 20)")
                        korean_type = st.radio("Test Type", ["TOPIK", "KIIP (Social Integration)"], horizontal=True)
                        korean_level = st.slider("Level (1-5+)", 1, 6, 4)
                        
                        # 한국어 점수 로직
                        kor_pts = 0
                        if korean_level == 1: kor_pts = 3
                        elif korean_level == 2: kor_pts = 5
                        elif korean_level == 3: kor_pts = 10
                        elif korean_level == 4: kor_pts = 15
                        elif korean_level >= 5: kor_pts = 20
                        st.caption(f"Score: +{kor_pts}")

                        st.markdown("##### 4. Annual Income (Max 60)")
                        income_input = st.number_input("Yearly Income (Unit: 10,000 KRW)", min_value=0, value=0, step=100)
                        st.caption("e.g. 3000 = 30 Million KRW")
                        
                        # 소득 점수 로직 (대략적 GNI 배수 기준)
                        inc_pts = 0
                        if income_input >= 10000: inc_pts = 60 # 1억 이상
                        elif income_input >= 8000: inc_pts = 50
                        elif income_input >= 6000: inc_pts = 45
                        elif income_input >= 5000: inc_pts = 40
                        elif income_input >= 4000: inc_pts = 30
                        elif income_input >= 3000: inc_pts = 20 # GNI 0.7~
                        else: inc_pts = 0
                        st.caption(f"Score: +{inc_pts}")

                    st.divider()
                    
                    st.markdown("##### 5. Bonus & Penalty")
                    c_b1, c_b2 = st.columns(2)
                    with c_b1:
                        st.markdown("**Bonus (+)**")
                        bonus_kiip = st.checkbox("KIIP Completion (+10)")
                        bonus_kor_degree = False
                        if is_korean_degree: # 위에서 체크한 것 연동
                             st.success("✅ Korean Degree Bonus (+10) Applied")
                             bonus_kor_degree = True
                        bonus_volunteer = st.checkbox("Social Volunteer (>1yr) (+3)")
                        
                        total_bonus = 0
                        if bonus_kiip: total_bonus += 10
                        if bonus_kor_degree: total_bonus += 10
                        if bonus_volunteer: total_bonus += 3
                        
                    with c_b2:
                        st.markdown("**Penalty (-)**")
                        penalty_violation = st.checkbox("Immigration Law Violation (-)")
                        penalty_count = 0
                        if penalty_violation:
                            penalty_count = st.number_input("How many times?", 1, 3, 1)
                        
                        total_penalty = penalty_count * 10 # 1회당 10점 감점 가정
                    
                    st.write("")
                    submit_cal = st.form_submit_button("🏁 Calculate My Score")
                
                if submit_cal:
                    final_score = age_pts + edu_pts + kor_pts + inc_pts + total_bonus - total_penalty
                    
                    # 결과 시각화
                    col_res1, col_res2 = st.columns([1, 2])
                    with col_res1:
                        st.metric("Total Score", f"{final_score} / 135", delta=f"{final_score - 80} gap")
                    with col_res2:
                        bar_color = "#4CAF50" if final_score >= 80 else "#FF5252"
                        st.markdown(f"""
                        <div style="margin-top:10px;">
                            <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:bold; margin-bottom:5px;">
                                <span>0</span><span>Pass (80)</span><span>135</span>
                            </div>
                            <div style="background-color:#EEE; border-radius:10px; height:25px; width:100%; position:relative;">
                                <div style="background-color:{bar_color}; width:{min(final_score, 135)/135*100}%; height:100%; border-radius:10px;"></div>
                                <div style="position:absolute; top:0; left:{80/135*100}%; width:2px; height:100%; background-color:black; opacity:0.5;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if final_score >= 80:
                        st.balloons()
                        st.success("🎉 **Safe Zone!** You satisfy the F-2-7 requirements.")
                    else:
                        st.error(f"🚨 **Danger Zone.** You need {80 - final_score} more points.")
                        st.markdown("""
                        <div style="background-color:#FFEBEE; padding:15px; border-radius:10px; border:1px solid #FFCDD2;">
                            <b>💡 Immediate Actions to take:</b>
                            <ul style="margin-bottom:0;">
                                <li>If you finish <b>KIIP Level 5</b>, you get <b>+10 pts</b>.</li>
                                <li>If you increase income to <b>30M KRW</b>, you get <b>+20 pts</b>.</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

            # --- [TAB 2] 미래 시뮬레이터 (What-if Analysis) ---
            with tab_sim:
                st.markdown("### 🔮 What if...?")
                st.caption("Simulate your future score by changing your conditions.")
                
                # 시뮬레이션용 세션 상태 (간소화)
                if 'sim_kiip' not in st.session_state: st.session_state.sim_kiip = False
                if 'sim_income' not in st.session_state: st.session_state.sim_income = 0
                
                c_s1, c_s2 = st.columns([1, 1])
                with c_s1:
                    st.markdown("**Current State**")
                    # (위 탭 1에서 계산된 값을 가져왔다고 가정, 여기선 예시값 65)
                    st.metric("Current Score", "65 pts", "D-2 Visa")
                    
                with c_s2:
                    st.markdown("**Future Goal**")
                    target_kiip = st.toggle("✅ Complete KIIP Level 5 (+10 pts)")
                    target_master = st.toggle("🎓 Get Master's Degree (+5 pts)")
                    target_income = st.select_slider("💰 Future Salary", options=["None", "30M", "40M", "50M"])
                    
                    sim_score = 65
                    delta = 0
                    
                    if target_kiip: 
                        sim_score += 10
                        delta += 10
                    if target_master: 
                        sim_score += 5
                        delta += 5
                    
                    inc_gain = 0
                    if target_income == "30M": inc_gain = 20
                    elif target_income == "40M": inc_gain = 30
                    elif target_income == "50M": inc_gain = 40
                    
                    # 기존 소득 점수(0)를 뺀다고 가정하고 새로운 소득 점수 추가
                    sim_score += inc_gain
                    delta += inc_gain
                    
                    st.metric("Simulated Score", f"{sim_score} pts", f"+{delta} pts increase")
                
                st.divider()
                
                # 결과 멘트
                if sim_score >= 80:
                    st.success("🚀 **Strategy Success!** If you achieve these goals, you will pass.")
                    st.markdown("**Recommended Roadmap:**")
                    st.code("1. Enroll in KIIP (Month 1)\n2. Graduate with Master's (Year 2)\n3. Secure a job over 30M KRW (Year 2.5)")
                else:
                    st.warning("⚠️ Still not enough. You might need higher income or STEM major bonus.")

        # 3. Visa Roadmap (Timeline & Checklist) - [FIXED]
        elif menu == "🗺️ Visa Roadmap":
            st.title("🗺️ Smart Visa Roadmap")
            st.caption("A strategic timeline based on your expected graduation date.")
            
            # 1. Graduation Setup
            with st.expander("🎓 Set Graduation Date", expanded=True):
                col_date1, col_date2 = st.columns([2, 1])
                with col_date1:
                    grad_date = st.date_input("Expected Graduation Date", datetime.date(2027, 2, 28))
                with col_date2:
                    today = datetime.date.today()
                    d_day = (grad_date - today).days
                    st.metric("Time Remaining", f"D-{d_day}", "Keep pushing!")

            st.divider()

            # 2. Timeline Visualization
            current_stage = 1 
            
            stages = [
                {
                    "id": 0,
                    "title": "STEP 1: D-2 Maintenance (Student)",
                    "period": "Until Graduation",
                    "status": "Completed" if d_day < 365 else "Active",
                    "desc": "Focus on GPA and Part-time Job Report (S-3).",
                    "alert": "🚨 Working part-time without reporting to immigration is illegal. You will be denied E-7 later.",
                    "docs": ["Part-time Permit (HiKorea)", "Transcript (3.0+)"]
                },
                {
                    "id": 1,
                    "title": "STEP 2: D-10 Preparation",
                    "period": "D-90 to Graduation",
                    "status": "Active" if 0 < d_day <= 365 else "Upcoming",
                    "desc": "Prepare to switch to 'Job Seeker Visa' immediately after graduation.",
                    "alert": "⚠️ You must have 60+ points on the D-10 scorecard.",
                    "docs": ["Job Seeking Plan (Monthly)", "Bank Statement (4.5M KRW+)", "Diploma / Proof of Degree"]
                },
                {
                    "id": 2,
                    "title": "STEP 3: The Golden Time (Internship)",
                    "period": "Graduation + 6 Months",
                    "status": "Upcoming",
                    "desc": "Find a full-time offer within 6 months. Convert Internship to Probation.",
                    "alert": "💡 Your salary must be above 80% of GNI (approx. 34M KRW).",
                    "docs": ["Internship Contract", "Company Business License"]
                },
                {
                    "id": 3,
                    "title": "STEP 4: E-7 Application",
                    "period": "With Job Contract",
                    "status": "Upcoming",
                    "desc": "The final boss. Apply for the Professional Visa with your company.",
                    "alert": "🔥 The company must have a Korean:Foreigner ratio of 5:1.",
                    "docs": ["Employment Contract", "Company Recommendation Letter", "Tax Records (Company)"]
                }
            ]

            # Timeline Rendering (Fixed Indentation Issue)
            for stage in stages:
                border_color = "#4A90E2" if stage['status'] == "Active" else "#E0E0E0"
                bg_color = "#FDFEFF" if stage['status'] == "Active" else "#F9F9F9"
                opacity = "1.0" if stage['status'] in ["Active", "Completed"] else "0.7"
                
                # HTML 내부에 들여쓰기를 최소화하여 Code Block 인식을 방지함
                st.markdown(f"""
<div style="border-left: 5px solid {border_color}; background-color: {bg_color}; padding: 20px; border-radius: 5px; margin-bottom: 20px; opacity: {opacity}; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <h4 style="margin:0; color:#333;">{stage['title']}</h4>
        <span class="tag">{stage['period']}</span>
    </div>
    <p style="margin:10px 0; font-size:14px; color:#555;">{stage['desc']}</p>
    <div style="background-color:#FFEBEE; padding:10px; border-radius:5px; font-size:13px; color:#D32F2F; margin-bottom:10px;">
        {stage['alert']}
    </div>
</div>
""", unsafe_allow_html=True)
                
                with st.expander(f"📂 Open Document Checklist ({stage['title']})"):
                    st.write("**Required Documents:**")
                    for doc in stage['docs']:
                        st.checkbox(doc, key=f"doc_{stage['id']}_{doc}")
                    
                    if stage['status'] == "Active":
                        st.button(f"Start {stage['title'].split(':')[0]} Guide", key=f"btn_{stage['id']}")

            st.info("💡 **Tip:** E-7 screening takes 3-4 weeks. Do not travel outside Korea during the application.")

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
