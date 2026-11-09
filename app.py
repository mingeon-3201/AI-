
import streamlit as st
import os

# 페이지 설정
st.set_page_config(
    page_title="AI 분리수거 도우미",
    page_icon="♻️",
    layout="wide"
)

# 쓰레기 데이터
items = {
    "plastic": {
        "name": "플라스틱 물병",
        "image": "images/plastic_bottle.jpg",
        "correct": "플라스틱",
        "prediction": "플라스틱",
        "emoji": "🧴"
    },
    "can": {
        "name": "알루미늄 캔",
        "image": "images/can.jpg",
        "correct": "캔류",
        "prediction": "캔류",
        "emoji": "🥫"
    },
    "paper": {
        "name": "종이컵",
        "image": "images/paper_cup.jpg",
        "correct": "종이컵류",
        "prediction": "일반 종이",
        "emoji": "🥤"
    },
    "glass": {
        "name": "유리병",
        "image": "images/glass_bottle.jpg",
        "correct": "유리류",
        "prediction": "플라스틱",
        "emoji": "🍾"
    },
    "bag": {
        "name": "비닐봉지",
        "image": "images/plastic_bag.jpg",
        "correct": "비닐류",
        "prediction": "플라스틱",
        "emoji": "🛍️"
    },
    "cardboard": {
        "name": "종이 상자",
        "image": "images/cardboard.jpg",
        "correct": "종이류",
        "prediction": "종이류",
        "emoji": "📦"
    }
}

categories = [
    "플라스틱", "캔류", "일반 종이",
    "종이컵류", "유리류", "비닐류", "종이류"
]

guides = {
    "플라스틱": "내용물을 비우고 깨끗하게 헹군 후 배출합니다.",
    "캔류": "내용물을 비우고 가능한 한 압착하여 배출합니다.",
    "일반 종이": "물기와 이물질을 제거하고 종이류로 배출합니다.",
    "종이컵류": "내용물을 비우고 헹군 뒤 지역별 종이컵 배출 기준을 확인합니다.",
    "유리류": "내용물을 비우고 깨끗하게 배출합니다. 깨진 유리는 별도 기준을 확인합니다.",
    "비닐류": "이물질을 제거하고 깨끗한 비닐만 배출합니다.",
    "종이류": "테이프와 이물질을 제거하고 종이류로 배출합니다."
}

# 세션 데이터 초기화
if "selected" not in st.session_state:
    st.session_state.selected = None

if "errors" not in st.session_state:
    st.session_state.errors = []

# 제목
st.title("♻️ AI 분리수거 도우미")
st.write("쓰레기 이미지를 선택하면 AI가 분리배출 종류를 예측합니다.")
st.divider()

# 이미지 선택
st.subheader("🔍 분리수거할 쓰레기를 선택하세요.")

cols = st.columns(3)

for i, (key, item) in enumerate(items.items()):
    with cols[i % 3]:
        if os.path.exists(item["image"]):
            st.image(item["image"], use_container_width=True)
        else:
            st.markdown(
                f"<div style='font-size:65px;text-align:center;"
                f"padding:20px'>{item['emoji']}</div>",
                unsafe_allow_html=True
            )

        st.write(f"**{item['name']}**")

        if st.button("이 이미지 선택", key=key, use_container_width=True):
            st.session_state.selected = key

# 분석 결과
if st.session_state.selected:
    key = st.session_state.selected
    item = items[key]

    st.divider()
    st.subheader("🤖 AI 분석 결과")

    st.write(f"선택한 물건: **{item['name']}**")
    st.info(f"AI 예측 결과: {item['prediction']}")

    # 예측 결과와 정답 비교
    if item["prediction"] != item["correct"]:
        st.warning("⚠️ 인식 오류가 발생했습니다. 결과를 확인해 주세요.")
    else:
        st.success("✅ 올바르게 분류했습니다.")

    st.write("### 분리배출 방법")
    st.write(guides[item["correct"]])

    st.caption(
        "※ 이 프로그램은 AI 분류를 모방한 초기 시뮬레이션이며, "
        "실제 AI 이미지 분석 결과는 아닙니다."
    )

    st.divider()
    st.subheader("📝 AI 예측 결과 수정")

    answer = st.selectbox(
        "올바른 분리수거 종류를 선택하세요.",
        categories,
        key=f"answer_{key}"
    )

    if st.button("정답 수정 및 기록", use_container_width=True):
        if answer == item["correct"]:
            st.session_state.errors.append({
                "물건": item["name"],
                "AI 예측": item["prediction"],
                "실제 정답": answer,
                "오류 여부": item["prediction"] != answer
            })
            st.success("정답이 확인되고 기록되었습니다!")
        else:
            st.error("정답이 아닙니다. 다시 확인해 주세요.")

# 오류 통계
st.divider()
st.subheader("📊 AI 오류 분석")

total = len(st.session_state.errors)
wrong = sum(
    1 for x in st.session_state.errors if x["오류 여부"]
)

col1, col2 = st.columns(2)

col1.metric("수정 및 확인한 항목", f"{total}개")
col2.metric("AI 오인식 횟수", f"{wrong}개")

if total > 0:
    st.write("### 오류 기록")

    st.dataframe(
        st.session_state.errors,
        use_container_width=True
    )

    if st.button("기록 초기화"):
        st.session_state.errors = []
        st.rerun()
else:
    st.write("아직 기록된 오류가 없습니다.")
