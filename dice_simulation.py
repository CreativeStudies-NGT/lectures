import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib_fontja

st.write('新潟大学創生学部：データサイエンス概説')
st.title('サイコロシミュレーション')
st.write('サイコロを $n$ 回振ったときの実現値のヒストグラムです。')

# --- サイドバー: パラメータ設定 ---
st.sidebar.header('パラメータ設定')

n = st.sidebar.slider('試行回数 $n$', min_value=10, max_value=6000, value=10, step=10)
yaxis = st.sidebar.radio('縦軸', ['回数', '相対度数'])

if 'seed' not in st.session_state:
    st.session_state.seed = 0

if st.sidebar.button('🎲 振り直す'):
    st.session_state.seed += 1

# --- シミュレーション ---
rng = np.random.default_rng(st.session_state.seed)
results = rng.integers(1, 7, size=n)
use_density = (yaxis == '相対度数')

# --- プロット ---
fig = plt.figure(figsize=(9, 5))

plt.hist(results, bins=np.arange(0.5, 7.5, 1), edgecolor='white', color='steelblue', density=use_density)
if use_density:
    plt.axhline(1/6, color='tomato', linestyle='--', linewidth=1.5, label='理論値 $1/6$')
    plt.ylim(0, 0.5)
else:
    plt.axhline(n/6, color='tomato', linestyle='--', linewidth=1.5, label=f'理論値 $n/6$ = {n/6:.1f}回')
    plt.ylim(0, n * 0.5)

plt.xlabel('出目', fontsize=14)
plt.ylabel(yaxis, fontsize=14)
plt.title(f'試行回数 $n={n}$', fontsize=16)
plt.xticks(range(1, 7))
plt.grid(color='gray', linestyle=':', alpha=0.7)
plt.legend(fontsize=12, frameon=False)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --- 大数の法則 ---
st.markdown('---')
st.subheader('大数の法則')
st.write(
    '試行回数 n を増やすと、各出目の相対度数は理論値 1/6 ≈ 0.167 に近づいていく。'
    'これを**大数の法則**という。'
    'n が小さいときは偏りが目立つが、n を大きくするほどヒストグラムが理論値（赤破線）に揃っていく様子を確認してみよう。'
)

max_dev = np.max(np.abs(counts / n - 1/6))
if max_dev < 0.02:
    st.success(f'n = {n}：各出目の相対度数が理論値 1/6 にかなり近づいている（最大ずれ {max_dev:.3f}）')
elif max_dev < 0.05:
    st.info(f'n = {n}：理論値に近づいてきている（最大ずれ {max_dev:.3f}）。さらに n を増やしてみよう。')
else:
    st.warning(f'n = {n}：まだ理論値からのずれが大きい（最大ずれ {max_dev:.3f}）。n を増やすと変化する。')

st.markdown('---')
# --- 統計量 ---
counts = np.bincount(results, minlength=7)[1:]

st.subheader('統計量')
col1, col2, col3 = st.columns(3)
col1.metric('平均', f'{results.mean():.3f}', f'理論値 3.500')
col2.metric('分散', f'{results.var():.3f}', f'理論値 2.917')
col3.metric('標準偏差', f'{results.std():.3f}', f'理論値 1.708')

st.subheader('各出目の度数')
st.dataframe(
    {'出目': list(range(1, 7)), '度数': counts, '相対度数': (counts / n).round(4)},
    hide_index=True,
    use_container_width=True,
)
