import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="대한민국 헌법 문장 만들기 게임",
    page_icon="🇰🇷",
    layout="centered",
)

# 커스텀 CSS 스타일링 (책 느낌 디자인 + 공중에서 떨어지는 애니메이션)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #fdfbf7 0%, #e6e2d6 100%);
        font-family: 'Gowun Batang', serif;
    }

    /* 책 프레임 카드 */
    .book-frame {
        background: #fffdfa;
        padding: 30px;
        border-radius: 16px;
        border: 3px solid #d4cbb3;
        box-shadow: 0 12px 35px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* 단어가 공중에서 문장으로 뚝 떨어지는 비행 애니메이션 */
    @keyframes flyDrop {
        0% {
            transform: translateY(-35px) scale(0.6);
            opacity: 0;
        }
        70% {
            transform: translateY(6px) scale(1.05);
            opacity: 1;
        }
        100% {
            transform: translateY(0) scale(1);
            opacity: 1;
        }
    }

    .flying-effect {
        animation: flyDrop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        display: inline-block;
    }

    /* 실제 책 본문처럼 단어가 유연하게 이어지는 문장 슬롯 영역 */
    .sentence-box {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
        justify-content: flex-start;
        background: #f7f5ef;
        padding: 22px;
        border-radius: 12px;
        border: 1.5px solid #dcd4c0;
        min-height: 110px;
        margin-bottom: 15px;
    }

    .filled-word-card {
        background-color: #ffffff;
        color: #2c2c2c;
        padding: 10px 16px;
        border-radius: 8px;
        border: 2px solid #8c7b65;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.06);
        word-break: keep-all;
    }

    .empty-slot-card {
        background-color: #eae6dc;
        color: #9c9384;
        padding: 10px 16px;
        border-radius: 8px;
        border: 2px dashed #b5ab9a;
        font-size: 1rem;
        font-weight: 400;
    }

    .success-box {
        background-color: #eafaf1;
        color: #1e8449;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #27ae60;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        animation: flyDrop 0.3s ease-in-out;
        margin-bottom: 15px;
    }

    .error-box {
        background-color: #fdedec;
        color: #c0392b;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #e74c3c;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        animation: flyDrop 0.3s ease-in-out;
        margin-bottom: 15px;
    }

    .hint-banner {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 40px 20px;
        border-radius: 20px;
        text-align: center;
        border: 4px solid #f39c12;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin: 20px 0;
        animation: flyDrop 0.5s ease-in-out;
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
        "text": (
            "국가는 / 재해를 / 예방하고 / 그 위험으로부터 / 국민을 / 보호하기 위하여"
            " / 노력하여야 / 한다."
        ),
    },
    {
        "level": "난이도 2 (8단어)",
        "title": "헌법 제37조",
        "text": (
            "국민의 / 자유와 / 권리는 / 헌법에 / 열거되지 / 아니한 이유로 / 경시되지"
            " / 아니한다."
        ),
    },
    {
        "level": "난이도 3 (9단어)",
        "title": "헌법 제2조",
        "text": (
            "국가는 / 법률이 / 정하는 / 바에 / 의하여 / 재외국민을 / 보호할 / 의무를"
            " / 진다"
        ),
    },
    {
        "level": "난이도 3 (9단어)",
        "title": "헌법 제12조",
        "text": (
            "모든 / 국민은 / 고문을 / 받지 아니하며 / 형사상 / 자기에게 / 불리한 /"
            " 진술을 / 강요당하지 아니한다"
        ),
    },
    {
        "level": "난이도 3 (9단어)",
        "title": "헌법 제21조",
        "text": (
            "모든 / 국민은 / 언론 / 출판의 / 자유와 / 집회 / 결사의 / 자유를 /"
            " 가진다."
        ),
    },
    {
        "level": "난이도 4 (10단어)",
        "title": "헌법 제10조",
        "text": (
            "모든 / 국민은 / 인간으로서의 / 존엄과 / 가치를 / 가지며 / 행복을 /"
            " 추구할 / 권리를 / 가진다"
        ),
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
    "<h1 style='text-align: center; color: #2c3e50;'>🇰🇷 대한민국 헌법 문장"
    " 완성하기</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #666;'>단어를 순서대로 배치하여 실제"
    " 헌법 조문을 책처럼 완성해 보세요.</p>",
    unsafe_allow_html=True,
)
st.divider()

if not st.session_state.game_over:
  current_prob = PROBLEMS[st.session_state.current_q]

  # 상단 진행 상태 카드
  st.markdown('<div class="book-frame">', unsafe_allow_html=True)
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

  # 1. 책 본문 형태의 완성된 문장 칸 (긴 단어와 문장 전체가 잘 보이도록 Flexbox 적용)
  st.markdown("#### 📖 완성된 문장 영역")
  slots_html = '<div class="sentence-box">'
  for i in range(len(correct_list)):
    if i < len(placed_items):
      word, _ = placed_items[i]
      slots_html += (
          f'<span class="filled-word-card flying-effect">{word}</span>'
      )
    else:
      slots_html += '<span class="empty-slot-card">빈칸</span>'
  slots_html += "</div>"
  st.markdown(slots_html, unsafe_allow_html=True)

  # 마지막 단어 취소 버튼
  if placed_items and not (st.session_state.checked and st.session_state.is_correct):
    if st.button("↩️ 방금 고른 단어 취소하기"):
      st.session_state.placed_items.pop()
      st.rerun()

  # 정답 확인 후 피드백 메시지 출력
  if st.session_state.checked:
    if st.session_state.is_correct:
      st.markdown(
          '<div class="success-box">✅ 정답입니다! 조문을 완벽하게'
          " 완성하셨습니다!</div>",
          unsafe_allow_html=True,
      )
    else:
      st.markdown(
          '<div class="error-box">❌ 아쉽네요! 순서가 틀린 곳이 있습니다. 단어를'
          " 취소하거나 초기화 후 다시 도전해보세요.</div>",
          unsafe_allow_html=True,
      )

  st.divider()

  # 2. 선택 가능한 단어 풀 영역
  st.markdown("#### 🔀 단어 선택 영역")
  st.caption("아래 단어를 클릭하면 위쪽 문장 빈칸으로 날아와 채워집니다.")

  used_pool_indices = [item[1] for item in placed_items]
  cols = st.columns(4)
  for idx, word in enumerate(st.session_state.shuffled_words):
    col_idx = idx % 4
    with cols[col_idx]:
      is_used = idx in used_pool_indices
      if not is_used:
        if st.button(
            word,
            key=f"pool_{idx}",
            disabled=st.session_state.checked and st.session_state.is_correct,
        ):
          if (
              len(st.session_state.placed_items) < len(correct_list)
              and not st.session_state.checked
          ):
            st.session_state.placed_items.append((word, idx))
            st.rerun()
      else:
        st.button(
            f"✓ {word}",
            key=f"pool_used_{idx}",
            disabled=True,
            use_container_width=True,
        )

  st.write("")
  st.divider()

  # 하단 제어 버튼 그룹
  col_a, col_b, col_c = st.columns(3)

  with col_a:
    if st.button(
        "🔄 초기화",
        use_container_width=True,
        disabled=st.session_state.checked and st.session_state.is_correct,
    ):
      st.session_state.placed_items = []
      st.session_state.checked = False
      st.session_state.is_correct = False
      st.rerun()

  with col_b:
    if len(placed_items) == len(correct_list) and not st.session_state.checked:
      if st.button("🔍 정답 확인하기", type="primary", use_container_width=True):
        user_sent = [item[0] for item in placed_items]
        is_correct = user_sent == correct_list
        st.session_state.checked = True
        st.session_state.is_correct = is_correct
        if is_correct:
          st.session_state.score += 10
        st.rerun()
    else:
      if not st.session_state.checked:
        st.button(
            "🔍 정답 확인하기", disabled=True, use_container_width=True
        )

  with col_c:
    if st.session_state.checked and st.session_state.is_correct:
      next_label = (
          "다음 문제로 ➔"
          if st.session_state.current_q < len(PROBLEMS) - 1
          else "완료하기 ➔"
      )
      if st.button(next_label, type="primary", use_container_width=True):
        if st.session_state.current_q < len(PROBLEMS) - 1:
          st.session_state.current_q += 1
          init_question(st.session_state.current_q)
        else:
          st.session_state.game_over = True
        st.rerun()
    else:
      st.button("다음 문제로 ➔", disabled=True, use_container_width=True)

else:
  # ----------------------------------------------------
  # 10문제 완료 시 대형 힌트 9 팝업 표시 화면
  # ----------------------------------------------------
  st.balloons()
  st.markdown(
      """
    <div style="text-align: center; padding: 30px; background: white; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); margin-bottom: 20px;">
        <h2>🎉 축하합니다! 10문제를 모두 완벽하게 클리어하셨습니다!</h2>
        <p style="color: #666; font-size: 1.1rem;">대한민국 헌법 조문 마스터가 되셨네요.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  # 요청하신 따옴표 없는 대형 힌트 9 배너
  st.markdown(
      """
    <div class="hint-banner">
        <h3 style="color: #c0392b; margin-bottom: 10px; font-size: 1.6rem;">🎁 최종 미션 성공 보상</h3>
        <div style="font-size: 4.5rem; font-weight: 900; color: #2c3e50; margin: 15px 0; letter-spacing: 2px;">
            힌트 9
        </div>
        <p style="color: #555; font-size: 1.2rem; margin-top: 10px; font-weight: bold;">
            정답을 다 풀면 하나씩 주어지는 4자리 비밀 코드 중 하나입니다!
        </p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.write("")
  if st.button("🎮 게임 다시 시작하기", type="primary", use_container_width=True):
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    init_question(0)
    st.rerun()
