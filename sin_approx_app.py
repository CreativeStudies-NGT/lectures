import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from math import gcd
from fractions import Fraction

st.write('新潟大学創生学部：データサイエンス概説')
st.title('「近似」について（sin関数を例に）')
st.markdown('原点に近づくほど $\\sin(x) \\approx x$ が成り立つことを確認しよう。')

zoom = st.slider('拡大率', min_value=1.0, max_value=25.0, value=1.0, step=0.5)

def pi_label(n, num, den):
    p, q = n * num, den
    if p == 0:
        return r'$0$'
    g = gcd(abs(p), q)
    p, q = p // g, q // g
    if q == 1:
        if p == 1: return r'$\pi$'
        if p == -1: return r'$-\pi$'
        return rf'${p}\pi$'
    ap = abs(p)
    sign = '-' if p < 0 else ''
    if ap == 1:
        return rf'${sign}\dfrac{{\pi}}{{{q}}}$'
    return rf'${sign}\dfrac{{{ap}\pi}}{{{q}}}$'

def auto_pi_ticks(half):
    denoms = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256]
    for d in denoms:
        step = np.pi / d
        n_max = int(half / step)
        count = 2 * n_max + 1
        if 3 <= count <= 11:
            ns = range(-n_max, n_max + 1)
            ticks = [n * step for n in ns]
            labels = [pi_label(n, 1, d) for n in ns]
            return ticks, labels
    return [0], [r'$0$']

half = 4.0 / zoom
x_full = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x_full, np.sin(x_full), 'b-', lw=2, label='y = sin(x)')
ax.plot(x_full, x_full, 'r--', lw=2, label='y = x')
ax.axhline(0, color='k', lw=0.5)
ax.axvline(0, color='k', lw=0.5)
ax.set_xlim(-half, half)
ax.set_ylim(-half, half)
ax.legend(fontsize=13)
ax.grid(True, alpha=0.3)

ticks, labels = auto_pi_ticks(half)
ax.set_xticks(ticks)
ax.set_xticklabels(labels, fontsize=11)

st.pyplot(fig)
plt.close(fig)

def half_to_pi_str(val):
    r = Fraction(val / np.pi).limit_denominator(256)
    p, q = r.numerator, r.denominator
    if p == 0: return '0'
    if q == 1: return 'π' if p == 1 else f'{p}π'
    if p == 1: return f'π/{q}'
    return f'{p}π/{q}'

pi_str = half_to_pi_str(half)
st.metric('表示範囲', f'±{pi_str}  (±{half:.3f})')

st.markdown("""
**使い方**
- スライダーを左（1倍）にすると広い範囲が見え、sin(x) と y=x がずれていくのがわかる
- スライダーを右に動かすほど原点付近が拡大され、2本の線がぴったり重なっていく
""")
