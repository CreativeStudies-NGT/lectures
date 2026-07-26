import time
from dataclasses import dataclass
from typing import Optional

import streamlit as st

st.set_page_config(page_title='プレゼンタイマー', page_icon='⏱️', layout='centered')

PHASE_LABELS = {'presentation': '🎤 発表時間', 'qa': '💬 質疑応答時間'}


@dataclass
class TimerState:
    phase: str = 'idle'
    running: bool = False
    phase_elapsed: float = 0.0
    phase_start: Optional[float] = None
    pres_min: int = 5
    pres_sec: int = 0
    qa_min: int = 3
    qa_sec: int = 0
    show_seconds: bool = False
    warning_min: int = 2


@st.cache_resource
def get_state():
    return TimerState()


state = get_state()

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap');

h1 {
    font-family: 'Nunito', sans-serif;
    font-size: 1.6rem !important;
    text-align: center;
    margin-bottom: 1.5rem !important;
}

.phase-label {
    text-align: center;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
}

[data-testid="stSidebar"] {
    width: 220px !important;
}

.timer {
    text-align: center;
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 14rem;
    line-height: 1.1;
    margin-bottom: 1.5rem;
}
</style>
''', unsafe_allow_html=True)

st.markdown('<h1>⏱️ DXスタディーズ発表会 プレゼンタイマー</h1>', unsafe_allow_html=True)


def get_elapsed():
    if state.running and state.phase_start is not None:
        return state.phase_elapsed + (time.time() - state.phase_start)
    return state.phase_elapsed


def start_phase(phase):
    state.phase = phase
    state.phase_elapsed = 0.0
    state.phase_start = time.time()
    state.running = True


def pause():
    state.phase_elapsed = get_elapsed()
    state.running = False
    state.phase_start = None


def resume():
    state.phase_start = time.time()
    state.running = True


def reset():
    state.phase = 'idle'
    state.running = False
    state.phase_elapsed = 0.0
    state.phase_start = None


locked = state.phase != 'idle'

st.sidebar.header('⏱️ 時間設定')

with st.sidebar.expander('⚙️ settings'):
    state.show_seconds = st.checkbox('秒の設定を表示', value=state.show_seconds, disabled=locked)
    state.warning_min = st.number_input(
        '残り何分で色が変わるか', min_value=0, max_value=30, value=state.warning_min, disabled=locked
    )

st.sidebar.subheader('発表時間')
state.pres_min = st.sidebar.number_input('分', min_value=0, max_value=60, value=state.pres_min, disabled=locked)
if state.show_seconds:
    state.pres_sec = st.sidebar.number_input('秒', min_value=0, max_value=59, value=state.pres_sec, disabled=locked)
else:
    state.pres_sec = 0

st.sidebar.subheader('質疑応答時間')
state.qa_min = st.sidebar.number_input('分', min_value=0, max_value=60, value=state.qa_min, disabled=locked)
if state.show_seconds:
    state.qa_sec = st.sidebar.number_input('秒', min_value=0, max_value=59, value=state.qa_sec, disabled=locked)
else:
    state.qa_sec = 0

DURATIONS = {
    'presentation': state.pres_min * 60 + state.pres_sec,
    'qa': state.qa_min * 60 + state.qa_sec,
}
WARNING_SECONDS = state.warning_min * 60

if state.phase == 'idle':
    st.info('時間を設定して「発表スタート」を押してください')
    if st.button('▶️ 発表スタート', type='primary', use_container_width=True):
        start_phase('presentation')
        st.rerun()

elif state.phase == 'done':
    st.success('お疲れ様でした！')
    if st.button('🔄 最初から', use_container_width=True):
        reset()
        st.rerun()

else:
    duration = DURATIONS[state.phase]
    remaining = duration - get_elapsed()

    mins, secs = divmod(int(abs(remaining)), 60)
    time_str = f'{mins:02d}:{secs:02d}'

    if remaining < 0:
        color = '#FF4B4B'
    elif remaining <= WARNING_SECONDS:
        color = '#FFA500'
    else:
        color = '#4D96FF'

    st.markdown(f'<p class="phase-label">{PHASE_LABELS[state.phase]}</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="timer" style="color:{color};">{time_str}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if state.running:
            if st.button('⏸️ 一時停止', use_container_width=True):
                pause()
                st.rerun()
        else:
            if st.button('▶️ 再開', use_container_width=True):
                resume()
                st.rerun()

    with col2:
        if state.phase == 'presentation':
            if st.button('⏭️ 質疑応答へ', use_container_width=True):
                start_phase('qa')
                st.rerun()
        else:
            if st.button('🏁 終了', use_container_width=True):
                state.phase = 'done'
                state.running = False
                st.rerun()

    with col3:
        if st.button('🔄 リセット', use_container_width=True):
            reset()
            st.rerun()

if state.running:
    time.sleep(1)
    st.rerun()
