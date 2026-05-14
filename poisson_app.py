import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import poisson, binom
import streamlit as st

import matplotlib_fontja
plt.rcParams['axes.unicode_minus'] = False

st.write('新潟大学創生学部：データサイエンス概説')
st.title('Poisson分布形状のシミュレーション')

# --- サイドバー: パラメータ設定 ---
st.sidebar.header('パラメータ設定')

mu = st.sidebar.slider('ポアソン分布の平均 μ', min_value=0.1, max_value=20.0, value=5.0, step=0.1)

show_binomial = st.sidebar.checkbox('二項分布を表示して比較', value=False)

if show_binomial:
    st.sidebar.subheader('二項分布のパラメータ')
    n_min = max(10, int(np.ceil(mu)))
    n = st.sidebar.slider('試行回数 n', min_value=n_min, max_value=500, value=max(100, n_min), step=10)
    p = mu / n
    st.sidebar.info(f'成功確率 p = μ/n = {p:.4f}')
    st.sidebar.caption('μ = n × p の関係でポアソン分布と結びつきます')

# --- x軸の範囲: μに応じて自動調整 ---
x_max = max(20, int(mu * 3) + 5)
k = np.arange(0, x_max + 1)

# --- プロット ---
fig, ax = plt.subplots(figsize=(9, 5))

y_p = poisson.pmf(k, mu)

if show_binomial:
    y_b = binom.pmf(k, n, p)
    ax.bar(k, y_b, color='steelblue', alpha=0.6, label=f'二項分布 (n={n}, p={p:.4f})')
    ax.plot(k, y_p, 'ro-', markersize=6, linewidth=1.5, label=f'ポアソン分布 (μ={mu})')
else:
    ax.plot(k, y_p, 'bo-', markersize=6, linewidth=1.5, label=f'ポアソン分布 (μ={mu})')

ax.set_xlabel('k', fontsize=14)
ax.set_ylabel('P(X = k)', fontsize=14)
ax.set_title('ポアソン分布の確率質量関数 (PMF)', fontsize=16)
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.set_xlim(-0.5, min(x_max + 0.5, mu * 3 + 5))
ax.grid(color='gray', linestyle=':', alpha=0.7)
ax.legend(fontsize=12, frameon=False)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.latex(r'P(X = k) = \frac{\mu^k \, e^{-\mu}}{k!} \quad (k = 0, 1, 2, \ldots)')

# --- 統計量の表示 ---
st.subheader('統計量')
col1, col2 = st.columns(2)
with col1:
    st.metric('ポアソン分布の平均 (μ)', f'{mu:.2f}')
    st.metric('ポアソン分布の分散 (μ)', f'{mu:.2f}')
    st.metric('ポアソン分布の標準偏差 (√μ)', f'{np.sqrt(mu):.4f}')
with col2:
    if show_binomial:
        bi_mean = n * p
        bi_var = n * p * (1 - p)
        st.metric('二項分布の平均 (np)', f'{bi_mean:.2f}')
        st.metric('二項分布の分散 (np(1-p))', f'{bi_var:.4f}')
        st.metric('二項分布の標準偏差', f'{np.sqrt(bi_var):.4f}')

# --- 確率表 ---
st.subheader('各実現値の確率')
import pandas as pd

display_max = min(x_max, int(mu * 3) + 4)
k_disp = np.arange(0, display_max + 1)
table_data = {'k': k_disp, 'ポアソン P(X=k)': poisson.pmf(k_disp, mu).round(6)}
if show_binomial:
    table_data['二項分布 P(X=k)'] = binom.pmf(k_disp, n, p).round(6)
df = pd.DataFrame(table_data).set_index('k')
st.dataframe(df.style.format('{:.6f}'), use_container_width=True)

# --- 近似精度の説明 ---
if show_binomial:
    st.subheader('近似の精度')
    st.write(f'μ = n × p = {n} × {p:.4f} = {n * p:.4f}')
    st.write(
        'nが大きく、pが小さいとき（μ = npを固定）、二項分布はポアソン分布に近似されます。'
        f' 現在: n={n}, p={p:.4f}'
    )
    # KLダイバージェンス的な差の指標として総変動距離を計算
    tvd = 0.5 * np.sum(np.abs(y_p[:len(k)] - y_b[:len(k)]))
    st.metric('総変動距離 (0に近いほど近似精度が高い)', f'{tvd:.4f}')
