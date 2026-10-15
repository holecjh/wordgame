import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="대한민국 헌법 문장 만들기 게임",
    page_icon="🇰🇷",
    layout="centered",
)

# 역동적인 게임 스타일을 위한 커스텀 CSS (애니메이션, 통통 튀는 버튼, 카드 효과)
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .correct-box {
        background-color: #d4edda;
        color: #155724;
        padding: 12px;
        border-radius: 12px;
        border: 2px solid #28a745;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        animation: popUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
    }
    .wrong-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 12px;
        border-radius: 12px;
        border: 2px solid #dc3545;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        animation: shake 0.4s ease-in-out;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.2);
    }
    @keyframes popUp {
        0% { transform: scale(0.6); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-8px); }
        40%, 80% { transform: translateX(8px); }
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1rem;
        padding: 10px;
        background-color: #ffffff;
        border: 2px solid #4a90e2;
        color: #333333;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        background-color: #4a90e2;
        color: white;
        box-shadow: 0 6px 12px rgba(74, 144, 226, 0.3);
    }
    .game-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        margin-bottom: 20px;
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
  st.session_state.feedback = None
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
st.markdown(
    "<h1 style='text-align: center; color: #2c3e50;'>🇰🇷 헌법 완성 대작전!</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #555;'>단어를 올바른 순서대로 조립하여"
    " 대한민국 헌법을 완성하세요.</p>",
    unsafe_allow_html=True,
)
st.divider()

if not st.session_state.game_over:
  current_prob = PROBLEMS[st.session_state.current_q]

  # 상단 정보 카드
  st.markdown('<div class="game-card">', unsafe_allow_html=True)
  col1, col2 = st.columns([2, 1])
  with col1:
    st.markdown(f"### 🎯 문제 {st.session_state.current_q + 1} / 10")
    st.markdown(
        f"**난이도:** `{current_prob['level']}` &nbsp;|&nbsp; **조문:**"
        f" **{current_prob['title']}**"
    )
  with col2:
    st.metric(
        label="⭐ 획득 점수", value=f"{st.session_state.score} 점", delta="+10점/문항"
    )
  st.markdown("</div>", unsafe_allow_html=True)

  # 1. 완성된 문장 칸 (슬롯)
  st.markdown("#### 🧩 문장 맞추기 칸")
  correct_list = st.session_state.correct_list
  placed = st.session_state.placed_words

  slot_cols = st.columns(len(correct_list))
  for i, col in enumerate(slot_cols):
    with col:
      if i < len(placed):
        st.markdown(
            f'<div class="correct-box">{placed[i]}</div>', unsafe_allow_html=True
        )
      else:
        st.markdown(
            '<div style="background-color: #e9ecef; color: #adb5bd; padding:'
            ' 12px; border-radius: 12px; text-align: center; border: 2px dashed'
            ' #ced4da; font-weight: bold;">빈칸</div>',
            unsafe_allow_html=True,
        )

  st.write("")

  # 피드백 메시지 표시
  if st.session_state.feedback == "wrong":
    st.markdown(
        '<div class="wrong-box">❌ 아까워요! 순서가 틀렸습니다. 다시'
        " 도전해보세요!</div>",
        unsafe_allow_html=True,
    )
  elif st.session_state.feedback == "correct_step":
    st.markdown(
        '<div class="correct-box">✨ 딩동댕! 올바른 단어입니다. 계속해서'
        " 이어가세요!</div>",
        unsafe_allow_html=True,
    )

  st.divider()

  # 2. 선택 가능한 단어들 (버튼 형태)
  st.markdown("#### 🔀 아래 단어를 클릭하여 빈칸을 채우세요")

  # 남은 단어들을 필터링하여 버튼으로 배치
  cols = st.columns(4)
  for i, word in enumerate(st.session_state.shuffled_words):
    col_idx = i % 4
    with cols[col_idx]:
      # 이미 배치된 단어인지 확인하여 사용 완료된 단어는 비활성화 효과 혹은 처리
      # 여기서는 심플하게 버튼 클릭 시 정오답 판정
      if st.button(word, key=f"word_btn_{i}_{random.random()}"):
        next_idx = len(st.session_state.placed_words)
        expected_word = st.session_state.correct_list[next_idx]

        if word == expected_word:
          # 정답일 때
          st.session_state.placed_words.append(word)

          # 문장을 전부 완성했을 때 (자동 다음 문제 전환 + 빵빠레)
          if len(st.session_state.placed_words) == len(
              st.session_state.correct_list
          ):
            st.session_state.score += 10
            st.balloons()  # 🎊 빵빠레 터트리기!

            if st.session_state.current_q < len(PROBLEMS) - 1:
              st.session_state.current_q += 1
              load_question(st.session_state.current_q)
            else:
              st.session_state.game_over = True
          else:
            st.session_state.feedback = "correct_step"
          st.rerun()
        else:
          # 틀렸을 때
          st.session_state.feedback = "wrong"
          st.rerun()

  st.write("")
  if st.button("🔄 현재 문제 다시 시작하기"):
    load_question(st.session_state.current_q)
    st.rerun()

else:
  # 게임 최종 클리어 화면
  st.balloons()
  st.markdown(
      """
    <div style="text-align: center; padding: 40px; background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <h1>🏆 축하합니다! 모든 게임을 클리어하셨습니다!</h1>
        <p style="font-size: 1.2rem; color: #555;">대한민국 헌법의 수호자가 되셨습니다.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )
  st.success(f"최종 점수: 총 {st.session_state.score} 점 / 100점 만점")

  if st.button("🎮 처음부터 다시 도전하기"):
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    load_question(0)
    st.rerun()
