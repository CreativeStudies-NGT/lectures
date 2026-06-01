import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib_fontja

plt.rcParams['axes.unicode_minus'] = False

st.write('新潟大学創生学部：データサイエンス概説')
st.title('中心極限定理のデモ ― サイコロ実験')
st.write(
    'サイコロの出目は 1〜6 の**一様分布**に従い、特定の目が出やすいわけではない。'
    'しかし **N 個のサイコロの平均値**を何度も求めると、その分布は正規分布に近づく（中心極限定理）。'
)

# サイコロの理論値
MU = 3.5
SIGMA = np.sqrt(35 / 12)   # 一様分布 {1,…,6} の標準偏差 ≈ 1.708
N_REPEAT = 2000
DICE = list(range(1, 7))

st.sidebar.header('パラメータ設定')
N = st.sidebar.slider('サイコロの個数 N（1試行あたり）', min_value=1, max_value=100, value=1, step=1)
se = SIGMA / np.sqrt(N)
st.sidebar.markdown('---')
st.sidebar.metric('標準偏差 σ/√N（理論値）', f'{se:.4f}')
st.sidebar.caption(f'サイコロ1個の理論値：μ = {MU}、σ = {SIGMA:.4f}')
st.sidebar.markdown('---')
st.sidebar.button('🎲 振り直す')

rng = np.random.default_rng()

tab1, tab2 = st.tabs(['🎲 出目の分布（元の分布）', '📊 標本平均の分布'])

# --- Tab1: サイコロN個の出目の分布 ---
with tab1:
    st.markdown(f'**サイコロを {N} 回振った結果**。どの目も同じ確率（1/6）で出るはず。')
    rolls = rng.integers(1, 7, N)

    fig1 = plt.figure(figsize=(8, 5))
    plt.hist(rolls, bins=range(1, 8), align='left', density=True,
             facecolor='steelblue', ec='k', alpha=0.8, label=f'実験結果 (N={N}回)')
    plt.axhline(1 / 6, color='r', ls='--', lw=2, label='理論値 1/6 ≈ 0.167')
    plt.xticks(DICE)
    plt.xlabel('サイコロの目', fontsize=13)
    plt.ylabel('相対頻度', fontsize=13)
    plt.title(f'サイコロを {N} 回振った出目の分布', fontsize=15)
    plt.ylim(0, 0.6)
    plt.legend(fontsize=12)
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

    st.info('N が小さいと出目はバラつく。N を大きくすると理論値（赤破線）に近づいていく。')

# --- Tab2: 標本平均の分布 ---
with tab2:
    st.markdown(
        f'サイコロを **{N} 個**振って平均値を記録する、という操作を **{N_REPEAT} 回**繰り返した結果。'
    )
    samples = rng.integers(1, 7, (N_REPEAT, N))
    means = samples.mean(axis=1)

    x = np.linspace(1, 6, 500)

    fig2 = plt.figure(figsize=(8, 5))
    plt.hist(means, bins=40, density=True,
             facecolor='steelblue', ec='k', alpha=0.6,
             label=f'標本平均の分布 (N={N}, {N_REPEAT}回)')
    plt.plot(x, norm.pdf(x, MU, se), 'r-', lw=2,
             label=f'理論値（正規分布）: σ/√N = {se:.4f}')
    plt.axvline(MU, color='k', ls='--', lw=1.5, label=f'理論平均 μ = {MU}')
    plt.xlabel(f'サイコロ {N} 個の出目の平均値', fontsize=13)
    plt.ylabel('確率密度', fontsize=13)
    plt.title(f'N = {N} のときの標本平均の分布（{N_REPEAT} 回試行）', fontsize=14)
    plt.xlim(1, 6)
    plt.grid(alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    col1, col2, col3 = st.columns(3)
    col1.metric('サイコロの個数 N', f'{N}')
    col2.metric('σ/√N（理論値）', f'{se:.4f}')
    col3.metric('標本平均の標準偏差（実測）', f'{means.std():.4f}', f'理論値 {se:.4f}')

    st.markdown(f'''
**σ/√N とは？**
サイコロ1個の出目の標準偏差を σ（= {SIGMA:.3f}）とすると、
**N 個の出目の平均値**がどれだけばらつくかは σ/√N で表せる。
N が大きいほど √N も大きくなるので σ/√N は小さくなり、平均値が μ = {MU} の近くに集まりやすくなる。
''')

    st.info('N を大きくすると、ヒストグラムが赤い正規分布曲線にどんどん近づいていく。')
