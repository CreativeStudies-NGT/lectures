import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from math import gcd

fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.25)

x_full = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
(line_sin,) = plt.plot(x_full, np.sin(x_full), 'b-', lw=2, label='y = sin(x)')
(line_lin,) = plt.plot(x_full, x_full, 'r--', lw=2, label='y = x')

plt.axhline(0, color='k', lw=0.5)
plt.axvline(0, color='k', lw=0.5)
plt.legend(fontsize=13)
plt.title('sin(x) の近似：原点に近づくほど y = x に一致する', fontsize=13)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.grid(True, alpha=0.3)

ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
slider = Slider(ax_slider, '拡大率', 1.0, 50.0, valinit=1.0, valstep=0.5)

slider_label = plt.axes([0.2, 0.05, 0.6, 0.03])
slider_label.axis('off')
info_text = slider_label.text(
    0.5, 0.5,
    '← スライダーを左に動かすと原点付近を拡大できます →',
    ha='center', va='center', fontsize=11, color='gray',
    transform=slider_label.transAxes,
)

# π分数の目盛りラベルを生成（tick = n * num/den * π）
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

# 表示範囲 half に応じて適切な目盛りを返す（常にπ表示）
def auto_pi_ticks(half):
    # 分母を増やしながら π/d 刻みを試す → 常にπ分数で表示
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

def update(val):
    zoom = slider.val
    half = 4.0 / zoom
    ax.set_xlim(-half, half)
    ax.set_ylim(-half, half)

    pct = abs(np.sin(half) - half) / (abs(half) + 1e-9) * 100
    info_text.set_text(
        f'表示範囲: ±{half:.3f}　　'
        f'端点での誤差: {pct:.2f}%'
    )

    ticks, labels = auto_pi_ticks(half)
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, fontsize=11)
    fig.canvas.draw_idle()

slider.on_changed(update)
update(1.0)

plt.show()
