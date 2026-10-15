{\rtf1\ansi\ansicpg949\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import random\
import streamlit as st\
\
# \uc0\u54168 \u51060 \u51648  \u49444 \u51221 \
st.set_page_config(\
    page_title="\uc0\u45824 \u54620 \u48124 \u44397  \u54732 \u48277  \u47928 \u51109  \u47564 \u46308 \u44592  \u44172 \u51076 ",\
    page_icon="\uc0\u55356 \u56816 \u55356 \u56823 ",\
    layout="centered",\
)\
\
# \uc0\u52964 \u49828 \u53568  CSS (\u50528 \u45768 \u47700 \u51060 \u49496  \u48143  \u49353 \u49345  \u54952 \u44284 )\
st.markdown(\
    """\
    <style>\
    .correct-box \{\
        background-color: #d4edda;\
        color: #155724;\
        padding: 10px;\
        border-radius: 8px;\
        border: 2px solid #c3e6cb;\
        text-align: center;\
        font-weight: bold;\
        animation: popUp 0.3s ease-in-out;\
    \}\
    .wrong-box \{\
        background-color: #f8d7da;\
        color: #721c24;\
        padding: 10px;\
        border-radius: 8px;\
        border: 2px solid #f5c6cb;\
        text-align: center;\
        font-weight: bold;\
        animation: shake 0.4s ease-in-out;\
    \}\
    @keyframes popUp \{\
        0% \{ transform: scale(0.8); opacity: 0; \}\
        100% \{ transform: scale(1); opacity: 1; \}\
    \}\
    @keyframes shake \{\
        0%, 100% \{ transform: translateX(0); \}\
        25% \{ transform: translateX(-6px); \}\
        75% \{ transform: translateX(6px); \}\
    \}\
    .stButton>button \{\
        width: 100%;\
        border-radius: 8px;\
        font-weight: bold;\
        transition: all 0.2s;\
    \}\
    .stButton>button:hover \{\
        transform: scale(1.03);\
    \}\
    </style>\
""",\
    unsafe_allow_html=True,\
)\
\
# 10\uc0\u47928 \u51228  \u45936 \u51060 \u53552  \u51221 \u51032  (\u45212 \u51060 \u46020 \u48324  \u45800 \u50612  \u49688 : 7\u44060  ~ 10\u44060 )\
PROBLEMS = [\
    # \uc0\u45212 \u51060 \u46020  1 (7\u45800 \u50612 )\
    \{\
        "level": "\uc0\u45212 \u51060 \u46020  1 (7\u45800 \u50612 )",\
        "title": "\uc0\u54732 \u48277  \u51228 5\u51312 ",\
        "text": "\uc0\u45824 \u54620 \u48124 \u44397 \u51008  / \u44397 \u51228 \u54217 \u54868 \u51032  / \u50976 \u51648 \u50640  / \u45432 \u47141 \u54616 \u44256  / \u52840 \u47029 \u51201  / \u51204 \u51137 \u51012  / \u48512 \u51064 \u54620 \u45796 .",\
    \},\
    \{\
        "level": "\uc0\u45212 \u51060 \u46020  1 (7\u45800 \u50612 )",\
        "title": "\uc0\u54732 \u48277  \u51228 17\u51312 ",\
        "text": "\uc0\u47784 \u46304  / \u44397 \u48124 \u51008  / \u49324 \u49373 \u54876 \u51032  / \u48708 \u48128 \u44284  / \u51088 \u50976 \u47484  / \u52840 \u54644 \u48155 \u51648  / \u50500 \u45768 \u54620 \u45796 .",\
    \},\
    \{\
        "level": "\uc0\u45212 \u51060 \u46020  1 (7\u45800 \u50612 )",\
        "title": "\uc0\u54732 \u48277  \u51228 27\u51312 ",\
        "text": "\uc0\u54805 \u49324 \u54588 \u44256 \u51064 \u51008  / \u50976 \u51396 \u51032  / \u54032 \u44208 \u51060  / \u54869 \u51221 \u46112  / \u46412 \u44620 \u51648 \u45716  / \u47924 \u51396 \u47196  / \u52628 \u51221 \u46108 \u45796 .",\
    \},\
    # \uc0\u45212 \u51060 \u46020  2 (8\u45800 \u50612 )\
    \{\
        "level": "\uc0\u45212 \u51060 \u46020  2 (8\u45800 \u50612 )",\
        "title": "\uc0\u54732 \u48277  \u51228 1\u51312 ",\
        "text": "\uc0\u45824 \u54620 \u48124 \u44397 \u51032  / \u51452 \u44428 \u51008  / \u44397 \u48124 \u50640 \u44172  / \u51080 \u44256  / \u47784 \u46304  / \u44428 \u47141 \u51008  / \u44397 \u48124 \u51004 \u47196 \u48512 \u53552  / \u45208 \u50728 \u45796 .",\
    \},\
    \{\
        "level": "\uc0\u45212 \u51060 \u46020  2 (8\u45800 \u50612 )",\
        "title": "\uc0\u54732 \u48277  \u51228 34\u51312 ",\
        "text": "\uc0\u44397 \u44032 \u45716  / \u51116 \u54644 \u47484  / \u50696 \u48169 \u54616 \u44256  / \u44536  \u50948 \u54744 \u51004 \u47196 \u48512 \u53552  / \u44397 \u48124 \u51012  / \u48372 \u54840 \u54616 \u44592  \u50948 \u54616 \u50668  / \u45432 \u47141 \u54616 \u50668 \u50556  / \u54620 \u45796 .",\
    \},\
    \{\
        "level": "\uc0\u45212 \u51060 \u46020  2 (8\u45800 \u50612 )",\
        "title": "\uc0\u54732 \u48277  \u51228 37\u51312 ",\
        "text": "\uc0\u44397 \u48124 \u51032  / \u51088 \u50976 \u50752  / \u44428 \u47532 \u45716  / \u54732 \u48277 \u50640  / \u50676 \u44144 \u46104 \u51648  / \u50500 \u45768 \u54620  \u51060 \u50976 \u47196  / \u44221 \u49884 \u46104 \u51648  / \u50500 \u45768 \u54620 \u45796 .",\
    \},\
    # \uc0\u45212 \u51060 \u46020  3 (9\u45800 \u50612 )\
    \{\
        "level": "\uc0\u45212 \u51060 \u46020  3 (9\u45800 \u50612 )",\
        "title": "\uc0\u54732 \u48277  \u51228 2\u51312 ",\
        "text": "\uc0\u44397 \u44032 \u45716  / \u48277 \u47456 \u51060  / \u51221 \u54616 \u45716  / \u48148 \u50640  / \u51032 \u54616 \u50668  / \u51116 \u50808 \u44397 \u48124 \u51012  / \u48372 \u54840 \u54624  / \u51032 \u47924 \u47484  / \u51652 \u45796 ",\
    \},\
    \{\
        "level": "\uc0\u45212 \u51060 \u46020  3 (9\u45800 \u50612 )",\
        "title": "\uc0\u54732 \u48277  \u51228 12\u51312 ",\
        "text": "\uc0\u47784 \u46304  / \u44397 \u48124 \u51008  / \u44256 \u47928 \u51012  / \u48155 \u51648  \u50500 \u45768 \u54616 \u47728  / \u54805 \u49324 \u49345  / \u51088 \u44592 \u50640 \u44172  / \u48520 \u47532 \u54620  / \u51652 \u49696 \u51012  / \u44053 \u50836 \u45817 \u54616 \u51648  \u50500 \u45768 \u54620 \u45796 ",\
    \},\
    \{\
        "level": "\uc0\u45212 \u51060 \u46020  3 (9\u45800 \u50612 )",\
        "title": "\uc0\u54732 \u48277  \u51228 21\u51312 ",\
        "text": "\uc0\u47784 \u46304  / \u44397 \u48124 \u51008  / \u50616 \u47200  / \u52636 \u54032 \u51032  / \u51088 \u50976 \u50752  / \u51665 \u54924  / \u44208 \u49324 \u51032  / \u51088 \u50976 \u47484  / \u44032 \u51652 \u45796 .",\
    \},\
    # \uc0\u45212 \u51060 \u46020  4 (10\u45800 \u50612 )\
    \{\
        "level": "\uc0\u45212 \u51060 \u46020  4 (10\u45800 \u50612 )",\
        "title": "\uc0\u54732 \u48277  \u51228 10\u51312 ",\
        "text": "\uc0\u47784 \u46304  / \u44397 \u48124 \u51008  / \u51064 \u44036 \u51004 \u47196 \u49436 \u51032  / \u51316 \u50628 \u44284  / \u44032 \u52824 \u47484  / \u44032 \u51648 \u47728  / \u54665 \u48373 \u51012  / \u52628 \u44396 \u54624  / \u44428 \u47532 \u47484  / \u44032 \u51652 \u45796 ",\
    \},\
]\
\
# \uc0\u49464 \u49496  \u49345 \u53468  \u52488 \u44592 \u54868 \
if "current_q" not in st.session_state:\
  st.session_state.current_q = 0\
if "score" not in st.session_state:\
  st.session_state.score = 0\
if "placed_words" not in st.session_state:\
  st.session_state.placed_words = []\
if "shuffled_words" not in st.session_state:\
  st.session_state.shuffled_words = []\
if "feedback" not in st.session_state:\
  st.session_state.feedback = None  # "correct", "wrong"\
if "game_over" not in st.session_state:\
  st.session_state.game_over = False\
\
\
def load_question(idx):\
  prob = PROBLEMS[idx]\
  correct_list = [w.strip() for w in prob["text"].split("/")]\
  shuffled = correct_list.copy()\
  random.shuffle(shuffled)\
  st.session_state.correct_list = correct_list\
  st.session_state.shuffled_words = shuffled\
  st.session_state.placed_words = []\
  st.session_state.feedback = None\
\
\
# \uc0\u44172 \u51076  \u52488 \u44592  \u47196 \u46377 \
if not st.session_state.shuffled_words and not st.session_state.game_over:\
  load_question(st.session_state.current_q)\
\
# \uc0\u53440 \u51060 \u53952 \
st.title("\uc0\u55356 \u56816 \u55356 \u56823  \u45824 \u54620 \u48124 \u44397  \u54732 \u48277  \u47928 \u51109  \u47564 \u46308 \u44592  \u44172 \u51076 ")\
st.markdown("\uc0\u50732 \u48148 \u47480  \u49692 \u49436 \u45824 \u47196  \u45800 \u50612 \u47484  \u53364 \u47533 \u54616 \u50668  \u54732 \u48277  \u51312 \u47928 \u51012  \u50756 \u49457 \u54616 \u49464 \u50836 !")\
st.divider()\
\
if not st.session_state.game_over:\
  current_prob = PROBLEMS[st.session_state.current_q]\
\
  # \uc0\u51652 \u54665  \u49345 \u53468  \u54364 \u49884 \
  col1, col2 = st.columns([2, 1])\
  with col1:\
    st.subheader(f"\uc0\u47928 \u51228  \{st.session_state.current_q + 1\} / 10")\
    st.markdown(f"**[\{current_prob['level']\}] \{current_prob['title']\}**")\
  with col2:\
    st.metric("\uc0\u54788 \u51116  \u51216 \u49688 ", f"\{st.session_state.score\} \u51216 ")\
\
  st.write("")\
\
  # 1. \uc0\u54788 \u51116  \u47582 \u52628 \u44256  \u51080 \u45716  \u50756 \u49457  \u50689 \u50669  (\u54616 \u45800  \u48176 \u52824 )\
  st.markdown("### \uc0\u55358 \u56809  \u50756 \u49457 \u46108  \u47928 \u51109  \u52856 ")\
  correct_list = st.session_state.correct_list\
  placed = st.session_state.placed_words\
\
  # \uc0\u49836 \u47215  \u49884 \u44033 \u54868 \
  slot_cols = st.columns(len(correct_list))\
  for i, col in enumerate(slot_cols):\
    with col:\
      if i < len(placed):\
        st.markdown(\
            f'<div class="correct-box">\{placed[i]\}</div>', unsafe_allow_html=True\
        )\
      else:\
        st.markdown(\
            '<div style="background-color: #f1f3f5; color: #adb5bd; padding:'\
            ' 10px; border-radius: 8px; text-align: center; border: 2px dashed'\
            ' #ced4da;">\uc0\u48712 \u52856 </div>',\
            unsafe_allow_html=True,\
        )\
\
  st.write("")\
  st.divider()\
\
  # \uc0\u54588 \u46300 \u48177  \u47700 \u49884 \u51648  \u54364 \u49884 \
  if st.session_state.feedback == "wrong":\
    st.markdown(\
        '<div class="wrong-box">\uc0\u10060  \u53952 \u47160 \u49845 \u45768 \u45796 ! \u50732 \u48148 \u47480  \u49692 \u49436 \u44032  \u50500 \u45785 \u45768 \u45796 . \u45796 \u49884 '\
        " \uc0\u46020 \u51204 \u54644 \u48372 \u49464 \u50836 !</div>",\
        unsafe_allow_html=True,\
    )\
  elif st.session_state.feedback == "correct_step":\
    st.markdown(\
        '<div class="correct-box">\uc0\u9989  \u47582 \u50520 \u49845 \u45768 \u45796 ! \u45796 \u51020  \u45800 \u50612 \u47484  \u49440 \u53469 \u54616 \u49464 \u50836 .</div>',\
        unsafe_allow_html=True,\
    )\
\
  # 2. \uc0\u49440 \u53469  \u44032 \u45733 \u54620  \u45800 \u50612 \u46308  (\u46028 \u50500 \u45796 \u45768 \u45716  \u45800 \u50612  \u53080 \u49481 \u53944  -> \u48260 \u53948  \u54805 \u53468 \u47196  \u48176 \u52824 )\
  st.markdown("### \uc0\u55357 \u56576  \u45800 \u50612  \u49440 \u53469  \u50689 \u50669 ")\
  st.caption("\uc0\u50500 \u47000  \u45800 \u50612  \u51473  \u45796 \u51020 \u50640  \u50732  \u50508 \u47582 \u51008  \u45800 \u50612 \u47484  \u49440 \u53469 \u54616 \u49464 \u50836 .")\
\
  # \uc0\u45224 \u51008  \u45800 \u50612 \u46308  \u54364 \u49884 \
  remaining_words = [\
      w\
      for w in st.session_state.shuffled_words\
      if st.session_state.shuffled_words.count(w)\
      > st.session_state.placed_words.count(w)\
  ]\
\
  # \uc0\u54620  \u51460 \u50640  4\u44060 \u50473  \u48260 \u53948  \u48176 \u52824 \
  cols = st.columns(4)\
  for i, word in enumerate(st.session_state.shuffled_words):\
    # \uc0\u51060 \u48120  \u50732 \u48148 \u47476 \u44172  \u48176 \u52824 \u46108  \u45800 \u50612  \u44060 \u49688  \u54028 \u50501 \
    already_used = st.session_state.placed_words.count(word)\
    # \uc0\u54788 \u51116  \u54868 \u47732 \u50640  \u45224 \u50500 \u51080 \u45716  \u46041 \u51068  \u45800 \u50612  \u52404 \u53356  \u44036 \u45800  \u44396 \u54788 \u51012  \u50948 \u54644  \u51064 \u45937 \u49828  \u44592 \u48152 \u51004 \u47196  \u44288 \u47532 \
    col_idx = i % 4\
    with cols[col_idx]:\
      # \uc0\u51060 \u48120  \u49324 \u50857 \u46108  \u45800 \u50612 \u51064 \u51648  \u54869 \u51064  (\u51473 \u48373  \u45800 \u50612  \u45824 \u51025 )\
      # \uc0\u44036 \u45800 \u54616 \u44172  \u54788 \u51116  \u49324 \u50857 \u46108  \u54943 \u49688 \u48372 \u45796  \u51201 \u44172  \u49440 \u53469 \u46104 \u50632 \u51012  \u46412 \u47564  \u54876 \u49457 \u54868 \
      used_count = st.session_state.placed_words.count(word)\
      total_count_in_problem = st.session_state.correct_list.count(word)\
\
      # \uc0\u48260 \u53948  \u53364 \u47533  \u51060 \u48292 \u53944 \
      if st.button(word, key=f"word_\{i\}"):\
        next_idx = len(st.session_state.placed_words)\
        expected_word = st.session_state.correct_list[next_idx]\
\
        if word == expected_word:\
          # \uc0\u51221 \u45813 \u51068  \u46412 \
          st.session_state.placed_words.append(word)\
          st.session_state.feedback = "correct_step"\
\
          # \uc0\u47928 \u51109 \u51012  \u51204 \u48512  \u47582 \u52676 \u51012  \u46412 \
          if len(st.session_state.placed_words) == len(\
              st.session_state.correct_list\
          ):\
            st.session_state.score += 10\
            st.success("\uc0\u55356 \u57225  \u47928 \u51109 \u51012  \u50756 \u48317 \u54616 \u44172  \u50756 \u49457 \u54664 \u49845 \u45768 \u45796 !")\
            if st.session_state.current_q < 9:\
              st.session_state.current_q += 1\
              st.balloons()\
              # \uc0\u45796 \u51020  \u47928 \u51228 \u47196  \u45336 \u50612 \u44032 \u44592  \u50948 \u54620  \u48260 \u53948  \u50976 \u46020 \
            else:\
              st.session_state.game_over = True\
          st.rerun()\
        else:\
          # \uc0\u53952 \u47160 \u51012  \u46412 \
          st.session_state.feedback = "wrong"\
          st.rerun()\
\
  st.write("")\
  if st.button("\uc0\u55357 \u56580  \u54788 \u51116  \u47928 \u51228  \u52488 \u44592 \u54868 "):\
    load_question(st.session_state.current_q)\
    st.rerun()\
\
else:\
  # \uc0\u44172 \u51076  \u51333 \u47308  \u54868 \u47732 \
  st.balloons()\
  st.title("\uc0\u55356 \u57286  \u44172 \u51076  \u53364 \u47532 \u50612 !")\
  st.success(\
      f"\uc0\u52629 \u54616 \u54633 \u45768 \u45796 ! \u52509  10\u47928 \u51228 \u47484  \u47784 \u46160  \u54400 \u50632 \u49845 \u45768 \u45796 .\\n\\n \u52572 \u51333  \u51216 \u49688 : \u52509 "\
      f" \{st.session_state.score\} \uc0\u51216 "\
  )\
\
  if st.button("\uc0\u55356 \u57262  \u44172 \u51076  \u45796 \u49884  \u49884 \u51089 \u54616 \u44592 "):\
    st.session_state.current_q = 0\
    st.session_state.score = 0\
    st.session_state.game_over = False\
    load_question(0)\
    st.rerun()}