import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, binom
import streamlit as st

import matplotlib_fontja
plt.rcParams['axes.unicode_minus'] = False

st.write('新潟大学創生学部：データサイエンス概説')
st.title('正規分布のシミュレーション')

# --- サイドバー: パラメータ設定 ---
st.sidebar.header('パラメータ設定')

mu = st.sidebar.slider('平均 μ', min_value=1.0, max_value=100.0, value=15.0, step=0.5)
sigma = st.sidebar.slider('標準偏差 σ', min_value=0.5, max_value=15.0, value=3.0, step=0.5)

show_binomial = st.sidebar.checkbox('二項分布を重ねて表示', value=False)

# --- x軸範囲 ---
x_lo = mu - 4 * sigma
x_hi = mu + 4 * sigma
x_norm = np.linspace(x_lo, x_hi, 300)

# --- プロット ---
fig = plt.figure(figsize=(9, 5))

# 二項分布の描画 (μ, σ から n, p を逆算)
binom_valid = False
if show_binomial:
    # μ = np, σ² = np(1-p) → p = 1 - σ²/μ, n = μ/p
    if sigma ** 2 < mu:
        p_b = 1 - sigma ** 2 / mu
        n_b = int(round(mu / p_b))
        p_b = mu / n_b  # n を整数化した後で p を再計算
        sigma_b = np.sqrt(n_b * p_b * (1 - p_b))
        k = np.arange(max(0, int(x_lo)), int(x_hi) + 1)
        y_b = binom.pmf(k, n_b, p_b)
        plt.bar(k, y_b, color='steelblue', alpha=0.6,
                label=f'二項分布 B(n={n_b}, p={p_b:.3f})')
        binom_valid = True
    else:
        st.sidebar.warning('σ² ≥ μ のため二項分布を表示できません（二項分布では必ず σ² < μ）')

plt.plot(x_norm, norm.pdf(x_norm, loc=mu, scale=sigma),
         'r-', linewidth=2.5, label=f'正規分布 N(μ={mu:.1f}, σ={sigma:.1f})')

plt.xlabel('x', fontsize=14)
plt.ylabel('f(x)', fontsize=14)
plt.title('正規分布の確率密度関数 (PDF)', fontsize=16)
plt.xlim(x_lo, x_hi)
plt.grid(color='gray', linestyle=':', alpha=0.7)
plt.legend(fontsize=12, frameon=False)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --- 統計量の表示 ---
st.subheader('統計量')
col1, col2 = st.columns(2)
with col1:
    st.metric('平均 μ', f'{mu:.2f}')
    st.metric('標準偏差 σ', f'{sigma:.2f}')
    st.metric('分散 σ²', f'{sigma**2:.2f}')
with col2:
    if show_binomial and binom_valid:
        st.metric('対応する二項分布 n', f'{n_b}')
        st.metric('対応する二項分布 p', f'{p_b:.4f}')
        st.metric('二項分布の標準偏差 √(np(1-p))', f'{sigma_b:.4f}')

# --- 近似の説明 ---
if show_binomial and binom_valid:
    st.subheader('二項分布との関係')
    st.write(
        '二項分布 $B(n, p)$ は $n$ が大きいとき、'
        '平均 $\\mu = np$、標準偏差 $\\sigma = \\sqrt{np(1-p)}$ の正規分布で近似できます。'
    )
    st.write(f'現在の設定に対応: $n={n_b}$、$p={p_b:.4f}$、$\\mu={n_b*p_b:.2f}$、$\\sigma={sigma_b:.4f}$')
