import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 페이지 설정
st.set_page_config(
    page_title="Career Map v2.0",
    page_icon="🧭",
    layout="wide"
)

# 2. 스타일링 (Sky & Lemon 테마)
st.markdown("""
    <style>
    .main {background-color: #F5F7FA;}
    h1 {color: #1A237E;}
    .stButton>button {background-color: #4A90E2; color: white; border-radius: 10px; width: 100%;}
    .metric-card {background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바: 기본 프로필
with st.sidebar:
    st.title("🧭 Career Map")
    st.caption("v2.0 | 정밀 진단 모드")
    
    st.header("👤 기본 프로필")
    user_name = st.text_input("이름", "연세인")
    univ = st.selectbox("소속 대학", ["연세대", "고려대", "서울대", "서성한", "기타"])
    major = st.text_input("주전공", "경제학과")
    grade = st.radio("현재 상태", ["3~4학년 (실전 취준)", "1~2학년 (진로 탐색)"])

# 4. 메인 화면
st.title(f"🚀 {user_name}님의 커리어 진단 리포트")

# --- Track A: 실전 취준 (데이터 입력 강화) ---
if grade == "3~4학년 (실전 취준)":
    st.info("💡 더 정밀한 분석을 위해 상세 스펙을 입력해주세요. 입력값에 따라 합격 확률이 실시간으로 변합니다.")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("📝 상세 스펙 입력")

        # 섹션 1: 학업 (Academic)
        with st.expander("🎓 학업 및 전공 (Academic)", expanded=True):
            gpa = st.slider("학점 (4.3 만점)", 2.0, 4.3, 3.5, step=0.1)
            double_major = st.checkbox("복수/부전공 이수 중인가요?")

        # 섹션 2: 어학 (Language)
        with st.expander("🗣️ 어학 능력 (Global)", expanded=True):
            toeic = st.slider("토익 점수", 0, 990, 800, step=10)
            speaking = st.select_slider("스피킹 (OPIc/토스)", options=["None", "IM1", "IM2", "IM3", "IH", "AL"])
            second_lang = st.checkbox("제2외국어 가능 (중국어/일본어 등)")

        # 섹션 3: 실무 경험 (Experience) - 여기가 핵심!
        with st.expander("💼 실무 및 활동 (Experience)", expanded=True):
            intern_months = st.number_input("인턴십 근무 개월 수 (없으면 0)", min_value=0, max_value=24, value=0)
            awards = st.number_input("교내외 공모전 수상 횟수", min_value=0, value=0)
            activity = st.number_input("대외활동/동아리 경험 횟수", min_value=0, value=1)
            license_count = st.number_input("직무 관련 자격증 개수 (컴활, CFA 등)", min_value=0, value=0)

    with col2:
        st.subheader("📊 AI 진단 결과")
        
        # --- 점수 계산 로직 (가상 알고리즘) ---
        # 기본점수 + 학점
        score = 30 + (gpa * 8) 
        
        # 어학 가산점
        if toeic >= 900: score += 10
        elif toeic >= 800: score += 5
        
        if speaking in ["IH", "AL"]: score += 10
        elif speaking == "IM3": score += 5
        
        if second_lang: score += 5

        # 경험 가산점 (여기가 중요)
        score += (intern_months * 3) # 인턴 개월당 3점
        score += (awards * 5)        # 수상 1회당 5점
        score += (license_count * 3)
        if double_major: score += 5

        # 최대 99점 제한
        final_prob = min(int(score), 99)

        # 결과 카드 표시
        st.markdown(f"""
        <div class="metric-card">
            <h3 style='margin:0; color:#555;'>예상 합격 확률</h3>
            <h1 style='font-size: 60px; color:#4A90E2; margin:0;'>{final_prob}%</h1>
            <p style='color:#666;'>지원자 상위 {max(1, 100-final_prob)}% 수준</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") # 여백

        # 피드백 메시지 로직
        if intern_months == 0:
            st.error("🚨 **치명적 약점:** 실무 경험(인턴)이 부족합니다. 요즘 채용은 '직무 경험'이 1순위입니다. 방학 인턴이 시급합니다.")
        elif toeic < 850 and speaking in ["None", "IM1", "IM2"]:
            st.warning("⚠️ **주의:** 어학 점수가 안정권보다 낮습니다. 서류 통과율을 높이려면 오픽 IH가 필요합니다.")
        elif awards == 0 and activity < 2:
            st.warning("⚠️ **주의:** 정량 스펙은 좋으나, 자소서에 쓸 '스토리(활동)'가 부족해 보입니다.")
        elif final_prob >= 80:
            st.success("🎉 **탁월함:** 스펙 밸런스가 아주 좋습니다! 이제 자소서와 면접 준비에 올인하세요.")
        else:
            st.info("💡 **조언:** 강점을 하나 더 만드세요. 자격증 취득이나 공모전 참여를 추천합니다.")

        # 레이더 차트 데이터 (임시)
        chart_data = pd.DataFrame({
            "영역": ["학업", "어학", "실무경험", "대외활동"],
            "내 점수": [gpa*20, toeic/10, min(intern_months*15, 100), min(activity*20, 100)],
            "합격자 평균": [85, 90, 60, 70] # 3.5학점, 900점, 인턴 4개월, 활동 3회 기준
        })
        st.bar_chart(chart_data.set_index("영역"))


# --- Track B: 저학년 (로드맵) ---
else:
    st.header("🗺️ 학년별 성장 로드맵")
    st.info(f"{user_name}님의 전공({major})과 학년을 고려한 맞춤 로드맵입니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ **지금 꼭 해야 할 것 (Priority)**")
        st.checkbox("학점 3.8 이상 만들기 (재수강 체크)")
        st.checkbox("진로 탐색: 교내 취업지원팀 상담 받기")
        st.checkbox("영어 기초 쌓기 (토익 700+ 목표)")
    
    with col2:
        st.warning("🔜 **미리 준비하면 좋은 것**")
        st.checkbox("직무 관련 학회/동아리 리크루팅 일정 확인")
        st.checkbox("컴활 / 한국사 자격증 (공기업/대기업 공통)")
