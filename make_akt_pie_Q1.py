import openpyxl
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import japanize_matplotlib  # pip install japanize-matplotlib
from collections import Counter

# Illustratorでテキストを編集可能にする(アウトライン化ではなくフォント埋め込み)
matplotlib.rcParams['ps.fonttype'] = 42

# --- データ読み込み ---
# akt_dx2026.xlsx をこのファイルと同じフォルダに置いてください
wb = openpyxl.load_workbook('akt_dx2026.xlsx', data_only=True)
ws = wb['Sheet1']
rows = list(ws.iter_rows(values_only=True))
data = rows[1:]

answers = [r[0] for r in data if r[0] is not None]  # Q1列
OUTPATH = 'akt_dx2026_Q1.eps'

# 達成度が高い順の固定順序(この順で色・凡例を揃える)
ORDER = ['達成できた', 'どちらかと言えば達成できた',
         'どちらかと言えば達成できなかった', '達成できなかった']

COLORS = {
    '達成できた': '#007354',
    'どちらかと言えば達成できた': '#d09200',
    'どちらかと言えば達成できなかった': '#c92124',
    '達成できなかった': '#8a1620',
}

INK = '#222222'
INK_SUB = '#555555'
INK_MUTED = '#888888'

n = len(answers)
counts = Counter(answers)
labels = [lab for lab in ORDER if lab in counts]
values = [counts[lab] for lab in labels]
colors = [COLORS[lab] for lab in labels]
pcts = [v / n * 100 for v in values]

fig = plt.figure(figsize=(9, 5.5), dpi=150)
ax = fig.add_axes((0, 0, 1, 1))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# ドーナツ本体
pie_ax = fig.add_axes((0.02, 0.05, 0.55, 0.90))
pie_ax.set_aspect('equal')

wedges, _ = pie_ax.pie(
    values,
    colors=colors,
    startangle=90,
    counterclock=False,
    wedgeprops=dict(width=0.38, edgecolor='white', linewidth=2),
    radius=1.0,
)

# スライスごとのラベル(%)。小さいスライスは外側に引き出す
for w, pct in zip(wedges, pcts):
    ang = (w.theta2 + w.theta1) / 2
    x, y = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
    if pct >= 8:
        r = 0.81
        pie_ax.text(x * r, y * r, f'{pct:.0f}%', ha='center', va='center',
                    fontsize=16, color='#ffffff', fontweight='bold', zorder=5)
    else:
        r_in, r_out = 1.03, 1.22
        pie_ax.plot([x * r_in, x * r_out], [y * r_in, y * r_out],
                    color=INK_MUTED, linewidth=1.2, zorder=5)
        ha = 'left' if x >= 0 else 'right'
        pie_ax.text(x * 1.28, y * 1.22, f'{pct:.0f}%', ha=ha, va='center',
                    fontsize=16, color=INK, fontweight='bold', zorder=5)

pie_ax.set_xlim(-1.55, 1.55)
pie_ax.set_ylim(-1.55, 1.55)

# 凡例(ドーナツのすぐ右・縦積み・中央揃え)
legend_dot_x = 0.49
legend_text_x = 0.515
row_h = 0.11
top_y = 0.5 + (len(labels) - 1) * row_h / 2
for i, (lab, val, pct) in enumerate(zip(labels, values, pcts)):
    y0 = top_y - i * row_h
    ax.add_patch(plt.Circle((legend_dot_x, y0), 0.014,
                             facecolor=COLORS[lab], linewidth=0, zorder=3))
    ax.text(legend_text_x, y0 + 0.011, lab, ha='left', va='center',
            fontsize=12, color=INK, zorder=3)
    ax.text(legend_text_x, y0 - 0.020, f'{pct:.0f}%', ha='left', va='center',
            fontsize=10.5, color=INK_SUB, zorder=3)

fig.savefig(OUTPATH, format='eps', transparent=True)
plt.show()
print(f'saved: {OUTPATH}  n={n}  ' +
      ', '.join(f'{l}:{c}({c/n*100:.1f}%)' for l, c in zip(labels, values)))
