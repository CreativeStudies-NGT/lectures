import numpy as np
import matplotlib.pyplot as plt
import matplotlib_fontja
import streamlit as st
from scipy.stats import binom

st.set_page_config(page_title='二項分布の可視化', layout='centered')
st.title('二項分布の可視化')
st.markdown('スライダーで **試行回数 n** と **成功確率 p** を変えて分布の変化を確認しよう。')

n = st.slider('試行回数 n', min_value=1, max_value=100, value=10, step=1)
p = st.slider('成功確率 p', min_value=0.01, max_value=0.99, value=0.4, step=0.01)

x = np.arange(0, n + 1)
y = binom.pmf(x, n, p)

mu = n * p
sigma = np.sqrt(n * p * (1 - p))

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(x, y, color='y', zorder=2)
ax.set_title('二項分布', fontsize=16)
ax.set_xlabel('実現値 (x)', fontsize=12)
ax.set_ylabel('f(x)', fontsize=12)
ax.grid(True, zorder=1)
ax.text(0.85, 0.90, f'n={n}',        fontsize=12, transform=ax.transAxes)
ax.text(0.85, 0.83, f'p={p:.2f}',    fontsize=12, transform=ax.transAxes)
ax.text(0.85, 0.74, f'μ={mu:.2f}',   fontsize=12, transform=ax.transAxes)
ax.text(0.85, 0.65, f'σ={sigma:.2f}', fontsize=12, transform=ax.transAxes)
st.pyplot(fig)
plt.close(fig)

col1, col2, col3 = st.columns(3)
col1.metric('期待値 μ', f'{mu:.4f}')
col2.metric('標準偏差 σ', f'{sigma:.4f}')
col3.metric('分散 σ²', f'{n*p*(1-p):.4f}')

with st.expander('各実現値の確率を表示'):
    mask = y > 0.0001
    rows = [{'x': int(xi), 'f(x)': f'{yi:.6f}'} for xi, yi in zip(x[mask], y[mask])]
    st.dataframe(rows, use_container_width=True)

st.markdown('---')
st.markdown(
    '**累積確率の計算**  \n'
    'ある値 x₀ を指定して、P(X = x₀)・P(X ≥ x₀)・P(X ≤ x₀) を確認できます。'
)
x0 = st.number_input('実現値 x₀', min_value=0, max_value=n, value=min(int(round(mu)), n), step=1)

c1, c2, c3 = st.columns(3)
c1.metric(f'P(X = {x0})', f'{y[x0]:.4f}')
c2.metric(f'P(X ≥ {x0})', f'{y[x0:].sum():.4f}')
c3.metric(f'P(X ≤ {x0})', f'{y[:x0+1].sum():.4f}')
