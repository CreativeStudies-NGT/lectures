import time

import streamlit as st

st.set_page_config(page_title='プレゼンタイマー', page_icon='⏱️', layout='centered')

PHASE_LABELS = {'presentation': '🎤 発表時間', 'qa': '💬 質疑応答時間'}

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap');

h1 {
    font-family: 'Nunito', sans-serif;
    font-size: 2.4rem !important;
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

st.markdown('<h1>⏱️ プレゼンタイマー</h1>', unsafe_allow_html=True)

if 'phase' not in st.session_state:
    st.session_state.phase = 'idle'
if 'running' not in st.session_state:
    st.session_state.running = False
if 'phase_elapsed' not in st.session_state:
    st.session_state.phase_elapsed = 0.0
if 'phase_start' not in st.session_state:
    st.session_state.phase_start = None


def get_elapsed():
    if st.session_state.running and st.session_state.phase_start is not None:
        return st.session_state.phase_elapsed + (time.time() - st.session_state.phase_start)
    return st.session_state.phase_elapsed


def start_phase(phase):
    st.session_state.phase = phase
    st.session_state.phase_elapsed = 0.0
    st.session_state.phase_start = time.time()
    st.session_state.running = True


def pause():
    st.session_state.phase_elapsed = get_elapsed()
    st.session_state.running = False
    st.session_state.phase_start = None


def resume():
    st.session_state.phase_start = time.time()
    st.session_state.running = True


def reset():
    st.session_state.phase = 'idle'
    st.session_state.running = False
    st.session_state.phase_elapsed = 0.0
    st.session_state.phase_start = None


locked = st.session_state.phase != 'idle'

st.sidebar.header('⏱️ 時間設定')

st.sidebar.subheader('発表時間')
pcol1, pcol2 = st.sidebar.columns(2)
pres_min = pcol1.number_input('分', min_value=0, max_value=60, value=5, key='pres_min', disabled=locked)
pres_sec = pcol2.number_input('秒', min_value=0, max_value=59, value=0, key='pres_sec', disabled=locked)

st.sidebar.subheader('質疑応答時間')
qcol1, qcol2 = st.sidebar.columns(2)
qa_min = qcol1.number_input('分', min_value=0, max_value=60, value=3, key='qa_min', disabled=locked)
qa_sec = qcol2.number_input('秒', min_value=0, max_value=59, value=0, key='qa_sec', disabled=locked)

DURATIONS = {
    'presentation': pres_min * 60 + pres_sec,
    'qa': qa_min * 60 + qa_sec,
}

if st.session_state.phase == 'idle':
    st.info('時間を設定して「発表スタート」を押してください')
    if st.button('▶️ 発表スタート', type='primary', use_container_width=True):
        start_phase('presentation')
        st.rerun()

elif st.session_state.phase == 'done':
    st.success('お疲れ様でした！')
    if st.button('🔄 最初から', use_container_width=True):
        reset()
        st.rerun()

else:
    duration = DURATIONS[st.session_state.phase]
    remaining = duration - get_elapsed()

    mins, secs = divmod(int(abs(remaining)), 60)
    sign = '+' if remaining < 0 else ''
    time_str = f'{sign}{mins:02d}:{secs:02d}'

    if remaining < 0:
        color = '#FF4B4B'
    elif duration > 0 and remaining <= duration * 0.2:
        color = '#FFA500'
    else:
        color = '#4D96FF'

    st.markdown(f'<p class="phase-label">{PHASE_LABELS[st.session_state.phase]}</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="timer" style="color:{color};">{time_str}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.session_state.running:
            if st.button('⏸️ 一時停止', use_container_width=True):
                pause()
                st.rerun()
        else:
            if st.button('▶️ 再開', use_container_width=True):
                resume()
                st.rerun()

    with col2:
        if st.session_state.phase == 'presentation':
            if st.button('⏭️ 質疑応答へ', use_container_width=True):
                start_phase('qa')
                st.rerun()
        else:
            if st.button('🏁 終了', use_container_width=True):
                st.session_state.phase = 'done'
                st.session_state.running = False
                st.rerun()

    with col3:
        if st.button('🔄 リセット', use_container_width=True):
            reset()
            st.rerun()

if st.session_state.running:
    time.sleep(1)
    st.rerun()
