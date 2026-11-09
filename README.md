
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =====================================
# 1. 페이지 기본 설정
# =====================================

st.set_page_config(
    page_title="AI 분리수거 도우미",
    page_icon="♻️",
    layout="wide"
)

# =====================================
# 2. 쓰레기 데이터 설정
# =====================================

ITEMS = {
    "plastic": {
        "name": "플라스틱 물병",
        "image": "images/plastic_bottle.jpg",
        "emoji": "🧴",
        "correct": "플라스틱",
        "prediction": "플라스틱"
    },
    "can": {
        "name": "알루미늄 캔",
        "image": "images/can.jpg",
        "emoji": "🥫",
        "correct": "캔류",
        "prediction": "캔류"
    },
    "paper": {
        "name": "종이컵",
        "image": "images/paper_cup.jpg",
        "emoji": "🥤",
        "correct": "종이컵류",
        "prediction": "일반 종이"
    },
    "glass": {
        "name": "유리병",
        "image": "images/glass_bottle.jpg",
        "emoji": "🍾",
        "correct": "유리류",
        "prediction": "플라스틱"
    },
    "bag": {
        "name": "비닐봉지",
        "image": "images/plastic_bag.jpg",
        "emoji": "🛍️",
        "correct": "비닐류",
        "prediction": "플라스틱"
    },
    "cardboard": {
        "name": "종이 상자",
        "image": "images/cardboard.jpg",
        "emoji": "📦",
        "correct": "종이류",
        "prediction": "종이류"
    },
    "food": {
        "name": "과일 껍질",
        "image": "images/food_waste.jpg",
        "emoji": "🍎",
        "correct": "음식물쓰레기",
        "prediction": "음식물쓰레기"
    }
}

# =====================================
# 3. 분리배출 안내 데이터
# =====================================

GUIDES = {
    "플라스틱":
        "내용물을 비우고 헹군 뒤 라벨을 제거하여 배출합니다.",

    "캔류":
        "내용물을 비우고 가능한 한 압착하여 배출합니다.",

    "일반 종이":
        "물기와 이물질을 제거하고 종이류 배출 기준에 따라 배출합니다.",

    "종이컵류":
        "내용물을 비우고 헹군 뒤 지역별 종이컵 배출 기준을 확인합니다.",

    "유리류":
        "내용물을 비우고 깨끗하게 배출합니다. 깨진 유리는 별도 기준을 확인합니다.",

    "비닐류":
        "이물질을 제거하고 깨끗한 비닐만 분리배출합니다.",

    "종이류":
        "테이프와 이물질을 제거하고 종이류로 배출합니다.",

    "음식물쓰레기":
        "물기를 제거하고 음식물쓰레기 배출 기준에 따라 배출합니다."
}

CATEGORIES = list(GUIDES.keys())

# =====================================
# 4. 세션 상태 초기화
# =====================================

if "selected_item" not in st.session_state:
    st.session_state.selected_item = None

if "records" not in st.session_state:
    st.session_state.records = {}

# =====================================
# 5. 제목 및 소개
# =====================================

st.title("♻️ AI 분리수거 도우미")

st.markdown("""
쓰레기 이미지를 선택하면 분리수거 종류를 예측하고
올바른 분리배출 방법을 알려주는 프로그램입니다.

**목표:** AI의 분류 오류를 확인하고 개선 방향을 찾아봅니다.
""")

st.info(
    "현재 버전은 실제 AI 모델이 아닌 "
    "이미지별 예측 결과를 설정한 분류 시뮬레이션입니다."
)

st.divider()

# =====================================
# 6. 쓰레기 이미지 선택 기능
# =====================================

st.subheader("🔍 분리수거할 쓰레기를 선택하세요.")

cols = st.columns(3)

for index, (key, item) in enumerate(ITEMS.items()):

    with cols[index % 3]:

        # 이미지 파일 확인
        if os.path.isfile(item["image"]):
            st.image(
                item["image"],
                use_container_width=True
            )
        else:
            st.markdown(
                f"<div style='font-size:75px;"
                f"text-align:center;padding:20px;'>"
                f"{item['emoji']}</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            f"<div style='text-align:center;font-weight:bold;'>"
            f"{item['name']}</div>",
            unsafe_allow_html=True
        )

        if st.button(
            "이미지 선택",
            key=f"select_{key}",
            use_container_width=True
        ):
            st.session_state.selected_item = key
            st.rerun()

# =====================================
# 7. 이미지 분류 및 결과 출력
# =====================================

st.divider()
st.subheader("🤖 분리수거 분석 결과")

selected = st.session_state.selected_item

if selected is None:

    st.info("위에서 쓰레기 이미지를 선택해 주세요.")

else:

    item = ITEMS[selected]

    st.write(f"**선택한 물건:** {item['name']}")

    prediction = item["prediction"]
    correct = item["correct"]

    st.markdown(
        f"### AI 예측 결과: {prediction}"
    )

    # 예측 결과 확인
    if prediction == correct:

        st.success("✅ 올바르게 분류했습니다.")

    else:

        st.warning(
            "⚠️ 분류 오류가 발생했습니다. "
            "실제 정답을 확인해 주세요."
        )

    # 분리배출 안내
    st.markdown("### ♻️ 올바른 분리배출 방법")

    st.write(GUIDES[correct])

    st.caption(
        "※ 실제 배출 방법은 제품의 재질과 오염 상태, "
        "지역별 분리배출 기준에 따라 달라질 수 있습니다."
    )

    # =================================
    # 8. 사용자 정답 확인 및 오류 기록
    # =================================

    st.divider()

    st.subheader("📝 AI 예측 결과 확인 및 수정")

    answer = st.selectbox(
        "실제 분리수거 종류를 선택하세요.",
        CATEGORIES,
        index=CATEGORIES.index(correct),
        key=f"answer_{selected}"
    )

    if st.button(
        "정답 확인 및 오류 기록",
        use_container_width=True
    ):

        if answer != correct:

            st.error(
                "입력한 정답이 올바르지 않습니다. "
                "다시 확인해 주세요."
            )

        else:

            is_wrong = prediction != correct

            st.session_state.records[selected] = {
                "물건": item["name"],
                "AI 예측": prediction,
                "실제 정답": correct,
                "오류 여부": "오류" if is_wrong else "정상",
                "기록 시간": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            if is_wrong:
                st.warning(
                    "AI의 오인식 사례가 기록되었습니다."
                )
            else:
                st.success(
                    "정확하게 분류한 사례가 기록되었습니다."
                )

            st.rerun()

# =====================================
# 9. 오류 통계 분석
# =====================================

st.divider()

st.subheader("📊 AI 분류 결과 통계")

records = list(st.session_state.records.values())

total = len(records)

wrong = sum(
    1 for record in records
    if record["오류 여부"] == "오류"
)

correct_count = total - wrong

col1, col2, col3 = st.columns(3)

col1.metric("확인한 이미지", f"{total}개")
col2.metric("정상 분류", f"{correct_count}개")
col3.metric("오인식 횟수", f"{wrong}개")

if total > 0:

    accuracy = (correct_count / total) * 100

    st.write("### 분류 정확도")

    st.progress(int(accuracy))

    st.write(f"확인한 항목 기준 정확도: {accuracy:.1f}%")

    st.write("### 오류 및 분류 기록")

    df = pd.DataFrame(records)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # CSV 다운로드
    csv_data = df.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        label="📥 기록 파일 다운로드",
        data=csv_data,
        file_name="recycling_records.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info(
        "아직 기록된 데이터가 없습니다. "
        "이미지를 선택하고 결과를 확인해 보세요."
    )

# =====================================
# 10. 기록 초기화
# =====================================

st.divider()

with st.expander("⚙️ 기록 관리"):

    st.write("현재 저장된 분류 기록을 초기화할 수 있습니다.")

    if st.button("전체 기록 초기화"):

        st.session_state.records = {}
        st.session_state.selected_item = None

        st.success("기록이 초기화되었습니다.")

        st.rerun()

# =====================================
# 11. 하단 안내
# =====================================

st.divider()

st.caption(
    "AI 분리수거 도우미 | 초기 개발 버전 | "
    "이미지 분류 및 오류 분석 프로젝트"
)
