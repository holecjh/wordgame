import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="대한민국 헌법 문장 만들기 게임",
    page_icon="🇰🇷",
    layout="centered",
)

# 커스텀 CSS (애니메이션 및 색상 효과)
st.markdown(
    """
    <style>
    .correct-box {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #c3e6cb;
        text-align: center;
        font-weight: bold;
        animation: popUp 0.3s ease-in-out;
    }
    .wrong-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #f5c6cb;
        text-align: center;
        font-weight: bold;
        animation: shake 0.4s ease-in-out;
    }
    @keyframes popUp {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-6px); }
        75% { transform: translateX(6px); }
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.03);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 10문제 데이터 정의 (난이도별 단어 수: 7개 ~ 10개)
PROBLEMS = [
    # 난이도 1 (7단어)
    {
        "level": "난이도 1 (7단어)",
        "title": "헌법 제5조",
        "text": "대한민국은 / 국제평화의 / 유지에 / 노력하고 / 침략적 / 전쟁을 / 부인한다.",
    },
    {
        "level": "난이도 1 (7단어)",
        "title": "헌법 제17조",
        "text": "모든 / 국민은 / 사생활의 / 비밀과 / 자유를 / 침해받지 / 아니한다.",
    },
    {
        "level": "난이도 1 (7단어)",
        "title": "헌법 제27조",
        "text": "형사피고인은 / 유죄의 / 판결이 / 확정될 / 때까지는 / 무죄로 / 추정된다.",
    },
    # 난이도 2 (8단어)
    {
        "level": "난이도 2 (8단어)",
        "title": "헌법 제1조",
        "text": "대한민국의 / 주권은 / 국민에게 / 있고 / 모든 / 권력은 / 국민으로부터 / 나온다.",
    },
    {
        "level": "난이도 2 (8단어)",
        "title": "헌법 제34조",
        "text": "국가는 / 재해를 / 예방하고 / 그 위험으로부터 / 국민을 / 보호하기 위하여 / 노력하여야 / 한다.",
    },
    {
        "level": "난이도 2 (8단어)",
        "title": "헌법 제37조",
        "text": "국민의 / 자유와 / 권리는 / 헌법에 / 열거되지 / 아니한 이유로 / 경시되지 / 아니한다.",
    },
    # 난이도 3 (9단어)
    {
        "level": "난이도 3 (9단어)",
        "title": "헌법 제2조",
        "text": "국가는 / 법률이 / 정하는 / 바에 / 의하여 / 재외국민을 / 보호할 / 의무를 / 진다",
    },
    {
        "level": "난이도 3 (9단어)",
        "title": "헌법 제12조",
        "text": "모든 / 국민은 / 고문을 / 받지 아니하며 / 형사상 / 자기에게 / 불리한 / 진술을 / 강요당하지 아니한다",
    },
    {
        "level": "난이도 3 (9단어)",
        "title": "헌법 제21조",
        "text": "모든 / 국민은 / 언론 / 출판의 / 자유와 / 집회 / 결사의 / 자유를 / 가진다.",
    },
    # 난이도 4 (10단어)
    {
        "level": "난이도 4 (10단어)",
        "title": "헌법 제10조",
        "text": "모든 / 국민은 / 인간으로서의 / 존엄과 / 가치를 / 가지며 / 행복을 / 추구할 / 권리를 / 가진다",
    },
]

# 세션 상태 초기화
if "current_q" not in st.session_state:
  st.session_state.current_q = 0
if "score" not in st.session_state:
  st.session_state.score = 0
if "placed_words" not in st.session_state:
  st.session_state.placed_words = []
if "shuffled_words" not in st.session_state:
  st.session_state.shuffled_words = []
if "feedback" not in st.session_state:
  st.session_state.feedback = None  # "correct", "wrong"
if "game_over" not in st.session_state:
  st.session_state.game_over = False


def load_question(idx):
  prob = PROBLEMS[idx]
  correct_list = [w.strip() for w in prob["text"].split("/")]
  shuffled = correct_list.copy()
  random.shuffle(shuffled)
  st.session_state.correct_list = correct_list
  st.session_state.shuffled_words = shuffled
  st.session_state.placed_words = []
  st.session_state.feedback = None


# 게임 초기 로딩
if not st.session_state.shuffled_words and not st.session_state.game_over:
  load_question(st.session_state.current_q)

# 타이틀
st.title("🇰🇷 대한민국 헌법 문장 만들기 게임")
st.markdown("올바른 순서대로 단어를 클릭하여 헌법 조문을 완성하세요!")
st.divider()

if not st.session_state.game_over:
  current_prob = PROBLEMS[st.session_state.current_q]

  # 진행 상태 표시
  col1, col2 = st.columns([2, 1])
  with col1:
    st.subheader(f"문제 {st.session_state.current_q + 1} / 10")
    st.markdown(f"**[{current_prob['level']}] {current_prob['title']}**")
  with col2:
    st.metric("현재 점수", f"{st.session_state.score} 점")

  st.write("")

  # 1. 현재 맞추고 있는 완성 영역 (하단 배치)
  st.markdown("### 🧩 완성된 문장 칸")
  correct_list = st.session_state.correct_list
  placed = st.session_state.placed_words

  # 슬롯 시각화
  slot_cols = st.columns(len(correct_list))
  for i, col in enumerate(slot_cols):
    with col:
      if i < len(placed):
        st.markdown(
            f'<div class="correct-box">{placed[i]}</div>', unsafe_allow_html=True
        )
      else:
        st.markdown(
            '<div style="background-color: #f1f3f5; color: #adb5bd; padding:'
            ' 10px; border-radius: 8px; text-align: center; border: 2px dashed'
            ' #ced4da;">빈칸</div>',
            unsafe_allow_html=True,
        )

  st.write("")
  st.divider()

  # 피드백 메시지 표시
  if st.session_state.feedback == "wrong":
    st.markdown(
        '<div class="wrong-box">❌ 틀렸습니다! 올바른 순서가 아닙니다. 다시'
        " 도전해보세요!</div>",
        unsafe_allow_html=True,
    )
  elif st.session_state.feedback == "correct_step":
    st.markdown(
        '<div class="correct-box">✅ 맞았습니다! 다음 단어를 선택하세요.</div>',
        unsafe_allow_html=True,
    )

  # 2. 선택 가능한 단어들 (돌아다니는 단어 콘셉트 -> 버튼 형태로 배치)
  st.markdown("### 🔀 단어 선택 영역")
  st.caption("아래 단어 중 다음에 올 알맞은 단어를 선택하세요.")

  # 남은 단어들 표시
  remaining_words = [
      w
      for w in st.session_state.shuffled_words
      if st.session_state.shuffled_words.count(w)
      > st.session_state.placed_words.count(w)
  ]

  # 한 줄에 4개씩 버튼 배치
  cols = st.columns(4)
  for i, word in enumerate(st.session_state.shuffled_words):
    # 이미 올바르게 배치된 단어 개수 파악
    already_used = st.session_state.placed_words.count(word)
    # 현재 화면에 남아있는 동일 단어 체크 간단 구현을 위해 인덱스 기반으로 관리
    col_idx = i % 4
    with cols[col_idx]:
      # 이미 사용된 단어인지 확인 (중복 단어 대응)
      # 간단하게 현재 사용된 횟수보다 적게 선택되었을 때만 활성화
      used_count = st.session_state.placed_words.count(word)
      total_count_in_problem = st.session_state.correct_list.count(word)

      # 버튼 클릭 이벤트
      if st.button(word, key=f"word_{i}"):
        next_idx = len(st.session_state.placed_words)
        expected_word = st.session_state.correct_list[next_idx]

        if word == expected_word:
          # 정답일 때
          st.session_state.placed_words.append(word)
          st.session_state.feedback = "correct_step"

          # 문장을 전부 맞췄을 때
          if len(st.session_state.placed_words) == len(
              st.session_state.correct_list
          ):
            st.session_state.score += 10
            st.success("🎉 문장을 완벽하게 완성했습니다!")
            if st.session_state.current_q < 9:
              st.session_state.current_q += 1
              st.balloons()
              # 다음 문제로 넘어가기 위한 버튼 유도
            else:
              st.session_state.game_over = True
          st.rerun()
        else:
          # 틀렸을 때
          st.session_state.feedback = "wrong"
          st.rerun()

  st.write("")
  if st.button("🔄 현재 문제 초기화"):
    load_question(st.session_state.current_q)
    st.rerun()

else:
  # 게임 종료 화면
  st.balloons()
  st.title("🏆 게임 클리어!")
  st.success(
      f"축하합니다! 총 10문제를 모두 풀었습니다.\n\n 최종 점수: 총"
      f" {st.session_state.score} 점"
  )

  if st.button("🎮 게임 다시 시작하기"):
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    load_question(0)
    st.rerun()
