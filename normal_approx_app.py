import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, binom
import streamlit as st

import matplotlib_fontja
plt.rcParams['axes.unicode_minus'] = False

st.write('新潟大学創生学部：データサイエンス概説')
st.title('正規分布のシミュレーション（二項分布からの近似）')

# --- サイドバー: パラメータ設定 ---
st.sidebar.header('パラメータ設定')

n = st.sidebar.slider('試行回数 n', min_value=5, max_value=200, value=30, step=1)
p = st.sidebar.slider('成功確率 p', min_value=0.01, max_value=0.99, value=0.4, step=0.01)

show_binomial = st.sidebar.checkbox('二項分布を重ねて表示', value=False)

# --- 統計量の計算 ---
mu = n * p
sigma = np.sqrt(n * p * (1 - p))

# --- x軸範囲 ---
x_lo = max(0, mu - 4 * sigma)
x_hi = min(n, mu + 4 * sigma)
x_norm = np.linspace(x_lo, x_hi, 300)

# --- プロット ---
fig = plt.figure(figsize=(9, 5))

if show_binomial:
    k = np.arange(int(x_lo), int(x_hi) + 1)
    y_b = binom.pmf(k, n, p)
    plt.bar(k, y_b, color='steelblue', alpha=0.6, label=f'二項分布 (n={n}, p={p:.2f})')

plt.plot(x_norm, norm.pdf(x_norm, loc=mu, scale=sigma),
         'r-', linewidth=2.5, label=f'正規分布 N(μ={mu:.2f}, σ={sigma:.2f})')

plt.xlabel('x', fontsize=14)
plt.ylabel('f(x)', fontsize=14)
plt.title('正規分布の確率密度関数 (PDF)', fontsize=16)
plt.xlim(x_lo - 1, x_hi + 1)
plt.grid(color='gray', linestyle=':', alpha=0.7)
plt.legend(fontsize=12, frameon=False)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --- 統計量の表示 ---
st.subheader('統計量')
col1, col2 = st.columns(2)
with col1:
    st.metric('平均 μ = np', f'{mu:.4f}')
    st.metric('標準偏差 σ = √(np(1-p))', f'{sigma:.4f}')
    st.metric('分散 σ² = np(1-p)', f'{n * p * (1 - p):.4f}')
with col2:
    if show_binomial:
        st.metric('近似の目安 (np ≥ 5)', f'{mu:.2f}', delta='OK' if mu >= 5 else 'NG')
        st.metric('近似の目安 (n(1-p) ≥ 5)', f'{n * (1-p):.2f}', delta='OK' if n * (1 - p) >= 5 else 'NG')
        k_all = np.arange(0, n + 1)
        y_p = norm.pdf(k_all, loc=mu, scale=sigma)
        y_b_all = binom.pmf(k_all, n, p)
        tvd = 0.5 * np.sum(np.abs(y_p / y_p.sum() - y_b_all))
        st.metric('総変動距離 (0に近いほど近似精度が高い)', f'{tvd:.4f}')

# --- 近似の説明 ---
if show_binomial:
    st.subheader('近似の条件')
    st.write(
        '二項分布 $B(n, p)$ は、$n$ が大きいとき平均 $\\mu = np$、'
        '標準偏差 $\\sigma = \\sqrt{np(1-p)}$ の正規分布で近似できます。'
    )
    st.write('一般的な目安: $np \\geq 5$ かつ $n(1-p) \\geq 5$')
