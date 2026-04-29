import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib_fontja

st.write('新潟大学創生学部：データサイエンス概説')
st.title('サイコロシミュレーション')
st.write('サイコロを $n$ 回振ったときの実現値のヒストグラムです。')

n = st.slider('試行回数 $n$', min_value=10, max_value=10000, value=100, step=10)

if 'seed' not in st.session_state:
    st.session_state.seed = 0

if st.button('🎲 振り直す'):
    st.session_state.seed += 1

rng = np.random.default_rng(st.session_state.seed)
results = rng.integers(1, 7, size=n)

fig, ax = plt.subplots()
ax.hist(results, bins=np.arange(0.5, 7.5, 1), edgecolor='white', color='steelblue', density=True)
ax.axhline(1/6, color='tomato', linestyle='--', linewidth=1.5, label='理論値 $1/6$')
ax.set_xlabel('出目')
ax.set_ylabel('相対度数')
ax.set_title(f'試行回数 $n={n}$')
ax.set_xticks(range(1, 7))
ax.set_ylim(0, 0.5)
ax.legend()
st.pyplot(fig)

counts = np.bincount(results, minlength=7)[1:]
st.write('**各出目の度数**')
st.dataframe(
    {'出目': list(range(1, 7)), '度数': counts, '相対度数': (counts / n).round(4)},
    hide_index=True,
    use_container_width=True,
)
