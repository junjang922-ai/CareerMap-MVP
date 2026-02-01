import streamlit as st
import pandas as pd
import time
import datetime

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="Career Map v5.2", page_icon="🧭", layout="wide")

# 세션 상태 관리
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1:입력 -> 2:트랙선택 -> 3:상세 -> 4:대시보드
if 'user_info' not in st.session_state:
    st.session_state.user_info = {} # 유저 정보를 담을 딕셔너리

# 스타일링 (서핏 느낌의 카드 UI - v5.0 디자인 복원)
st.markdown("""
    <style>
    .main {background-color: #F8F9FA;}
    h1, h2, h3 {color: #1A237E; font-family: 'Pretendard', sans-serif;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 8px; width: 100%; height: 45px; font-weight: bold;}
    
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
        cursor: pointer;
    }
    .tag {
        background-color: #E3F2FD;
        color: #1565C0;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        margin-right: 5px;
    }
    .metric-box {
        background-color: #fff;
        border: 1px solid #eee;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# STEP 1: 로그인 및 회원가입 (v5.1 유지 - 변경 없음)
# ==========================================
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; margin-top: 50px;'>🧭 Career Map</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>불확실한 미래를 데이터로 확신하다.</p>", unsafe_allow_html=True)
        st.write("")
        
        tab1, tab2 = st.tabs(["로그인", "회원가입 (필수)"])
        
        # [Tab 1] 로그인
        with tab1:
            with st.container(border=True):
                login_id = st.text_input("아이디", key="login_id")
                login_pw = st.text_input("비밀번호", type="password", key="login_pw")
                if st.button("로그인"):
                    if login_id:
                        st.session_state.user_info['name'] = login_id + "님"
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.warning("아이디를 입력해주세요.")

        # [Tab 2] 회원가입
        with tab2:
            st.info("👋 정확한 진단을 위해 기본 정보를 입력해주세요.")
            with st.form("signup_form"):
                st.markdown("##### 1️⃣ 계정 정보")
                new_id = st.text_input("아이디 (ID)")
                new_pw = st.text_input("비밀번호 (Password)", type="password")
                
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
# STEP 2: 트랙 선택 (v5.0의 상세 설명 복원)
# ==========================================
elif st.session_state.step == 2:
    user_name = st.session_state.user_info.get('name', '사용자')
    
    st.title(f"{user_name}님, 환영합니다! 👋")
    st.subheader("현재 상황에 맞는 트랙을 선택하세요.")
    st.markdown("선택하신 트랙에 따라 **전혀 다른 솔루션**이 제공됩니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🐣 저학년 (1~2학년)")
            st.write("아직 구체적인 진로를 정하지 못했어요.")
            st.info("🎯 **제공 서비스:**\n- 커리어 성향(DNA) 진단\n- 학년별 필수 로드맵\n- 교내외 대외활동 추천")
            if st.button("저학년 트랙 선택"):
                st.session_state.user_info['track'] = 'Junior'
                st.session_state.step = 3
                st.rerun()
                
    with col2:
        with st.container(border=True):
            st.markdown("### 🦅 고학년 (3~4학년/취준)")
            st.write("목표 직무가 있고, 합격이 목표예요.")
            st.info("🎯 **제공 서비스:**\n- 이력서/자소서 AI 분석\n- 합격 확률 시뮬레이션\n- 부족한 스펙(Gap) 진단")
            if st.button("고학년 트랙 선택"):
                st.session_state.user_info['track'] = 'Senior'
                st.session_state.step = 3
                st.rerun()

# ==========================================
# STEP 3: 상세 진단 & 파일 업로드 (v5.0 기능 복원)
# ==========================================
elif st.session_state.step == 3:
    track = st.session_state.user_info.get('track', 'Senior')
    st.title("🧩 맞춤형 설계를 위한 추가 정보")
    
    # 1. 학적 및 직무 (필수)
    col1, col2 = st.columns(2)
    with col1:
        univ = st.text_input("소속 대학", placeholder="예: 연세대학교")
    with col2:
        major = st.text_input("전공", placeholder="예: 경제학과")

    target_job = st.text_input("관심 직무/분야 (필수)", placeholder="예: 마케팅, 데이터 분석, 금융권 등")
    
    st.write("")
    st.markdown("### 🕵️ 정밀 진단 (선택 사항)")
    st.caption("입력하시면 분석 정확도가 **200%** 올라갑니다.")
    
    # 2. 성향/인성 검사 (v5.0 복원)
    with st.expander("🧠 간단 성향/인성 검사 진행하기"):
        st.write("나에게 맞는 업무 스타일을 찾아드립니다.")
        q1 = st.radio("1. 새로운 문제를 마주했을 때 나는?", ["논리적으로 분석하여 근거를 찾는다", "직관적으로 아이디어를 낸다", "주변 사람들과 논의하여 해결한다"])
        q2 = st.radio("2. 선호하는 조직 문화는?", ["체계적이고 역할이 분명한 곳", "자율적이고 성과 중심인 곳", "수평적이고 협력적인 곳"])
        st.checkbox("진단 결과 반영하기", value=True)

    # 3. 파일 업로드 (v5.0 복원)
    uploaded_file = st.file_uploader("📂 이력서/자소서/포트폴리오 업로드 (PDF, Word)", type=['pdf', 'docx'])
    
    st.write("")
    if st.button("🚀 나만의 커리어 대시보드 생성하기"):
        if target_job:
            # 정보 업데이트
            st.session_state.user_info.update({
                'univ': univ,
                'major': major,
                'target_job': target_job
            })
            
            # 로딩 연출 (Wizard of Oz - v5.0 복원)
            progress_text = "AI가 회원님의 성향과 스펙을 분석 중입니다..."
            my_bar = st.progress(0, text=progress_text)
            
            for percent_complete in range(100):
                time.sleep(0.02) # 로딩 시간
                if percent_complete == 30:
                    my_bar.progress(percent_complete + 1, text="텍스트 추출 중 (OCR)...")
                elif percent_complete == 60:
                    my_bar.progress(percent_complete + 1, text="핵심 역량 파싱 및 매칭 중...")
                elif percent_complete == 90:
                    my_bar.progress(percent_complete + 1, text="합격자 데이터와 비교 분석 중...")
                else:
                    my_bar.progress(percent_complete + 1)
            
            time.sleep(0.5)
            st.session_state.step = 4
            st.rerun()
        else:
            st.warning("관심 직무는 필수 입력 사항입니다.")

# ==========================================
# STEP 4: 메인 대시보드 (v5.0 서핏 스타일 복원)
# ==========================================
elif st.session_state.step == 4:
    
    user_name = st.session_state.user_info.get('name', 'User')
    target_job = st.session_state.user_info.get('target_job', '직무')
    univ = st.session_state.user_info.get('univ', '대학교')
    track = st.session_state.user_info.get('track', 'Type')
    
    # [사이드바]
    with st.sidebar:
        st.title("🧭 Career Map")
        st.write(f"**{user_name}**님")
        st.caption(f"{univ} | {track}")
        st.divider()
        menu = st.radio("MENU", ["🏠 홈 (Feed)", "🗺️ 나의 로드맵/전략", "📂 내 서류함", "⚙️ 설정"])
        
        st.divider()
        st.info("💡 **Premium 기능**\n현직자 1:1 멘토링 매칭")

    # [메인 화면 1] 홈 (뉴스피드) - 카드 UI 복원
    if menu == "🏠 홈 (Feed)":
        st.header(f"🔥 {target_job} 분야 트렌드")
        
        # 상단 배너
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #4A90E2 0%, #00E676 100%); padding: 25px; border-radius: 12px; color: white; margin-bottom: 25px;">
            <h2 style='color:white; margin:0;'>📢 {user_name}님을 위한 추천 공고</h2>
            <p style='margin:5px 0 0 0;'>회원님의 스펙과 <b>92% 일치</b>하는 인턴 공고가 떴어요! 확인해보세요.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Today's Pick")
            
            # 피드 1
            st.markdown(f"""
            <div class="feed-card">
                <span class="tag">인턴십</span> <span class="tag" style="background-color:#E8F5E9; color:#2E7D32;">채용연계</span>
                <h4 style="margin: 10px 0;">[카카오] {target_job} 직무 채용 연계형 인턴 모집</h4>
                <p style="color:#666; font-size:14px; margin:0;">서류 마감까지 D-3 | <b>합격 예측: 매우 높음</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            # 피드 2
            st.markdown("""
            <div class="feed-card">
                <span class="tag">꿀팁</span>
                <h4 style="margin: 10px 0;">현직자가 말하는 "이런 자소서는 바로 탈락합니다"</h4>
                <p style="color:#666; font-size:14px; margin:0;">조회수 2.1k | 좋아요 520</p>
            </div>
            """, unsafe_allow_html=True)

            # 피드 3
            st.markdown(f"""
            <div class="feed-card">
                <span class="tag">멘토링</span>
                <h4 style="margin: 10px 0;">{target_job} 3년차 현직자 무료 커피챗 (선착순 5명)</h4>
                <p style="color:#666; font-size:14px; margin:0;">신청 마감 임박</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("실시간 인기 기업")
            st.markdown("""
            <div class="metric-box" style="text-align:left;">
                <p>🥇 <b>삼성전자</b> <span style="color:red; float:right;">▲ 2</span></p>
                <p>🥈 <b>SK하이닉스</b> <span style="color:gray; float:right;">-</span></p>
                <p>🥉 <b>네이버</b> <span style="color:blue; float:right;">▼ 1</span></p>
                <p>4. <b>현대자동차</b></p>
                <p>5. <b>LG에너지솔루션</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.subheader("📅 주요 일정")
            st.info("2/14: 상반기 공채 설명회")
            st.warning("2/20: 토익 시험 접수 마감")

    # [메인 화면 2] 로드맵/전략 (트랙별 분기 복원)
    elif menu == "🗺️ 나의 로드맵/전략":
        
        # 저학년 로드맵
        if track == 'Junior':
            st.title("🗺️ 커리어 로드맵 (Foundation)")
            st.info(f"{target_job} 전문가로 성장하기 위한 학년별 가이드입니다.")
            
            tab1, tab2 = st.tabs(["1~2학년 (현재)", "3~4학년 (미리보기)"])
            
            with tab1:
                st.markdown("### 🌱 Foundation Phase")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("""
                    <div class="feed-card">
                        <h5>✅ 필수 학업</h5>
                        <hr>
                        <p>□ 전공 기초 학점 3.8 이상 유지</p>
                        <p>□ 영어 기초(토익 700+) 완성</p>
                        <p>□ {0} 관련 교양 수강</p>
                    </div>
                    """.format(target_job), unsafe_allow_html=True)
                with col_b:
                    st.markdown("""
                    <div class="feed-card">
                        <h5>🔥 추천 활동</h5>
                        <hr>
                        <p>□ 교내 마케팅/창업 동아리 가입</p>
                        <p>□ 연합 동아리 네트워킹</p>
                        <p>□ 교외 공모전 1회 도전</p>
                    </div>
                    """, unsafe_allow_html=True)

            with tab2:
                st.write("인턴십과 실무 경험을 쌓는 시기입니다.")
                st.write("- 산학협력 인턴십")
                st.write("- 직무 관련 자격증 (데이터, 자격증 등)")

        # 고학년 전략 분석
        else: # Senior
            st.title("📊 Gap Analysis & Strategy")
            st.info(f"{target_job} 합격 확률을 높이기 위한 AI 전략 리포트입니다.")
            
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                st.subheader("진단 요약")
                st.markdown("""
                <div class="feed-card" style="border-left: 5px solid #4CAF50;">
                    <h4>👍 강점 (Strength)</h4>
                    <p>인턴 경험 1회가 큰 무기입니다. 실무 용어 활용 능력이 우수합니다.</p>
                </div>
                <div class="feed-card" style="border-left: 5px solid #F44336;">
                    <h4>👎 보완점 (Weakness)</h4>
                    <p>정량적 자격증이 부족합니다. 서류 통과율을 높이려면 보완이 필요합니다.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.subheader("스펙 레이더 차트")
                # 차트 데이터
                chart_data = pd.DataFrame({
                    "항목": ["학점", "어학", "직무경험", "자격증", "수상"],
                    "나의 점수": [80, 85, 75, 40, 60],
                    "합격자 평균": [85, 90, 65, 80, 60]
                })
                st.bar_chart(chart_data.set_index("항목"))
                
            st.divider()
            st.markdown("### 💡 Action Plan")
            st.markdown(f"""
            1. **[D-30]** 부족한 **직무 관련 자격증**을 최우선으로 취득하세요.
            2. **[D-60]** 자소서에 '인턴 시절 문제 해결 경험'을 **STAR 기법**으로 정리하세요.
            3. **[추천]** 현재 **원티드**에 올라온 {target_job} 직무 공고에 지원해보세요.
            """)

    elif menu == "📂 내 서류함":
        st.title("📂 내 서류함")
        st.info("업로드한 이력서와 포트폴리오를 관리하는 공간입니다. (준비 중)")
        st.file_uploader("추가 파일 업로드")

    elif menu == "⚙️ 설정":
        st.title("설정")
        st.markdown("##### 내 정보")
        st.write(f"ID: {st.session_state.user_info.get('id', '-')}")
        st.write(f"Email: {st.session_state.user_info.get('email', '-')}")
        st.write(f"Phone: {st.session_state.user_info.get('phone', '-')}")
        
        st.divider()
        if st.button("로그아웃"):
            st.session_state.step = 1
            st.rerun()
