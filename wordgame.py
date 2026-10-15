import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="대한민국 헌법 문장 만들기 게임",
    page_icon="🇰🇷",
    layout="centered",
)

# 커스텀 CSS 스타일링
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .word-slot {
        background-color: #ffffff;
        color: #212529;
        padding: 10px 14px;
        border-radius: 10px;
        border: 2px solid #4a90e2;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        cursor: pointer;
        margin-bottom: 5px;
    }
    .empty-slot {
        background-color: #f1f3f5;
        color: #adb5bd;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        border: 2px dashed #ced4da;
        font-weight: bold;
    }
    .game-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #28a745;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 15px;
        animation: popUp 0.3s ease-in-out;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #dc3545;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 15px;
        animation: shake 0.3s ease-in-out;
    }
    .hint-banner {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 40px 20px;
        border-radius: 20px;
        text-align: center;
        border: 4px solid #ff7675;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin: 20px 0;
        animation: popUp 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes popUp {
        0% { transform: scale(0.7); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-6px); }
        75% { transform: translateX(6px); }
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 10문제 데이터 정의
PROBLEMS = [
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
    {
        "level": "난이도 4 (10단어)",
        "title": "헌법 제10조",
        "text": "모든 / 국민은 / 인간으로서의 / 존엄과 / 가치를 / 가지며 / 행복을 / 추구할 / 권리를 / 가진다",
    },
]

# 세션 상태 초기화
if "current_q" not in st.session_state:
  st.session_state.current_q = 0
if "placed_items" not in st.session_state:
  st.session_state.placed_items = []
if "shuffled_words" not in st.session_state:
  st.session_state.shuffled_words = []
if "correct_list" not in st.session_state:
  st.session_state.correct_list = []
if "checked" not in st.session_state:
  st.session_state.checked = False
if "is_correct" not in st.session_state:
  st.session_state.is_correct = False
if "score" not in st.session_state:
  st.session_state.score = 0
if "game_over" not in st.session_state:
  st.session_state.game_over = False


def init_question(idx):
  prob = PROBLEMS[idx]
  correct_list = [w.strip() for w in prob["text"].split("/")]
  shuffled = correct_list.copy()
  random.shuffle(shuffled)
  st.session_state.correct_list = correct_list
  st.session_state.shuffled_words = shuffled
  st.session_state.placed_items = []
  st.session_state.checked = False
  st.session_state.is_correct = False


if not st.session_state.shuffled_words and not st.session_state.game_over:
  init_question(0)

# 타이틀
st.markdown(
    "<h1 style='text-align: center; color: #2c3e50;'>🇰🇷 헌법 완성 대작전</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #555;'>단어를 순서대로 배치한 뒤"
    " 정답을 확인하세요.</p>",
    unsafe_allow_html=True,
)
st.divider()

if not st.session_state.game_over:
  current_prob = PROBLEMS[st.session_state.current_q]

  # 상단 진행 상태
  st.markdown('<div class="game-card">', unsafe_allow_html=True)
  col1, col2 = st.columns([2, 1])
  with col1:
    st.markdown(f"### 🎯 문제 {st.session_state.current_q + 1} / 10")
    st.markdown(
        f"**난이도:** `{current_prob['level']}` &nbsp;|&nbsp; 조문:"
        f" **{current_prob['title']}**"
    )
  with col2:
    st.metric(
        label="진행도",
        value=f"{st.session_state.current_q + 1} / 10",
        delta="문항",
    )
  st.markdown("</div>", unsafe_allow_html=True)

  correct_list = st.session_state.correct_list
  placed_items = st.session_state.placed_items

  # 1. 완성된 문장 칸 (슬롯)
  st.markdown("#### 🧩 완성된 문장 칸 (클릭하면 단어가 빠집니다)")
  slot_cols = st.columns(len(correct_list))

  for i, col in enumerate(slot_cols):
    with col:
      if i < len(placed_items):
        word, pool_idx = placed_items[i]
        is_locked = st.session_state.checked and st.session_state.is_correct
        if st.button(
            f"❌ {word}" if not is_locked else word,
            key=f"placed_{i}_{pool_idx}",
            disabled=is_locked,
        ):
          if not st.session_state.checked:
            st.session_state.placed_items.pop(i)
            st.rerun()
      else:
        st.markdown(
            '<div class="empty-slot">빈칸</div>', unsafe_allow_html=True
        )

  st.write("")

  # 정답 확인 후 피드백 메시지 출력
  if st.session_state.checked:
    if st.session_state.is_correct:
      st.markdown(
          '<div class="success-box">✅ 정답입니다! 멋지게 문장을 완성하셨습니다!</div>',
          unsafe_allow_html=True,
      )
    else:
      st.markdown(
          '<div class="error-box">❌ 아쉽네요! 틀린 부분이 있습니다. 단어를'
          " 수정하거나 초기화 후 다시 도전해보세요.</div>",
          unsafe_allow_html=True
