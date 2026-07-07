import streamlit as st

# 페이지 설정
st.set_page_config(page_title="3학년 선택과목 규칙 점검기", page_icon="🏫", layout="wide")

st.title("🏫 3학년 선택과목 규칙 점검기")
st.write("2학년 여러분, 3학년 선택과목 유의사항이 헷갈리시죠? 아래에서 본인의 상황과 선택하려는 과목을 고르면 규칙에 어긋나는지 확인해 드립니다!")

# --- 1. 과목 데이터 분류 ---
# (학교 교육과정 편제표를 바탕으로 한 기본 분류입니다. 필요시 수정하세요.)
SUBJECTS_3_1 = {
    "국어/수학/영어": ["주제 탐구 독서", "미적분II", "미디어 영어"],
    "사회/과학": ["도시의 미래 탐구", "법과 사회", "역사로 탐구하는 현대 세계", "사회문제 탐구", "윤리문제 탐구", "전자기와 양자", "화학 반응의 세계", "세포와 물질대사", "행성우주과학"],
    "체육/예술": ["기초 체육 전공 실기", "실용음악실기I", "미술실기I"],
    "기술·가정/정보/외국어/교양": ["데이터 과학", "중국어 회화", "독일어 회화", "한문 고전 읽기", "교육의 이해", "보건", "논술"]
}

SUBJECTS_3_2 = {
    "국어/수학/영어": ["매체 의사소통", "경제 수학", "심화 영어"],
    "사회/과학": ["여행지리", "금융과 경제생활", "인문학과 윤리", "국제 관계의 이해", "기후변화와 지속가능한 세계", "기후변화와 환경생태", "융합과학 탐구", "생태와 환경"],
    "체육/예술": ["심화 체육 전공 실기", "실용음악실기II", "미술실기II"],
    "기술·가정/정보/외국어/교양": ["소프트웨어와 생활", "심화 중국어", "심화 독일어", "생활과 한문", "논리와 사고", "인간과 심리"]
}

def get_category(subject, semester_dict):
    for category, subjects in semester_dict.items():
        if subject in subjects:
            return category
    return None

# --- 2. 사용자 입력 ---
st.header("📝 1단계: 2학년 수강 내역 입력")
col1, col2 = st.columns(2)
with col1:
    history_kme = st.number_input("2학년 때 수강한 '국어/수학/영어' 선택과목 개수 (학기당 1개 기준 최대 2개)", min_value=0, max_value=2, value=0)
with col2:
    history_ss_taken = st.radio("2학년 때 '사회/과학' 교과를 1과목 이상 수강했나요?", ("예", "아니오"))

st.header("📝 2단계: 3학년 선택과목 고르기")
col3, col4 = st.columns(2)
with col3:
    st.subheader("3학년 1학기")
    all_3_1 = sum(SUBJECTS_3_1.values(), [])
    sel_3_1 = st.multiselect("3학년 1학기 과목을 선택하세요.", all_3_1)

with col4:
    st.subheader("3학년 2학기")
    all_3_2 = sum(SUBJECTS_3_2.values(), [])
    sel_3_2 = st.multiselect("3학년 2학기 과목을 선택하세요. (택4)", all_3_2)

# --- 3. 규칙 검사 로직 ---
if st.button("규칙 검사하기", type="primary"):
    errors = []
    
    # 카운팅 로직
    counts_1 = {"국어/수학/영어": 0, "사회/과학": 0, "체육/예술": 0, "기술·가정/정보/외국어/교양": 0}
    counts_2 = {"국어/수학/영어": 0, "사회/과학": 0, "체육/예술": 0, "기술·가정/정보/외국어/교양": 0}
    
    for sub in sel_3_1:
        cat = get_category(sub, SUBJECTS_3_1)
        if cat: counts_1[cat] += 1
        
    for sub in sel_3_2:
        cat = get_category(sub, SUBJECTS_3_2)
        if cat: counts_2[cat] += 1

    total_kme = history_kme + counts_1["국어/수학/영어"] + counts_2["국어/수학/영어"]
    
    # 📌 공통 및 1학기 유의사항 점검
    if counts_1["국어/수학/영어"] > 1:
        errors.append("❌ [3학년 1학기] 국어, 수학, 영어 교과는 최대 1과목만 선택할 수 있습니다.")
    if counts_1["체육/예술"] > 1:
        errors.append("❌ [3학년 1학기] 체육/예술 교과는 최대 1과목만 선택할 수 있습니다.")
    if counts_1["기술·가정/정보/외국어/교양"] != 1:
        errors.append("❌ [3학년 1학기] 기술·가정/정보/제2외국어/한문/교양 교과 중 **반드시 1과목**을 선택해야 합니다.")
        
    # 📌 2학기 유의사항 점검
    if counts_2["국어/수학/영어"] > 1:
        errors.append("❌ [3학년 2학기] 국어, 수학, 영어 교과는 최대 1과목만 선택할 수 있습니다.")
    if (history_kme + counts_1["국어/수학/영어"]) >= 3 and counts_2["국어/수학/영어"] > 0:
        errors.append("❌ [3학년 2학기] 3학년 1학기까지 국영수 교과를 3개 선택했으므로, 2학기에는 선택할 수 없습니다.")
    if total_kme > 3:
        errors.append(f"❌ [전체] 2, 3학년 국영수 선택 교과는 최대 3과목까지만 가능합니다. (현재 {total_kme}과목 선택함)")
        
    if history_ss_taken == "아니오" and counts_1["사회/과학"] == 0 and counts_2["사회/과학"] == 0:
        errors.append("❌ [3학년 2학기] 3학년 1학기까지 사회/과학 교과를 1개도 선택하지 않았다면, 2학기에는 반드시 1과목 이상 선택해야 합니다.")
        
    if counts_2["체육/예술"] > 1:
        errors.append("❌ [3학년 2학기] 체육/예술 교과는 최대 1과목만 선택할 수 있습니다.")
    if counts_2["기술·가정/정보/외국어/교양"] != 1:
        errors.append("❌ [3학년 2학기] 기술·가정/정보/제2외국어/한문/교양 교과 중 **반드시 1과목**을 선택해야 합니다.")

    # --- 4. 결과 출력 ---
    st.divider()
    if not errors:
        st.success("🎉 축하합니다! 유의사항을 모두 준수하여 완벽하게 과목을 선택했습니다.")
        st.balloons()
    else:
        st.error("⚠️ 아래의 유의사항 위반 항목을 확인하고 과목 선택을 수정해주세요.")
        for err in errors:
            st.write(err)

    # 요약 표 보여주기
    st.write("### 📊 나의 선택 요약")
    colA, colB = st.columns(2)
    colA.metric(label="현재까지 총 국영수 선택 수 (최대 3)", value=f"{total_kme}과목")
    colB.metric(label="사회/과학 이수 여부 (필수)", value="충족" if history_ss_taken=="예" or counts_1["사회/과학"]>0 or counts_2["사회/과학"]>0 else "미충족")
