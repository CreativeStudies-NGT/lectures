import streamlit as st
import random
import time

GROUPS = [
    '唐揚げ食べ隊',
    'ゆるふわ（仮）',
    '全く共通点のないオレら、これからどうなっちゃうの～！？ドキドキパラダイス伝説編',
    'セロガキ',
    '野菜生活',
    'ハイトーンチーム',
]

MEDALS = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣']

COLORS = ['#FF6B6B', '#FFA500', '#FFD700', '#6BCB77', '#4D96FF', '#C77DFF']

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap');

.main { background-color: #0f0f1a; }

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
    animation: slidein 0.4s ease forwards;
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
st.markdown(f'<p class="subtitle">参加グループ: {len(GROUPS)} チーム</p>', unsafe_allow_html=True)

if st.button('🎲 シャッフル！', use_container_width=True, type='primary'):
    with st.spinner('ランダム抽選中...'):
        time.sleep(0.8)
    order = random.sample(GROUPS, len(GROUPS))
    st.session_state['order'] = order
    st.balloons()

if 'order' in st.session_state:
    st.markdown('### 📋 結果発表！')
    for i, group in enumerate(st.session_state['order']):
        color = COLORS[i]
        medal = MEDALS[i]
        st.markdown(f'''
        <div class="card" style="background: linear-gradient(135deg, {color}cc, {color}66); border-left: 6px solid {color};">
            <span class="medal">{medal}</span>
            <div>
                <div class="rank">{i+1}番目</div>
                <div class="name">{group}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
