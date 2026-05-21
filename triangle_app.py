import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

import matplotlib_fontja
plt.rcParams['axes.unicode_minus'] = False

st.write('新潟大学創生学部：データサイエンス概説')
st.title('標準二等辺三角形分布と面積計算')

st.markdown('底辺2（$-1 \\leq x \\leq 1$）、頂点 $(0, 1)$ の二等辺三角形で、面積は1。')

st.latex(r'''
f(x) = \begin{cases}
  x + 1 & (-1 \leq x \leq 0) \\
  1 - x & (0 \leq x \leq 1) \\
  0      & (\text{otherwise})
\end{cases}
''')

st.latex(r'F(x) = \int_{-1}^{x} f(t)\,dt \quad\text{（-1 からの累積面積）}')


def pdf(x):
    x = np.asarray(x, dtype=float)
    return np.where(x < -1, 0.0,
           np.where(x <= 0, x + 1,
           np.where(x <= 1, 1 - x, 0.0)))


def cdf(x):
    if x < -1:
        return 0.0
    elif x <= 0:
        return (x + 1) ** 2 / 2
    elif x <= 1:
        return 1 - (1 - x) ** 2 / 2
    else:
        return 1.0


# --- サイドバー ---
st.sidebar.header('パラメータ設定')
a = st.sidebar.slider('下限 a', min_value=-1.0, max_value=1.0, value=-0.5, step=0.05)
b = st.sidebar.slider('上限 b', min_value=-1.0, max_value=1.0, value=0.5, step=0.05)

if a > b:
    a, b = b, a

Fa = cdf(a)
Fb = cdf(b)
area = Fb - Fa

# --- プロット ---
x_all = np.linspace(-1.3, 1.3, 600)

fig = plt.figure(figsize=(9, 5))

# -1 〜 a の累積面積（薄い青）
x_left = x_all[(x_all >= -1) & (x_all <= a)]
if len(x_left) > 0:
    plt.fill_between(x_left, pdf(x_left), alpha=0.20, color='steelblue',
                     label=f'$F(a) = {Fa:.4f}$')

# a 〜 b の面積（赤）
x_mid = x_all[(x_all >= a) & (x_all <= b)]
if len(x_mid) > 0:
    plt.fill_between(x_mid, pdf(x_mid), alpha=0.55, color='red',
                     label=f'$F(b) - F(a) = {area:.4f}$')

# 三角形の輪郭
plt.plot(x_all, pdf(x_all), 'b-', linewidth=2.5, label='$f(x)$')

# 縦線
plt.axvline(a, color='steelblue', linestyle='--', linewidth=1.8, label=f'$a = {a:.2f}$')
plt.axvline(b, color='firebrick', linestyle='--', linewidth=1.8, label=f'$b = {b:.2f}$')

plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('x', fontsize=14)
plt.ylabel('f(x)', fontsize=14)
plt.title('標準二等辺三角形分布', fontsize=16)
plt.xlim(-1.3, 1.3)
plt.ylim(bottom=0, top=1.15)
plt.grid(color='gray', linestyle=':', alpha=0.7)
plt.legend(fontsize=12, frameon=False, loc='upper right')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --- 計算結果 ---
st.subheader('計算結果')
col1, col2, col3 = st.columns(3)
col1.metric('F(a)　（-1 〜 a の面積）', f'{Fa:.4f}')
col2.metric('F(b)　（-1 〜 b の面積）', f'{Fb:.4f}')
col3.metric('F(b) − F(a)　（a 〜 b の面積）', f'{area:.4f}')

st.markdown('''
**面積の求め方：**
$$P(a \\leq X \\leq b) = F(b) - F(a)$$

正規分布表も同じしくみで、$F(z)$ を表から引いて差をとることで区間の確率を計算します。
''')
