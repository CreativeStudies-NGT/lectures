import streamlit as st
import random

GROUPS = [
    '唐揚げ食べ隊',
    'ゆるふわ（仮）',
    '全く共通点のないオレら、これからどうなっちゃうの～！？ドキドキパラダイス伝説編',
    'セロガキ',
    '野菜生活',
    'ハイトーンチーム',
]

st.title('発表順番決め')
st.write(f'参加グループ数: {len(GROUPS)} グループ')

if st.button('🎲 順番を決める', use_container_width=True):
    order = random.sample(GROUPS, len(GROUPS))
    st.session_state['order'] = order

if 'order' in st.session_state:
    st.subheader('発表順番')
    for i, group in enumerate(st.session_state['order'], 1):
        st.markdown(f'**{i}番目:** {group}')
