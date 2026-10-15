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
    .word-slot:hover {
        background-color: #ffe3e3;
        border-color: #fa5252;
        color: #c92a2a;
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
    .result-card-correct {
        background-color: #d4edda;
        border-left: 6px solid #28a745;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .result-card-wrong {
        background-color: #f8d7da;
        border-left: 6px solid #dc3545;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
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
  st.session_state.placed_items = (
      []
  )  # 형식: 리스트 내의 (word, original_pool_index) 튜플
if "shuffled_words" not in st.session_state:
  st.session_state.shuffled_words = []
if "correct_list" not in st.session_state:
  st.session_state.correct_list = []
if "results_history" not in st.session_state:
  st.session_state.results_history = []
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


# 게임 시작 시 초기화
if not st.session_state.shuffled_words and not st.session_state.game_over:
  init_question(0)

# 타이틀
st.markdown(
    "<h1 style='text-align: center; color: #2c3e50;'>🇰🇷 헌법 완성 대작전</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #555;'>단어를 순서대로 배치하여 문장을"
    " 완성하세요. (배치된 단어를 누르면 다시 제외됩니다)</p>",
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
  placed_items = st.session_state.placed_items  # [(word, pool_idx), ...]

  # 1. 완성된 문장 칸 (슬롯) - 클릭 시 해당 단어 제거 기능 포함
  st.markdown("#### 🧩 완성된 문장 칸 (클릭하면 단어가 빠집니다)")
  slot_cols = st.columns(len(correct_list))

  for i, col in enumerate(slot_cols):
    with col:
      if i < len(placed_items):
        word, pool_idx = placed_items[i]
        # 단어를 클릭하면 해당 단어를 빼는 버튼 구현
        if st.button(f"❌ {word}", key=f"placed_{i}_{pool_idx}"):
          # 해당 아이템 제거
          st.session_state.placed_items.pop(i)
          st.rerun()
      else:
        st.markdown(
            '<div class="empty-slot">빈칸</div>', unsafe_allow_html=True
        )

  st.write("")
  st.divider()

  # 2. 선택 가능한 단어 풀 영역
  st.markdown("#### 🔀 단어 선택 영역")
  st.caption("아래 단어를 클릭하면 빈칸에 차례대로 채워집니다.")

  used_pool_indices = [item[1] for item in placed_items]

  # 4열 버튼 배치
  cols = st.columns(4)
  for idx, word in enumerate(st.session_state.shuffled_words):
    col_idx = idx % 4
    with cols[col_idx]:
      is_used = idx in used_pool_indices
      if not is_used:
        if st.button(word, key=f"pool_{idx}"):
          if len(st.session_state.placed_items) < len(correct_list):
            st.session_state.placed_items.append((word, idx))
            st.rerun()
      else:
        # 이미 사용된 단어는 비활성화처럼 표시
        st.button(
            f"✓ {word}", key=f"pool_used_{idx}", disabled=True, use_container_width=True
        )

  st.write("")
  st.divider()

  # 하단 제어 버튼
  col_a, col_b = st.columns(2)
  with col_a:
    if st.button("🔄 전체 비우기", use_container_width=True):
      st.session_state.placed_items = []
      st.rerun()

  with col_b:
    # 모든 빈칸이 채워졌을 때만 제출 버튼 활성화
    if len(placed_items) == len(correct_list):
      if st.button("📥 이 문장으로 제출하기 ➔", type="primary", use_container_width=True):
        user_sent = [item[0] for item in placed_items]
        is_correct = user_sent == correct_list

        # 결과 기록 저장
        st.session_state.results_history.append({
            "q_num": st.session_state.current_q + 1,
            "title": current_prob["title"],
            "level": current_prob["level"],
            "correct_list": correct_list,
            "user_list": user_sent,
            "is_correct": is_correct,
        })

        # 다음 문제로 넘어가거나 게임 종료
        if st.session_state.current_q < len(PROBLEMS) - 1:
          st.session_state.current_q += 1
          init_question(st.session_state.current_q)
        else:
          st.session_state.game_over = True
          st.balloons()
        st.rerun()
    else:
      st.button(
          "📥 모든 빈칸을 채워주세요", disabled=True, use_container_width=True
      )

else:
  # ----------------------------------------------------
  # 4번 요구사항: 10문제 종료 후 정답 및 오답노트 일괄 공개
  # ----------------------------------------------------
  st.balloons()
  st.markdown(
      """
    <div style="text-align: center; padding: 30px; background: white; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); margin-bottom: 30px;">
        <h2>🎉 10문제 도전을 모두 완료하셨습니다!</h2>
        <p style="color: #666; font-size: 1.1rem;">아래에서 나의 정답 여부와 오답 노트를 꼼꼼히 확인해 보세요.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # 총 점수 계산
  correct_count = sum(
      1 for r in st.session_state.results_history if r["is_correct"]
  )
  total_score = correct_count * 10

  st.metric(label="🏆 최종 성적", value=f"{total_score} 점 / 100점 만점", delta=f"정답 수: {correct_count}/10")
  st.divider()

  st.subheader("📝 전체 문제 오답 노트 및 결과")

  for res in st.session_state.results_history:
    card_class = (
        "result-card-correct" if res["is_correct"] else "result-card-wrong"
    )
    status_icon = "✅ 정답" if res["is_correct"] else "❌ 오답"

    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    st.markdown(
        f"#### 문제 {res['q_num']} ({res['level']} - {res['title']}) &nbsp;&nbsp;"
        f" **{status_icon}**"
    )

    correct_str = " / ".join(res["correct_list"])
    user_str = " / ".join(res["user_list"])

    st.markdown(f"- **올바른 정답:** `{correct_str}`")
    st.markdown(f"- **내가 제출한 답:** `{user_str}`")

    if not res["is_correct"]:
      st.markdown(
          "<span style='color: #dc3545; font-weight: bold;'>💡 피드백:</span>"
          " 단어의 순서가 잘못 배치되었습니다. 올바른 순서를 다시 한번 눈여겨"
          " 익혀보세요!",
          unsafe_allow_html=True,
      )

    st.markdown("</div>", unsafe_allow_html=True)

  st.write("")
  if st.button("🎮 게임 다시 시작하기", type="primary", use_container_width=True):
    st.session_state.current_q = 0
    st.session_state.results_history = []
    st.session_state.game_over = False
    init_question(0)
    st.rerun()
