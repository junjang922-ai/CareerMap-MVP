import streamlit as st
import time
import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Career Map - Daily", page_icon="🔥", layout="wide")

# 세션 상태 (데이터 유지용)
if 'streak' not in st.session_state:
    st.session_state.streak = 3  # (가상의) 3일 연속 접속 중
if 'xp' not in st.session_state:
    st.session_state.xp = 1250   # 경험치
if 'notification_on' not in st.session_state:
    st.session_state.notification_on = False

# 스타일링 (듀오링고 느낌의 밝고 둥근 디자인)
st.markdown("""
    <style>
    .main {background-color: #F7F9FC;}
    .stButton>button {border-radius: 20px; font-weight: bold;}
    .quest-box {background-color: white; padding: 15px; border-radius: 15px; border: 2px solid #E0E0E0; margin-bottom: 10px;}
    .streak-fire {font-size: 24px; color: #FF9600; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 (Streak & Status) ---
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("🧭 Career Map")
with col2:
    # 듀오링고 스타일의 재화/스트릭 표시
    st.markdown(f"<div class='streak-fire'>🔥 {st.session_state.streak}일 연속 실천 중!</div>", unsafe_allow_html=True)
with col3:
    st.metric("현재 내 점수(XP)", f"{st.session_state.xp} XP", "+50 today")

st.divider()

# --- 메인 기능 1: 알림 설정 (핵심 기능) ---
if not st.session_state.notification_on:
    with st.container(border=True):
        st.subheader("🔔 합격 알림봇 켜기")
        st.write("듀오링고처럼 매일 정해진 시간에 '오늘의 할 일'을 알려드릴까요?")
        st.write("꾸준함이 합격의 지름길입니다!")
        
        c1, c2 = st.columns([3, 1])
        with c1:
             alarm_time = st.time_input("알림 받을 시간 설정", datetime.time(9, 00))
        with c2:
            st.write("")
            st.write("")
            if st.button("알림 켜기 (ON)"):
                st.session_state.notification_on = True
                st.toast("✅ 알림이 설정되었습니다! 내일 오전 9시에 뵙겠습니다.")
                time.sleep(1)
                st.rerun()
else:
    st.success(f"🔔 매일 {alarm_time.strftime('%H:%M')}에 **[오늘의 커리어 퀘스트]** 알림이 발송됩니다.")

st.write("")

# --- 메인 기능 2: 오늘의 퀘스트 (Daily Quest) ---
st.header("📅 Today's Quests")
st.caption("하루 딱 3개만! 부담 없이 스펙을 쌓아보세요.")

col_q1, col_q2 = st.columns(2)

with col_q1:
    st.markdown("### 🎯 필수 퀘스트 (Daily)")
    
    # 퀘스트 1
    with st.container(border=True):
        chk1 = st.checkbox("📰 경제 뉴스 헤드라인 3개 읽기")
        if chk1:
            st.caption("👍 잘하셨어요! 시사 상식 +10 XP")

    # 퀘스트 2
    with st.container(border=True):
        chk2 = st.checkbox("🔍 채용 공고 1회 훑어보기 (자소설닷컴/링커리어)")
        if chk2:
            st.caption("👀 시장 흐름 파악 완료! +10 XP")

    # 퀘스트 3
    with st.container(border=True):
        chk3 = st.checkbox("💪 토익 영단어 10개 외우기")
        if chk3:
             st.caption("🇺🇸 어학 기초 다지기 성공! +10 XP")
    
    # 보상 로직
    if chk1 and chk2 and chk3:
        st.balloons()
        st.success("🎉 오늘의 퀘스트 올 클리어! 연속 달성일이 내일 +1 됩니다.")

with col_q2:
    st.markdown("### ⚡ 나의 상태 (My Status)")
    # 도넛 차트 등으로 시각화 (진행률)
    progress = 0
    if chk1: progress += 33
    if chk2: progress += 33
    if chk3: progress += 34
    
    st.write(f"오늘의 달성률: **{progress}%**")
    st.progress(progress)
    
    st.write("")
    st.info("💡 **Tip:** 매일 10분씩만 투자해도 1년이면 3650분(60시간)의 스펙 준비 시간이 쌓입니다.")

st.divider()

# --- 메인 기능 3: 장기 로드맵 (기존 기능) ---
with st.expander("🗺️ 나의 전체 로드맵 보러가기 (Map)", expanded=False):
    st.write("매일의 퀘스트가 모여 완성되는 큰 그림입니다.")
    st.image("https://cdn-icons-png.flaticon.com/512/2702/2702134.png", width=100) # 지도 아이콘 예시
    st.write("**[3학년 1학기 목표]**")
    st.checkbox("컴활 1급 필기 합격", value=True)
    st.checkbox("컴활 1급 실기 합격", value=False)
    st.checkbox("하계 인턴 지원서 작성", value=False)
