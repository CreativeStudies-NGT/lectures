import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

import matplotlib_fontja
plt.rcParams['axes.unicode_minus'] = False

st.write('新潟大学創生学部：データサイエンス概説')
st.title('二等辺三角形分布と面積計算')

st.markdown('中心 $\\mu$、半幅 $h$ の二等辺三角形（面積 = 1）')

st.latex(r'''
f(x) = \begin{cases}
  \dfrac{x - (\mu - h)}{h^2} & (\mu - h \leq x \leq \mu) \\[6pt]
  \dfrac{(\mu + h) - x}{h^2} & (\mu \leq x \leq \mu + h) \\[4pt]
  0 & (\text{otherwise})
\end{cases}
''')

st.latex(r'''
F(x) = \int_{\mu-h}^{x} f(t)\,dt = \begin{cases}
  \dfrac{(x-(\mu-h))^2}{2h^2} & (\mu-h \leq x \leq \mu) \\[6pt]
  1 - \dfrac{((\mu+h)-x)^2}{2h^2} & (\mu \leq x \leq \mu+h)
\end{cases}
''')


def pdf(x, mu, h):
    x = np.asarray(x, dtype=float)
    left, right = mu - h, mu + h
    return np.where(x < left, 0.0,
           np.where(x <= mu, (x - left) / h**2,
           np.where(x <= right, (right - x) / h**2, 0.0)))


def cdf(x, mu, h):
    left, right = mu - h, mu + h
    if x < left:
        return 0.0
    elif x <= mu:
        return (x - left)**2 / (2 * h**2)
    elif x <= right:
        return 1 - (right - x)**2 / (2 * h**2)
    else:
        return 1.0


# --- サイドバー ---
st.sidebar.header('三角形のパラメータ')
mu = st.sidebar.slider('中心 μ', -3.0, 3.0, 0.0, 0.1)
h  = st.sidebar.slider('半幅 h', 0.5, 3.0, 1.0, 0.1)

left, right = mu - h, mu + h

st.sidebar.header('区間のパラメータ')
st.sidebar.caption(f'三角形の範囲：{left:.2f} 〜 {right:.2f}')
# a, b は三角形内の位置を % で指定（スライダー範囲が μ, h に依存しないため安定）
a_pct = st.sidebar.slider('下限 a の位置 (%)', 0, 100, 25)
b_pct = st.sidebar.slider('上限 b の位置 (%)', 0, 100, 75)
a = left + a_pct / 100 * 2 * h
b = left + b_pct / 100 * 2 * h

if a > b:
    a, b = b, a

Fa = cdf(a, mu, h)
Fb = cdf(b, mu, h)
area = Fb - Fa

# --- プロット ---
margin = h * 0.3
x_all = np.linspace(left - margin, right + margin, 600)

fig = plt.figure(figsize=(9, 5))

x_left_fill = x_all[(x_all >= left) & (x_all <= a)]
if len(x_left_fill) > 0:
    plt.fill_between(x_left_fill, pdf(x_left_fill, mu, h),
                     alpha=0.20, color='steelblue', label=f'$F(a) = {Fa:.4f}$')

x_mid = x_all[(x_all >= a) & (x_all <= b)]
if len(x_mid) > 0:
    plt.fill_between(x_mid, pdf(x_mid, mu, h),
                     alpha=0.55, color='red', label=f'$F(b) - F(a) = {area:.4f}$')

plt.plot(x_all, pdf(x_all, mu, h), 'b-', linewidth=2.5, label='$f(x)$')
plt.axvline(a, color='steelblue', linestyle='--', linewidth=1.8, label=f'$a = {a:.3f}$')
plt.axvline(b, color='firebrick', linestyle='--', linewidth=1.8, label=f'$b = {b:.3f}$')

plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('x', fontsize=14)
plt.ylabel('f(x)', fontsize=14)
plt.title(f'二等辺三角形分布　μ = {mu:.1f}、h = {h:.1f}', fontsize=16)
plt.xlim(left - margin, right + margin)
plt.ylim(bottom=0, top=1 / h * 1.15)
plt.grid(color='gray', linestyle=':', alpha=0.7)
plt.legend(fontsize=12, frameon=False, loc='upper right')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# --- 計算結果 ---
st.subheader('計算結果')
col1, col2, col3 = st.columns(3)
col1.metric('F(a)　（左端 〜 a の面積）', f'{Fa:.4f}', f'a = {a:.3f}', delta_color='off')
col2.metric('F(b)　（左端 〜 b の面積）', f'{Fb:.4f}', f'b = {b:.3f}', delta_color='off')
col3.metric('F(b) − F(a)　（a 〜 b の面積）', f'{area:.4f}')

st.latex(r'P(a \leq X \leq b) = F(b) - F(a)')
st.caption('正規分布表も同じしくみで、F(z) を表から引いて差をとることで区間の確率を計算します。')

st.info('**標準二等辺三角形**は μ = 0、h = 1 の場合です。')
