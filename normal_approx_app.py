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

mu = st.sidebar.slider('平均 μ', min_value=1.0, max_value=100.0, value=50.0, step=0.5)
sigma = st.sidebar.slider('標準偏差 σ', min_value=0.5, max_value=15.0, value=5.0, step=0.5)

show_binomial = st.sidebar.checkbox('二項分布を重ねて表示', value=False)

fix_xaxis = st.sidebar.checkbox('横軸の範囲を固定する', value=True)
if fix_xaxis:
    if 'x_lo_fixed' not in st.session_state:
        st.session_state['x_lo_fixed'] = 0
    if 'x_hi_fixed' not in st.session_state:
        st.session_state['x_hi_fixed'] = 110
    x_lo = st.sidebar.number_input('横軸 最小値', step=1, key='x_lo_fixed')
    x_hi = st.sidebar.number_input('横軸 最大値', step=1, key='x_hi_fixed')
else:
    st.session_state.pop('x_lo_fixed', None)
    st.session_state.pop('x_hi_fixed', None)
    x_lo = mu - 4 * sigma
    x_hi = mu + 4 * sigma

x_norm = np.linspace(x_lo, x_hi, 300)

show_area = st.sidebar.checkbox('区間の面積を表示', value=False)
if show_area:
    k_a = st.sidebar.number_input('始点 (σ の倍数)', value=-1.0, step=0.5, format='%.1f')
    k_b = st.sidebar.number_input('終点 (σ の倍数)', value=1.0, step=0.5, format='%.1f')
    if k_a > k_b:
        k_a, k_b = k_b, k_a
    area_a = mu + k_a * sigma
    area_b = mu + k_b * sigma
    area_prob = norm.cdf(area_b, loc=mu, scale=sigma) - norm.cdf(area_a, loc=mu, scale=sigma)

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

if show_area:
    x_fill = np.linspace(area_a, area_b, 300)
    area_label = f'$P(\\mu{k_a:+.1f}\\sigma \\leq X \\leq \\mu{k_b:+.1f}\\sigma) = {area_prob:.5f}$'
    plt.fill_between(x_fill, norm.pdf(x_fill, loc=mu, scale=sigma),
                     alpha=0.35, color='blue', label=area_label)

# 変曲点 (x = μ ± σ) の表示
y_inf = norm.pdf(mu + sigma, loc=mu, scale=sigma)
plt.vlines([mu - sigma, mu + sigma], 0, y_inf, colors='green', linestyles='--', linewidth=1.5)
plt.hlines(y_inf, mu - sigma, mu + sigma, colors='green', linestyles='-', linewidth=1.5)
# σ の矢印ラベル（左右それぞれ）
arrow_kw = dict(arrowstyle='<->', color='green', lw=1.2)
y_arrow = y_inf * 0.5
plt.annotate('', xy=(mu - sigma, y_arrow), xytext=(mu, y_arrow),
             arrowprops=arrow_kw)
plt.text(mu - sigma / 2, y_arrow * 1.15, 'σ', ha='center', color='green', fontsize=12)
plt.annotate('', xy=(mu + sigma, y_arrow), xytext=(mu, y_arrow),
             arrowprops=arrow_kw)
plt.text(mu + sigma / 2, y_arrow * 1.15, 'σ', ha='center', color='green', fontsize=12)

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
col1, col2, col3 = st.columns(3)
col1.metric('平均 μ', f'{mu:.2f}')
col2.metric('標準偏差 σ', f'{sigma:.2f}')
col3.metric('分散 σ²', f'{sigma**2:.2f}')

if show_binomial and binom_valid:
    col1, col2, col3 = st.columns(3)
    col1.metric('二項分布 n', f'{n_b}')
    col2.metric('二項分布 p', f'{p_b:.4f}')
    col3.metric('二項分布 σ', f'{sigma_b:.4f}')

# --- 区間確率の表示 ---
if show_area:
    st.subheader('区間の確率')
    col1, col2, col3 = st.columns(3)
    col1.metric('始点 a', f'μ{k_a:+.1f}σ = {area_a:.2f}')
    col2.metric('終点 b', f'μ{k_b:+.1f}σ = {area_b:.2f}')
    col3.metric('P(a ≤ X ≤ b)', f'{area_prob:.5f}')

# --- 近似の説明 ---
if show_binomial and binom_valid:
    st.subheader('二項分布との関係')
    st.write(
        '二項分布 $B(n, p)$ は $n$ が大きいとき、'
        '平均 $\\mu = np$、標準偏差 $\\sigma = \\sqrt{np(1-p)}$ の正規分布で近似できます。'
    )
    st.write(f'現在の設定に対応: $n={n_b}$、$p={p_b:.4f}$、$\\mu={n_b*p_b:.2f}$、$\\sigma={sigma_b:.4f}$')
