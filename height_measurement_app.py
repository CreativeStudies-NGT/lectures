import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib_fontja

plt.rcParams['axes.unicode_minus'] = False

st.write('新潟大学創生学部：データサイエンス概説')
st.title('中心極限定理のデモ ― 身長の繰り返し測定')
st.write(
    '真値 μ の身長を測定誤差 σ = 0.5 cm で繰り返し測定するシミュレーション。'
    ' **N 回の測定平均**は標準誤差 σ/√N の正規分布に従います（中心極限定理）。'
)

# --- サイドバー ---
st.sidebar.header('パラメータ設定')
true_height = st.sidebar.number_input('真値 μ (cm)', min_value=140.0, max_value=200.0,
                                       value=160.0, step=0.5)
sigma = 0.5
N = st.sidebar.slider('測定回数 N', min_value=1, max_value=200, value=1, step=1)

se = sigma / np.sqrt(N)
st.sidebar.markdown('---')
st.sidebar.metric('標準誤差 σ/√N', f'{se:.4f} cm')

N_REPEAT = 2000
rng = np.random.default_rng()

tab1, tab2 = st.tabs(['📊 標本平均の分布', '📈 測定回数の比較'])

# --- Tab1: N に応じた標本平均分布 ---
with tab1:
    samples = rng.normal(true_height, sigma, (N_REPEAT, N))
    means = samples.mean(axis=1)

    x = np.linspace(true_height - 4 * sigma, true_height + 4 * sigma, 500)

    fig1 = plt.figure(figsize=(9, 5))
    plt.hist(means, bins=60, density=True, facecolor='steelblue', ec='k', alpha=0.6,
             label=f'標本平均の分布 (N={N}, {N_REPEAT}回)')
    plt.plot(x, norm.pdf(x, true_height, se), 'r-', lw=2,
             label=f'理論値: σ/√N = {se:.4f} cm')
    plt.axvline(true_height, color='k', ls='--', lw=1.5, label=f'真値 {true_height:.1f} cm')
    plt.xlabel('N 回測定の平均値 (cm)', fontsize=13)
    plt.ylabel('確率密度', fontsize=13)
    plt.title(f'N = {N} 回測定の標本平均分布', fontsize=15)
    plt.xlim(true_height - 3.5 * sigma, true_height + 3.5 * sigma)
    plt.grid(color='gray', linestyle=':', alpha=0.7)
    plt.legend(fontsize=12, frameon=False)
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

    st.subheader('統計量')
    col1, col2, col3 = st.columns(3)
    col1.metric('測定回数 N', f'{N}')
    col2.metric('標準誤差 σ/√N', f'{se:.4f} cm')
    col3.metric('標本平均の標準偏差', f'{means.std():.4f} cm', f'理論値 {se:.4f}')

# --- Tab2: 複数 N の比較（静的） ---
with tab2:
    N_values = [1, 4, 16, 100]
    colors = ['royalblue', 'seagreen', 'orange', 'crimson']
    x2 = np.linspace(true_height - 3.5 * sigma, true_height + 3.5 * sigma, 500)

    fig2 = plt.figure(figsize=(9, 5))
    for nv, color in zip(N_values, colors):
        samp = rng.normal(true_height, sigma, (N_REPEAT, nv))
        m = samp.mean(axis=1)
        se_nv = sigma / np.sqrt(nv)
        plt.hist(m, bins=60, density=True, alpha=0.35, color=color, ec='none')
        plt.plot(x2, norm.pdf(x2, true_height, se_nv), color=color, lw=2,
                 label=f'N={nv:3d}  σ/√N = {se_nv:.3f} cm')

    plt.axvline(true_height, color='k', ls='--', lw=1.5, label=f'真値 {true_height:.1f} cm')
    plt.xlabel('N 回測定の平均値 (cm)', fontsize=13)
    plt.ylabel('確率密度', fontsize=13)
    plt.title('測定回数 N による標本平均分布の変化', fontsize=15)
    plt.xlim(true_height - 3.5 * sigma, true_height + 3.5 * sigma)
    plt.grid(color='gray', linestyle=':', alpha=0.7)
    plt.legend(fontsize=11, frameon=False)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    st.subheader('標準誤差 σ/√N の一覧')
    col1, col2, col3, col4 = st.columns(4)
    for col, nv in zip([col1, col2, col3, col4], N_values):
        col.metric(f'N = {nv}', f'{sigma / np.sqrt(nv):.4f} cm')
