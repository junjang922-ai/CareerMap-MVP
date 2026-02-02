import streamlit as st
import pandas as pd
import time
import datetime
import random
import graphviz

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="Career Map v7.1", page_icon="🧭", layout="wide")

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
                        st.session_state.user_info['name'] = login_id + "님"
                        st.session_state.step = 2
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
                        st.session_state.step = 2
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
# STEP 3: 상세 진단 (수정됨: 진단 여부 선택 + 외부 업로드 공존)
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
        
        test_keyword = st.session_state.user_info.get('test_keyword', '미입력')
        
        # 이미 진단을 완료한 경우
        if test_keyword != '미입력':
             st.success(f"✅ Career Map AI 진단 완료: **{test_keyword}**")
        
        # 진단을 아직 안 한 경우
        else:
            want_diagnosis = st.radio("진단 여부 선택", ["네, 받아볼래요. (추천)", "아니요, 괜찮습니다."], horizontal=True, label_visibility="collapsed")
            
            if want_diagnosis == "네, 받아볼래요. (추천)":
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
                if st.button("👉 AI 진단 시작하기 (새 페이지)"):
                    st.session_state.step = 3.5 # 진단 페이지로 이동
                    st.rerun()

        st.write("")
        st.divider()
        st.write("")

        # 1-2. 외부 결과 업로드 (항상 표시)
        st.markdown("#### Q. 외부 역량검사(마이다스, 잡다 등) 결과표가 있으신가요? (선택)")
        st.caption("결과표(PDF)를 업로드하면 해당 데이터를 기반으로 더 정교하게 분석합니다.")
        
        st.file_uploader("검사 결과표 업로드", type=['pdf', 'jpg', 'png'])
        st.selectbox("결과표의 핵심 성향 키워드를 선택해주세요", 
                         ["선택해주세요", "전략가형 (Strategic)", "분석가형 (Analytical)", "소통가형 (Social)", "개척자형 (Challenger)"])

        st.write("")
        st.divider()
        st.write("")

        # [New Feature] 이력서/자소서 분석 (유지)
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
        
        # 종합 분석 시작 버튼
        if st.button("🚀 AI 통합 분석 시작하기", type="primary"):
            # 데모용: 진단을 안 했다면 임의 설정
            if test_keyword == '미입력':
                st.session_state.user_info['test_keyword'] = "전략가형 (Strategic)"
            
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
    st.progress(30) 
    
    with st.container(border=True):
        st.markdown("#### Q1. 새로운 프로젝트를 시작할 때, 나는?")
        st.radio("1번 문항", ["철저하게 계획을 세우고 시작한다.", "일단 부딪혀보며 수정해 나간다."], label_visibility="collapsed")
    
    st.write("")
    
    with st.container(border=True):
        st.markdown("#### Q2. 팀원과 의견이 충돌할 때, 나는?")
        st.radio("2번 문항", ["논리적인 근거를 들어 설득한다.", "상대방의 감정을 먼저 살핀다."], label_visibility="collapsed")
    
    st.write("")
    
    with st.container(border=True):
        st.markdown("#### Q3. 내가 더 선호하는 업무 환경은?")
        st.radio("3번 문항", ["조용하고 독립적인 공간", "활발하게 소통하는 개방된 공간"], label_visibility="collapsed")
    
    st.write("")
    
    if st.button("진단 결과 제출하기"):
        with st.spinner("결과를 분석 중입니다..."):
            time.sleep(1.5)
            # 데모 결과 저장
            st.session_state.user_info['test_keyword'] = "분석가형 (Analytical)"
            st.session_state.step = 3 # 다시 데이터 연동 페이지로 복귀
            st.rerun()

# ==========================================
# STEP 4: 메인 대시보드 (유지)
# ==========================================
elif st.session_state.step == 4:
    
    user_name = st.session_state.user_info.get('name', 'User')
    target_job = st.session_state.user_info.get('target_job', '직무')
    test_key = st.session_state.user_info.get('test_keyword', '미입력')
    track = st.session_state.user_info.get('track', 'Type')
    
    # [사이드바]
    with st.sidebar:
        st.title("🧭 Career Map")
        st.write(f"**{user_name}**님")
        st.caption(f"{st.session_state.user_info.get('univ')} | {track}")
        
        # 뱃지 스타일 (Clubmate Blue)
        if track == 'Global':
            st.markdown(f"<span class='tag'>🛂 Visa: {st.session_state.user_info.get('visa_type', 'D-2')}</span>", unsafe_allow_html=True)
        else:
            if "분석가" in test_key or "전략가" in test_key:
                st.markdown(f"<span class='tag'>🧬 {test_key}</span>", unsafe_allow_html=True)
            elif "소통가" in test_key or "개척자" in test_key:
                st.markdown(f"<span class='tag'>🧬 {test_key}</span>", unsafe_allow_html=True)
            
        st.divider()
        menu = st.radio("MENU", ["🏠 홈 (Feed)", "🗺️ 나의 로드맵/전략", "📝 업무 다이어리", "✍️ AI 자소서 작성", "📂 내 서류함", "⚙️ 설정"])
        
        st.divider()
        st.info("💡 **Premium**\n현직자 1:1 멘토링 매칭")

    # [1] 홈 (Feed)
    if menu == "🏠 홈 (Feed)":
        st.header(f"🔥 {target_job} 분야 트렌드")
        
        # [Branch] Global Feed
        if track == 'Global':
             st.markdown(f"""
            <div class="banner-gradient">
                <h2 style='color:white; margin:0;'>🌏 Global Talent Analysis</h2>
                <p style='margin:5px 0 0 0;'>Visa Probability: <b>85%</b> (Safe)<br>
                Based on your TOPIK {st.session_state.user_info.get('topik', 'Level 4')} and Major.</p>
            </div>
            """, unsafe_allow_html=True)
             st.info("📢 **Visa Alert:** D-10 visa regulations have been updated. (Check Now)")
             
        # [Branch] Korean Feed
        else:
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
        
        # --- [Option 1] Global Track ---
        if track == 'Global':
            st.title("🌏 Visa & Career Roadmap")
            st.caption("Strategic roadmap for E-7 Visa acquisition.")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                graph = graphviz.Digraph()
                graph.attr(rankdir='LR')
                graph.attr('node', shape='box', style='rounded,filled', fillcolor='#E3F2FD', color='#1565C0', fontname="sans-serif")
                
                graph.node('D2', 'D-2 (Student)', fillcolor='#FFF9C4')
                graph.node('TOPIK', 'TOPIK Level 5', fillcolor='#FFCCBC')
                graph.node('Intern', 'Internship', fillcolor='#E3F2FD')
                graph.node('Grad', 'Graduation', fillcolor='#C8E6C9')
                graph.node('D10', 'D-10 (Job Seeker)', fillcolor='#E1BEE7')
                graph.node('E7', 'E-7 (Professional)', fillcolor='#FFD54F', shape='doubleoctagon')
                
                graph.edge('D2', 'TOPIK')
                graph.edge('TOPIK', 'Intern')
                graph.edge('Intern', 'Grad')
                graph.edge('Grad', 'D10')
                graph.edge('D10', 'E7')
                
                st.graphviz_chart(graph)
            
            with col2:
                st.info("💡 **Visa Analysis**")
                st.write("Your probability of getting **E-7 Visa** is **85%**.")
                st.write("- Strength: Major Match ✅")
                st.write("- Weakness: TOPIK Score (Need Level 5)")
                
        # --- [Option 2] Korean Junior ---
        elif track == 'Junior':
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

        # --- [Option 3] Korean Senior ---
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
