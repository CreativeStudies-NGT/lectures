import streamlit as st
import random
import time
from datetime import date

GROUPS = [
    'ふらっとGO～行先に迷うあなたへ～　「GeoWalk」',
    '土地を呑むということ　「株式会社 創生酒造」',
    'ARを利用した3D図書探索ツールの開発 〜「探す」から「見つかる」へ〜　「チームブックピカル」',
    '現実とリンクするVR創生学部棟を作ってみた 「前線組」',
    'Raspberry Pi を使ったリアルタイム指文字・音声認識システムの開発　「チームしゅわっち」',
    '次世代インターフォン開発　「こぐまさん」'
]

MEDALS = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣']
COLORS = ['#FF6B6B', '#FFA500', '#FFD700', '#6BCB77', '#4D96FF', '#C77DFF']

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap');

h1 {
    font-family: 'Nunito', sans-serif;
    font-size: 2.8rem !important;
    text-align: center;
    background: linear-gradient(135deg, #FF6B6B, #FFA500, #FFD700, #6BCB77, #4D96FF, #C77DFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem !important;
}

.subtitle {
    text-align: center;
    color: #aaaacc;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.card {
    border-radius: 16px;
    padding: 18px 24px;
    margin: 10px 0;
    display: flex;
    align-items: center;
    gap: 16px;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: #ffffff;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    animation: slidein 0.5s ease forwards;
}

@keyframes slidein {
    from { opacity: 0; transform: translateX(-30px); }
    to   { opacity: 1; transform: translateX(0); }
}

.medal { font-size: 2rem; }
.rank  { font-size: 0.85rem; opacity: 0.8; }
.name  { flex: 1; word-break: break-all; }
</style>
''', unsafe_allow_html=True)

st.markdown('<h1>🎉 発表順番決め 🎉</h1>', unsafe_allow_html=True)
today = date.today()
st.markdown('<p class="subtitle">DX共創コース・DXスタディーズ</p>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">{today.year}年{today.month}月{today.day}日</p>', unsafe_allow_html=True)


def card_html(rank_index, name):
    color = COLORS[rank_index]
    medal = MEDALS[rank_index]
    return f'''
    <div class="card" style="background: linear-gradient(135deg, {color}cc, {color}66); border-left: 6px solid {color};">
        <span class="medal">{medal}</span>
        <div>
            <div class="rank">{rank_index + 1}番目</div>
            <div class="name">{name}</div>
        </div>
    </div>
    '''


col1, col2 = st.columns(2)

with col1:
    if st.button('🎲 シャッフル！', use_container_width=True, type='primary'):
        st.session_state['order'] = random.sample(GROUPS, len(GROUPS))
        st.session_state.pop('revealed', None)

with col2:
    reveal_disabled = 'order' not in st.session_state
    if st.button('🎤 発表スタート！', use_container_width=True, disabled=reveal_disabled):
        st.session_state['revealed'] = True

if 'order' in st.session_state and 'revealed' in st.session_state:
    order = st.session_state['order']
    placeholder = st.empty()
    shown = []

    for idx in range(len(order) - 1, -1, -1):
        shown.insert(0, idx)
        html = ''.join(card_html(i, order[i]) for i in shown)
        placeholder.markdown(html, unsafe_allow_html=True)
        if idx > 0:
            time.sleep(1.5)

    st.balloons()

elif 'order' in st.session_state:
    st.info('「発表スタート！」ボタンを押してください')
