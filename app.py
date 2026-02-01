import streamlit as st
import pandas as pd
import time
import datetime
import graphviz # 로드맵 시각화용

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="Career Map v5.4", page_icon="🧭", layout="wide")

# 세션 상태 관리
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

# 스타일링 (서핏 느낌의 카드 UI)
st.markdown("""
    <style>
    .main {background-color: #F8F9FA;}
    h1, h2, h3 {color: #1A237E; font-family: 'Pretendard', sans-serif;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 8px; width: 100%; height: 45px; font-weight: bold;}
    
    /* 대시보드 카드 스타일 */
    .feed-card {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px;
        border: 1px solid #E0E0E0; transition: transform 0.2s;
    }
    .feed-card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); cursor: pointer; }
    .tag { background-color: #E3F2FD; color: #1565C0; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-right: 5px; }
    .metric-box { background-color: #fff; border: 1px solid #eee; padding: 15px; border-radius: 10px; text-align: center; }
    
    /* 잡다 연동 배너 스타일 */
    .jobda-box {
        background-color: #F3E5F5; border: 1px solid #CE93D8; padding: 15px; border-radius: 10px; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# STEP 1: 로그인 및 회원가입 (v5.2 유지)
# ==========================================
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; margin-top: 50px;'>🧭 Career Map</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>불확실한 미래를 데이터로 확신하다.</p>", unsafe_allow_html=True)
        st.write("")
        
        tab1, tab2 = st.tabs(["로그인", "회원가입 (필수)"])
        
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
                            'id': new_id, 'name': name, 'gender': gender, 'dob': str(dob), 'phone': phone, 'email': email
                        }
                        st.success("가입이 완료되었습니다!")
                        time.sleep(1)
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.error("필수 정보를 모두 입력해주세요.")

# ==========================================
# STEP 2: 트랙 선택 (v5.2 유지)
# ==========================================
elif st.session_state.step == 2:
    user_name = st.session_state.user_info.get('name', '사용자')
    st.title(f"{user_name}님, 환영합니다! 👋")
    st.subheader("현재 상황에 맞는 트랙을 선택하세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("### 🐣 저학년 (1~2학년)")
            st.write("아직 구체적인 진로를 정하지 못했어요.")
            if st.button("저학년 트랙 선택"):
                st.session_state.user_info['track'] = 'Junior'
                st.session_state.step = 3
                st.rerun()
    with col2:
        with st.container(border=True):
            st.markdown("### 🦅 고학년 (3~4학년/취준)")
            st.write("목표 직무가 있고, 합격이 목표예요.")
            if st.button("고학년 트랙 선택"):
                st.session_state.user_info['track'] = 'Senior'
                st.session_state.step = 3
                st.rerun()

# ==========================================
# STEP 3: 상세 진단 & 역량검사 연동 (New!)
# ==========================================
elif st.session_state.step == 3:
    track = st.session_state.user_info.get('track', 'Senior')
    st.title("🧩 데이터 연동 및 진단")
    
    col1, col2 = st.columns(2)
    with col1:
        univ = st.text_input("소속 대학", placeholder="예: 연세대학교")
    with col2:
        major = st.text_input("전공", placeholder="예: 경제학과")

    target_job = st.text_input("관심 직무/분야 (필수)", placeholder="예: 마케팅, 데이터 분석, 금융권 등")
    
    st.write("")
    
    # --- [핵심] 역량검사 데이터 연동 파트 ---
    st.markdown("### 🧬 AI 역량 데이터 연동 (잡다/JOBDA)")
    with st.container(border=True):
        st.markdown("""
        <div class="jobda-box">
            <b>📢 잡다(JOBDA) 역량검사 결과가 있으신가요?</b><br>
            결과표를 업로드하거나 핵심 키워드를 입력하시면, <b>성향 맞춤형 로드맵</b>을 설계해드립니다.
        </div>
        """, unsafe_allow_html=True)
        
        has_jobda = st.radio("역량검사 응시 여부", ["네, 응시했습니다.", "아니요, 아직입니다."], horizontal=True)
        
        jobda_keyword = "미입력"
        if has_jobda == "네, 응시했습니다.":
            col_j1, col_j2 = st.columns(2)
            with col_j1:
                # 파일 업로드 (시늉)
                st.file_uploader("역량검사 결과지 업로드 (PDF)", type=['pdf'])
            with col_j2:
                # 키워드 선택 (MVP용 간편 입력)
                jobda_keyword = st.selectbox("결과지에 나온 나의 핵심 성향 키워드는?", 
                                             ["선택해주세요", "전략가형 (Strategic)", "분석가형 (Analytical)", "소통가형 (Social)", "개척자형 (Challenger)"])
                if jobda_keyword != "선택해주세요":
                    st.success(f"✅ '{jobda_keyword}' 성향이 로드맵에 반영됩니다.")
        else:
            st.info("응시 경험이 없으셔도 기본 성향 검사로 대체 가능합니다.")
            with st.expander("간편 성향 진단 보기"):
                st.radio("선호하는 업무 스타일", ["혼자 깊게 파고들기", "함께 토론하며 풀기"])

    st.write("")
    # 기존 파일 업로드
    uploaded_file = st.file_uploader("📂 이력서/자소서 업로드 (Hard Skill 분석용)", type=['pdf', 'docx'])
    
    st.write("")
    if st.button("🚀 AI 통합 분석 시작하기"):
        if target_job:
            st.session_state.user_info.update({
                'univ': univ, 'major': major, 'target_job': target_job, 'jobda_keyword': jobda_keyword
            })
            
            # 로딩 연출
            progress_text = "잡다(Soft Skill)와 이력서(Hard Skill) 데이터를 결합 중입니다..."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.02)
                my_bar.progress(percent_complete + 1)
            
            st.session_state.step = 4
            st.rerun()
        else:
            st.warning("관심 직무는 필수 입력 사항입니다.")

# ==========================================
# STEP 4: 메인 대시보드 (로드맵 연동 강화)
# ==========================================
elif st.session_state.step == 4:
    
    user_name = st.session_state.user_info.get('name', 'User')
    target_job = st.session_state.user_info.get('target_job', '직무')
    jobda_key = st.session_state.user_info.get('jobda_keyword', '미입력') # 잡다 키워드 가져오기
    track = st.session_state.user_info.get('track', 'Type')
    
    # [사이드바]
    with st.sidebar:
        st.title("🧭 Career Map")
        st.write(f"**{user_name}**님")
        st.caption(f"{st.session_state.user_info.get('univ')} | {track}")
        if "분석가" in jobda_key or "전략가" in jobda_key:
            st.info(f"🧬 **DNA:** {jobda_key}") # 사이드바에 성향 표시
        st.divider()
        menu = st.radio("MENU", ["🏠 홈 (Feed)", "🗺️ 나의 로드맵/전략", "📂 내 서류함", "⚙️ 설정"])

    # [메인 화면 1] 홈 (Feed)
    if menu == "🏠 홈 (Feed)":
        st.header(f"🔥 {target_job} 분야 트렌드")
        
        # 잡다 연동 결과에 따른 맞춤형 배너 (Personalization)
        recomm_text = "회원님의 스펙"
        if "분석가" in jobda_key:
            recomm_text = "회원님의 **분석적 성향(JOBDA)**과 **스펙**"
        
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #6A1B9A 0%, #AB47BC 100%); padding: 25px; border-radius: 12px; color: white; margin-bottom: 25px;">
            <h2 style='color:white; margin:0;'>📢 잡다(JOBDA) 데이터 분석 완료!</h2>
            <p style='margin:5px 0 0 0;'>{recomm_text}을 결합하여 <b>{target_job} 직무 적합도 95%</b>로 확인되었습니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Today's Pick")
            st.markdown(f"""
            <div class="feed-card">
                <span class="tag">채용</span>
                <h4 style="margin: 10px 0;">[LG CNS] {target_job} 신입 채용</h4>
                <p style="color:#666; font-size:14px; margin:0;">
                🧬 <b>{jobda_key}</b> 인재를 우대하는 공고입니다! (서류 가산점 예상)</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feed-card">
                <span class="tag">꿀팁</span>
                <h4 style="margin: 10px 0;">역검 결과가 '안정형'이라면? 자소서 이렇게 쓰세요</h4>
                <p style="color:#666; font-size:14px; margin:0;">조회수 3.4k</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("실시간 랭킹")
            st.markdown("""
            <div class="metric-box" style="text-align:left;">
                <p>🥇 <b>삼성전자</b></p>
                <p>🥈 <b>LG CNS</b> (급상승 🔥)</p>
                <p>🥉 <b>SK하이닉스</b></p>
            </div>
            """, unsafe_allow_html=True)

    # [메인 화면 2] 로드맵/전략
    elif menu == "🗺️ 나의 로드맵/전략":
        
        # 저학년 로드맵 (Graphviz)
        if track == 'Junior':
            st.title(f"🗺️ {target_job} 커리어 로드맵")
            
            # 잡다 키워드에 따라 추천 로드맵이 바뀌는 멘트
            if "분석가" in jobda_key:
                st.success(f"💡 **AI Insight:** '{jobda_key}' 성향을 가진 선배들은 **자격증 취득**을 우선시했습니다.")
            elif "소통가" in jobda_key:
                st.success(f"💡 **AI Insight:** '{jobda_key}' 성향을 가진 선배들은 **대외활동/동아리**에 집중했습니다.")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                graph = graphviz.Digraph()
                graph.attr(rankdir='TB')
                graph.attr('node', shape='box', style='rounded,filled', fillcolor='#E3F2FD', color='#4A90E2', fontname="sans-serif")
                
                graph.node('Start', '🏁 입학 (1학년)', fillcolor='#FFF9C4')
                graph.node('GPA', '📚 학점 관리', fillcolor='#C8E6C9')
                
                # 성향에 따라 강조점 변경 (시각적 차별화)
                if "분석가" in jobda_key:
                    graph.node('Cert', '💳 데이터 자격증 (필수)', fillcolor='#FF8A65', penwidth='3') # 강조
                    graph.node('Club', '🤝 교내 학회', fillcolor='#E3F2FD')
                else:
                    graph.node('Cert', '💳 직무 자격증', fillcolor='#E3F2FD')
                    graph.node('Club', '🤝 연합 동아리 (강추)', fillcolor='#FF8A65', penwidth='3') # 강조

                graph.node('Intern', '💼 인턴십', fillcolor='#FFAB91')
                graph.node('Job', f'🏆 {target_job} 취업', fillcolor='#FFD54F', shape='doubleoctagon')

                graph.edge('Start', 'GPA')
                graph.edge('GPA', 'Cert')
                graph.edge('GPA', 'Club')
                graph.edge('Cert', 'Intern')
                graph.edge('Club', 'Intern')
                graph.edge('Intern', 'Job')
                st.graphviz_chart(graph)
            
            with col2:
                st.info("💡 **잡다(JOBDA) 연계 분석**")
                st.write(f"귀하의 **{jobda_key}** 성향은 연구/분석 직무에서 빛을 발합니다.")
                st.write("다만, **설득/협상 능력**이 부족할 수 있으니 관련 활동을 추천합니다.")

        # 고학년 전략
        else: # Senior
            st.title("📊 합격 전략 리포트")
            st.info(f"잡다 역량검사({jobda_key})와 스펙을 결합한 초개인화 리포트입니다.")
            
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.subheader("종합 진단")
                st.markdown(f"""
                <div class="feed-card" style="border-left: 5px solid #9C27B0;">
                    <h4>🧠 성향 적합도 (Soft Skill)</h4>
                    <p><b>{target_job}</b> 직무와 귀하의 <b>{jobda_key}</b> 성향은 <br>
                    <span style="color:#9C27B0; font-size:20px; font-weight:bold;">95% 일치</span>합니다.</p>
                </div>
                <div class="feed-card" style="border-left: 5px solid #F44336;">
                    <h4>💪 스펙 적합도 (Hard Skill)</h4>
                    <p>하지만 정량적 스펙(자격증)이 부족합니다.<br>
                    <span style="color:#F44336; font-size:20px; font-weight:bold;">70% 수준</span>입니다.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.subheader("보완 전략 (Action Plan)")
                st.markdown("""
                1. **[강점 강화]** 자소서 성격의 장단점 항목에 잡다 결과 키워드('분석력', '치밀함')를 적극 활용하세요.
                2. **[약점 보완]** 성향은 완벽하나 기술(Skill)이 부족합니다. SQLD 자격증으로 '분석력'을 증명할 근거를 만드세요.
                """)
                
                chart_data = pd.DataFrame({
                    "항목": ["성향적합도", "학점", "어학", "직무경험", "자격증"],
                    "점수": [95, 85, 90, 70, 40]
                })
                st.bar_chart(chart_data.set_index("항목"))

    elif menu == "📂 내 서류함":
        st.title("📂 내 서류함")
        st.write("업로드된 파일:")
        st.write("- 역량검사 결과지.pdf")
        st.write("- 이력서_final.pdf")

    elif menu == "⚙️ 설정":
        st.title("설정")
        st.write(f"ID: {st.session_state.user_info.get('id', '-')}")
        if st.button("로그아웃"):
            st.session_state.step = 1
            st.rerun()
