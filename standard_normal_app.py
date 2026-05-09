import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import streamlit as st

import matplotlib_fontja
plt.rcParams['axes.unicode_minus'] = False

st.write('新潟大学創生学部：データサイエンス概説')
st.title('標準正規分布と確率計算')

x_all = np.linspace(-4, 4, 500)

# --- サイドバー ---
st.sidebar.header('確率計算の設定')

mode = st.sidebar.radio(
    '計算モード',
    ['左側の面積 P(X ≤ b)', '右側の面積 P(X ≥ a)', '区間の面積 P(a ≤ X ≤ b)']
)

if mode == '左側の面積 P(X ≤ b)':
    b = st.sidebar.slider('上限 b', min_value=-4.0, max_value=4.0, value=1.0, step=0.05)
    prob = norm.cdf(b)
    label = f'$P(X \\leq {b:.2f}) = {prob:.4f}$'
    x_fill = x_all[x_all <= b]

elif mode == '右側の面積 P(X ≥ a)':
    a = st.sidebar.slider('下限 a', min_value=-4.0, max_value=4.0, value=1.0, step=0.05)
    prob = 1 - norm.cdf(a)
    label = f'$P(X \\geq {a:.2f}) = {prob:.4f}$'
    x_fill = x_all[x_all >= a]

else:
    a = st.sidebar.slider('下限 a', min_value=-4.0, max_value=4.0, value=-1.0, step=0.05)
    b = st.sidebar.slider('上限 b', min_value=-4.0, max_value=4.0, value=1.0, step=0.05)
    if a > b:
        a, b = b, a
    prob = norm.cdf(b) - norm.cdf(a)
    label = f'$P({a:.2f} \\leq X \\leq {b:.2f}) = {prob:.4f}$'
    x_fill = x_all[(x_all >= a) & (x_all <= b)]

# --- プロット ---
fig = plt.figure(figsize=(9, 5))

plt.plot(x_all, norm.pdf(x_all), 'r-', linewidth=2.5, label='N(0, 1)')
plt.fill_between(x_fill, norm.pdf(x_fill), alpha=0.35, color='red', label=label)

plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('z', fontsize=14)
plt.ylabel('f(z)', fontsize=14)
plt.title('標準正規分布 N(0, 1)', fontsize=16)
plt.xlim(-4, 4)
plt.ylim(bottom=0)
plt.grid(color='gray', linestyle=':', alpha=0.7)
plt.legend(fontsize=13, frameon=False)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --- 確率の表示 ---
st.subheader('計算結果')
if mode == '左側の面積 P(X ≤ b)':
    col1, col2 = st.columns(2)
    col1.metric('上限 b', f'{b:.2f}')
    col2.metric('P(X ≤ b)', f'{prob:.4f}')

elif mode == '右側の面積 P(X ≥ a)':
    col1, col2 = st.columns(2)
    col1.metric('下限 a', f'{a:.2f}')
    col2.metric('P(X ≥ a)', f'{prob:.4f}')

else:
    col1, col2, col3 = st.columns(3)
    col1.metric('下限 a', f'{a:.2f}')
    col2.metric('上限 b', f'{b:.2f}')
    col3.metric('P(a ≤ X ≤ b)', f'{prob:.4f}')

# --- 補足 ---
st.caption('標準正規分布は平均 μ=0、標準偏差 σ=1 の正規分布です。'
           '一般の正規分布 N(μ, σ²) は z = (x − μ) / σ で標準化できます。')
