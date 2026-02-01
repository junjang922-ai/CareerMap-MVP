import streamlit as st
import pandas as pd
import time # 로딩 효과를 위해 필요

# 1. 페이지 설정 및 세션 상태 초기화
st.set_page_config(page_title="Career Map v3.0", page_icon="🧭", layout="wide")

# 세션 상태(단계별 이동) 관리
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

# 스타일링
st.markdown("""
    <style>
    .main {background-color: #F5F7FA;}
    h1 {color: #1A237E;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 8px; width: 100%; height: 50px; font-size: 18px;}
    .success-box {padding: 20px; background-color: #E8F5E9; border-radius: 10px; border: 1px solid #4CAF50;}
    </style>
    """, unsafe_allow_html=True)

# --- STEP 1: 로그인 및 시작하기 ---
if st.session_state.step == 1:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.write("")
        st.markdown("<h1 style='text-align: center;'>🧭 Career Map</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>불확실한 미래를 확신으로 바꾸는 첫 걸음</h4>", unsafe_allow_html=True)
        st.divider()
        
        name_input = st.text_input("이름을 입력해주세요", placeholder="예: 연세인")
        password = st.text_input("비밀번호 (아무거나 입력)", type="password")
        
        if st.button("로그인 / 시작하기"):
            if name_input:
                st.session_state.user_name = name_input
                st.session_state.step = 2
                st.rerun() # 페이지 새로고침
            else:
                st.warning("이름을 입력해주세요.")

# --- STEP 2: 상황 선택 (온보딩) ---
elif st.session_state.step == 2:
    st.title(f"반갑습니다, {st.session_state.user_name}님! 👋")
    st.subheader("현재 어떤 상황에 놓여 계신가요?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🐣 진로 탐색 중 (저학년)")
            st.write("아직 구체적인 직무를 정하지 못했어요.")
            if st.button("로드맵 추천받기"):
                st.session_state.grade_mode = "Junior"
                st.session_state.step = 4 # 업로드 건너뛰기 가능
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 🦅 실전 취업 준비 (고학년)")
            st.write("목표 기업/직무가 있고 스펙 점검이 필요해요.")
            if st.button("합격 확률 진단하기"):
                st.session_state.grade_mode = "Senior"
                st.session_state.step = 3
                st.rerun()

# --- STEP 3: 이력서 업로드 (AI 분석 시뮬레이션) ---
elif st.session_state.step == 3:
    st.title("📄 이력서/포트폴리오 분석")
    st.info("기존에 가지고 계신 이력서나 자소서를 업로드하면, AI가 자동으로 스펙을 추출합니다.")
    
    uploaded_file = st.file_uploader("PDF 또는 Word 파일을 드래그하세요", type=['pdf', 'docx', 'txt'])
    
    if uploaded_file is not None:
        st.success(f"✅ {uploaded_file.name} 업로드 성공!")
        st.write("")
        
        if st.button("AI 정밀 분석 시작 (Click)"):
            # --- AI 분석 퍼포먼스 (Loading Bar) ---
            progress_text = "AI가 문서를 분석하고 있습니다..."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.03) # 3초 동안 로딩
                if percent_complete == 30:
                    my_bar.progress(percent_complete + 1, text="텍스트 추출 중 (OCR)...")
                elif percent_complete == 60:
                    my_bar.progress(percent_complete + 1, text="핵심 역량 및 경험 데이터 파싱 중...")
                elif percent_complete == 90:
                    my_bar.progress(percent_complete + 1, text="합격 데이터와 비교 분석 중...")
                else:
                    my_bar.progress(percent_complete + 1)
            
            time.sleep(1)
            st.session_state.step = 4
            st.rerun()

    st.markdown("---")
    if st.button("건너뛰기 (수동 입력)"):
        st.session_state.step = 4
        st.rerun()

# --- STEP 4: 최종 대시보드 (결과 화면) ---
elif st.session_state.step == 4:
    
    # 1. 사이드바 (재설정)
    with st.sidebar:
        st.header(f"👤 {st.session_state.user_name}님의 프로필")
        st.caption("AI가 추출한 정보입니다. 수정이 필요하면 변경하세요.")
        
        # 만약 파일을 업로드하고 왔다면, 값을 미리 채워주는 연출 (Simulated Parsed Data)
        default_gpa = 3.8 # AI가 읽은 척
        default_toeic = 850
        
        gpa = st.slider("학점", 2.0, 4.3, default_gpa, step=0.1)
        toeic = st.slider("토익", 0, 990, default_toeic, step=10)
        intern_months = st.number_input("인턴 경험(개월)", value=6) # AI가 찾은 척
        
        if st.button("처음으로 돌아가기"):
            st.session_state.step = 1
            st.rerun()

    # 2. 메인 리포트
    st.title("📊 AI 역량 진단 리포트")
    
    # 상단 요약 카드
    st.markdown(f"""
    <div class="success-box">
        <h3>🎉 분석 완료!</h3>
        <p>업로드하신 이력서에서 <b>[인턴 6개월]</b>, <b>[마케팅 학회 경험]</b>이 감지되었습니다.<br>
        이를 바탕으로 계산된 <b>삼성전자 마케팅 직무</b> 합격 확률입니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # 여백

    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        # 점수 계산 (단순 로직)
        final_prob = min(40 + (gpa*5) + (intern_months*5), 96)
        
        st.markdown("### 예상 합격 확률")
        st.markdown(f"<h1 style='font-size: 80px; color:#4A90E2;'>{int(final_prob)}%</h1>", unsafe_allow_html=True)
        if final_prob > 80:
            st.caption("안정권입니다! 면접 준비에 집중하세요.")
        else:
            st.caption("조금 더 스펙 보완이 필요합니다.")

    with col2:
        st.markdown("### ⚡ AI의 전략 제안")
        tab1, tab2 = st.tabs(["강점 분석", "보완 로드맵"])
        
        with tab1:
            st.write("👍 **Positives:**")
            st.success("인턴십 6개월 경험이 가장 큰 경쟁력입니다.")
            st.success("학점이 3.8로 성실함을 증명하고 있습니다.")
            st.write("👎 **Improvements:**")
            st.warning("비즈니스 영어(OPIc) 점수가 확인되지 않습니다.")
        
        with tab2:
            st.write("🚀 **다음 달까지 할 일:**")
            st.checkbox("OPIc IH 등급 취득하기", value=False)
            st.checkbox("포트폴리오에 '데이터 분석' 역량 한 줄 추가하기", value=True)

    st.divider()
    st.markdown("#### 🎁 상세 리포트를 PDF로 받아보시겠습니까?")
    st.button("이메일로 전체 리포트 전송받기")
