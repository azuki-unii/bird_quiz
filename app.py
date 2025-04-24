import streamlit as st
import os
import random

# ====== パスワード設定 ======
PASSWORD = "toridaisuki"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("鳥クイズ ログイン")
    pwd = st.text_input("パスワードを入力してください", type="password")
    if pwd == PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    elif pwd:
        st.error("パスワードが違います")
else:
    # ====== 鳥クイズ本体 ======
    AUDIO_FOLDER = "data"

    if "files" not in st.session_state:
        files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".mp3")]
        random.shuffle(files)
        st.session_state.files = files

    if "index" not in st.session_state:
        st.session_state.index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "last_answer_correct" not in st.session_state:
        st.session_state.last_answer_correct = None

    st.title("鳥の鳴き声クイズ")

    if st.session_state.index < len(st.session_state.files):
        current_file = st.session_state.files[st.session_state.index]
        bird_name = os.path.splitext(current_file)[0]

        with open(f"data/{current_file}", "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

        answer = st.text_input("この鳴き声はどの鳥の鳴き声ですか？")

        if not st.session_state.answered:
            if st.button("答え合わせ"):
                st.session_state.answered = True
                if answer.strip().lower() == bird_name.lower():
                    st.session_state.last_answer_correct = True
                    st.session_state.score += 1
                else:
                    st.session_state.last_answer_correct = False
                st.rerun()
        else:
            if st.session_state.last_answer_correct:
                st.success("正解！")
            else:
                st.error(f"不正解！ 正解は {bird_name} でした。")

            if st.button("次の問題へ"):
                st.session_state.index += 1
                st.session_state.answered = False
                st.session_state.last_answer_correct = None
                st.rerun()
    else:
        st.balloons()
        st.success("クイズ終了！")
        st.write(f"正解数：{st.session_state.score} / {len(st.session_state.files)}")
        if st.button("もう一度やる"):
            files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".mp3")]
            random.shuffle(files)
            st.session_state.files = files
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.last_answer_correct = None
            st.rerun()
