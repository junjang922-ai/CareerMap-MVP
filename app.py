import streamlit as st
import pandas as pd
import time
import datetime
import random # 다이어리 질문 랜덤 생성용
import graphviz # 로드맵 시각화용 (필수)

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="Career Map v6.0", page_icon="🧭", layout="wide")

# 세션 상태 관리
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

# [New] 다이어리 데이터 초기화
if 'diary_logs' not in st.session_state:
    st.session_state.diary_logs = [
        {"date": "2026-02-01", "q": "오늘 가장 뿌듯했던 일은?", "a": "사수님께 엑셀 정리 잘했다고 칭찬받음! VLOOKUP 드디어 마스터했다."},
        {"date": "2026-02-02", "q": "오늘 실수한 점이 있다면?", "a": "메일 참조(CC)에 팀장님을 빼먹었다... 다음엔 꼭 더블체크 하자."}
    ] # 예시 데이터
if 'diary_streak' not in st.session_state:
    st.session_state.diary_streak = 3 # 연속 기록일 수 (가짜 데이터)

# 스타일링
st.markdown("""
    <style>
    .main {background-color: #F8F9FA;}
    h1, h2, h3 {color: #1A237E; font-family: 'Pretendard', sans-serif;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 8px; width: 100%; height: 45px; font-weight: bold;}
    
    .feed-card {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px;
        border: 1px solid #E0E0E0; transition: transform 0.2s;
    }
    .feed-card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); cursor: pointer; }
    .tag { background-color: #E3F2FD; color: #1565C0; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-right: 5px; }
    .metric-box { background-color: #fff; border: 1px solid #eee; padding: 15px; border-radius: 10px; text-align: left; }
    .ai-box { background-color: #F3E5F5; border: 1px solid #CE93D8; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    
    /* [New] 다이어리 스타일 */
    .diary-card {
        background-color: #FFF3E0; border-left: 5px solid #FF9800; padding: 15px; border-radius: 10px; margin-bottom: 10px;
    }
    .question-box {
        font-size: 18px; font-weight: bold; color: #E65100; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# STEP 1: 로그인 및 회원가입
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
# STEP 2: 트랙 선택
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
# STEP 3: 상세 진단 & 역량검사 추가
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
    
    st.markdown("### 🧬 AI 역량/성향 데이터 연동")
    with st.container(border=True):
        st.markdown("""
        <div class="ai-box">
            <b>📢 외부 AI 역량검사 혹은 인성검사 결과표가 있으신가요?</b><br>
            결과표를 업로드하거나 핵심 키워드를 입력하시면, <b>성향 맞춤형 로드맵</b>을 설계해드립니다.
        </div>
        """, unsafe_allow_html=True)
        
        has_test = st.radio("검사 결과 보유 여부", ["네, 있습니다.", "아니요, 없습니다."], horizontal=True)
        
        test_keyword = "미입력"
        if has_test == "네, 있습니다.":
            col_j1, col_j2 = st.columns(2)
            with col_j1:
                st.file_uploader("검사 결과표 업로드 (PDF/JPG)", type=['pdf', 'jpg', 'png'])
            with col_j2:
                test_keyword = st.selectbox("결과표의 핵심 성향 키워드는?", 
                                             ["선택해주세요", "전략가형 (Strategic)", "분석가형 (Analytical)", "소통가형 (Social)", "개척자형 (Challenger)"])
                if test_keyword != "선택해주세요":
                    st.success(f"✅ '{test_keyword}' 성향 데이터를 반영합니다.")
        else:
            st.info("자체 간편 진단으로 대체합니다.")
            with st.expander("간편 성향 진단 진행하기"):
                st.radio("선호하는 업무 스타일", ["혼자 깊게 파고들기", "함께 토론하며 풀기"])

    st.write("")
    uploaded_file = st.file_uploader("📂 이력서/자소서 업로드 (Hard Skill 분석용)", type=['pdf', 'docx'])
    
    st.write("")
    if st.button("🚀 AI 통합 분석 시작하기"):
        if target_job:
            st.session_state.user_info.update({
                'univ': univ, 'major': major, 'target_job': target_job, 'test_keyword': test_keyword
            })
            
            progress_text = "성향(Soft Skill)과 이력서(Hard Skill) 데이터를 결합 중입니다..."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.02)
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
    target_job = st.session_state.user_info.get('target_job', '직무')
    test_key = st.session_state.user_info.get('test_keyword', '미입력')
    track = st.session_state.user_info.get('track', 'Type')
    
    # [사이드바]
    with st.sidebar:
        st.title("🧭 Career Map")
        st.write(f"**{user_name}**님")
        st.caption(f"{st.session_state.user_info.get('univ')} | {track}")
        
        if "분석가" in test_key or "전략가" in test_key:
            st.info(f"🧬 **DNA:** {test_key}")
        elif "소통가" in test_key or "개척자" in test_key:
            st.success(f"🧬 **DNA:** {test_key}")
            
        st.divider()
        # [New] '업무 다이어리' 메뉴 추가
        menu = st.radio("MENU", ["🏠 홈 (Feed)", "🗺️ 나의 로드맵/전략", "📝 업무 다이어리", "📂 내 서류함", "⚙️ 설정"])
        
        st.divider()
        st.markdown("💡 **Premium Service**")
        st.write("현직자 1:1 멘토링 매칭")

    # [1] 홈 (Feed)
    if menu == "🏠 홈 (Feed)":
        st.header(f"🔥 {target_job} 분야 트렌드")
        
        recomm_text = "회원님의 스펙"
        if "분석가" in test_key or "전략가" in test_key:
            recomm_text = f"회원님의 **{test_key} 성향**과 **스펙**"
        
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #6A1B9A 0%, #AB47BC 100%); padding: 25px; border-radius: 12px; color: white; margin-bottom: 25px;">
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
                <p style="color:#666; font-size:14px; margin:0;">
                🧬 <b>{test_key}</b> 인재를 선호하는 공고입니다! (성향 매칭됨)</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feed-card">
                <span class="tag">꿀팁</span>
                <h4 style="margin: 10px 0;">현직자가 말하는 "이런 자소서는 바로 탈락합니다"</h4>
                <p style="color:#666; font-size:14px; margin:0;">조회수 2.1k | 좋아요 520</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="feed-card">
                <span class="tag">멘토링</span>
                <h4 style="margin: 10px 0;">{target_job} 3년차 현직자 무료 커피챗 (선착순 5명)</h4>
                <p style="color:#666; font-size:14px; margin:0;">신청 마감 임박</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("실시간 랭킹")
            st.markdown("""
            <div class="metric-box">
                <p>🥇 <b>삼성전자</b> <span style="color:red; float:right;">▲ 2</span></p>
                <p>🥈 <b>SK하이닉스</b> <span style="color:gray; float:right;">-</span></p>
                <p>🥉 <b>네이버</b> <span style="color:blue; float:right;">▼ 1</span></p>
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
        
        if track == 'Junior':
            st.title(f"🗺️ {target_job} 커리어 로드맵")
            
            if "분석가" in test_key:
                st.success(f"💡 **AI Insight:** '{test_key}' 성향을 가진 선배들은 **데이터 자격증** 취득 시 취업률이 20% 높았습니다.")
            elif "소통가" in test_key:
                st.success(f"💡 **AI Insight:** '{test_key}' 성향을 가진 선배들은 **리더십 경험(학회장)**이 합격의 열쇠였습니다.")
            else:
                st.info(f"💡 **AI Insight:** 선배들의 합격 데이터를 기반으로 최적 경로를 추천합니다.")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                graph = graphviz.Digraph()
                graph.attr(rankdir='TB')
                graph.attr('node', shape='box', style='rounded,filled', fillcolor='#E3F2FD', color='#4A90E2', fontname="sans-serif")
                
                graph.node('Start', '🏁 입학 (1학년)', fillcolor='#FFF9C4')
                graph.node('GPA', '📚 학점 관리', fillcolor='#C8E6C9')
                
                if "분석가" in test_key:
                    graph.node('Cert', '💳 데이터 자격증 (필수)', fillcolor='#FF8A65', penwidth='3') 
                elif "소통가" in test_key:
                    graph.node('Club', '🤝 연합 동아리 (강추)', fillcolor='#FF8A65', penwidth='3')

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
                st.info("💡 **성향 연계 솔루션**")
                st.write(f"귀하의 **{test_key}** 성향은 연구/분석 직무에서 빛을 발합니다.")
                st.write("다만, **설득/협상 능력**이 부족할 수 있으니 관련 활동을 추천합니다.")
                st.divider()
                st.write("🚀 **추천 활동**")
                st.checkbox("SQLD 자격증 따기")
                st.checkbox("Y.E.S 경제학회 지원하기")

        else: # Senior
            st.title("📊 합격 전략 리포트")
            st.info(f"AI 역량검사 결과({test_key})와 스펙을 결합한 초개인화 리포트입니다.")
            
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.subheader("종합 진단")
                st.markdown(f"""
                <div class="feed-card" style="border-left: 5px solid #9C27B0;">
                    <h4>🧠 성향 적합도 (Soft Skill)</h4>
                    <p><b>{target_job}</b> 직무와 귀하의 <b>{test_key}</b> 성향은 <br>
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
                1. **[강점 강화]** 자소서 성격의 장단점 항목에 AI 진단 키워드('분석력', '치밀함')를 적극 활용하세요.
                2. **[약점 보완]** 성향은 완벽하나 기술(Skill)이 부족합니다. SQLD 자격증으로 '분석력'을 증명할 근거를 만드세요.
                """)
                
                chart_data = pd.DataFrame({
                    "항목": ["성향적합도", "학점", "어학", "직무경험", "자격증"],
                    "점수": [95, 85, 90, 70, 40]
                })
                st.bar_chart(chart_data.set_index("항목"))

    # [3] 업무 다이어리 (New Feature!)
    elif menu == "📝 업무 다이어리":
        st.title("📝 인턴 업무 다이어리 (Career Log)")
        st.caption("매일 3분, 질문에 답하며 나만의 업무 자산을 쌓아보세요. (AI 자소서의 기초 데이터가 됩니다)")
        
        # 1. 연속 기록 (Streak)
        st.markdown(f"""
        <div style="background-color:#FFF3E0; padding:15px; border-radius:10px; margin-bottom:20px; text-align:center;">
            <h3 style="color:#E65100; margin:0;">🔥 {st.session_state.diary_streak}일째 기록 중!</h3>
            <p style="margin:5px 0 0 0;">하루만 더 쓰면 레벨업! 꾸준함이 최고의 스펙입니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. 오늘의 질문 (랜덤 추천)
        today_questions = [
            "오늘 사수님이나 동료에게 들은 피드백이 있나요?",
            "오늘 업무 중 가장 뿌듯했던 순간은 언제인가요?",
            "오늘 실수하거나 아쉬웠던 점은 무엇인가요?",
            "오늘 새로 배운 업무 용어나 스킬이 있나요?"
        ]
        if 'today_q' not in st.session_state:
            st.session_state.today_q = random.choice(today_questions)
            
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown(f"""
            <div class="question-box">Q. {st.session_state.today_q}</div>
            """, unsafe_allow_html=True)
            
            # 답변 입력
            diary_input = st.text_area("답변을 입력하세요", height=100, placeholder="예: 오늘 엑셀 VLOOKUP 함수를 써서 1시간 걸릴 일을 10분 만에 끝냈다. 팀장님이 손이 빠르다고 칭찬해주셨다.")
            
            if st.button("오늘의 기록 저장하기 ✨"):
                if diary_input:
                    # 로그 저장
                    new_log = {
                        "date": datetime.date.today().strftime("%Y-%m-%d"),
                        "q": st.session_state.today_q,
                        "a": diary_input
                    }
                    st.session_state.diary_logs.insert(0, new_log) # 최신순 추가
                    st.session_state.diary_streak += 1 # 스트릭 증가
                    st.success("저장되었습니다! 내일도 잊지 마세요.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("내용을 입력해주세요.")
                    
        with col2:
            st.markdown("### 📅 지난 기록 모아보기")
            for log in st.session_state.diary_logs:
                st.markdown(f"""
                <div class="diary-card">
                    <span style="font-size:12px; color:#666;">{log['date']}</span><br>
                    <b>Q. {log['q']}</b><br>
                    <span style="color:#333;">{log['a']}</span>
                </div>
                """, unsafe_allow_html=True)

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
