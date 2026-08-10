import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from matplotlib.collections import LineCollection

conn = sqlite3.connect('/home/hkuma/.claude/skills/insta_follower/instagram.db')
cur = conn.cursor()
cur.execute('SELECT datetime, followers FROM followers ORDER BY datetime ASC')
rows = cur.fetchall()
conn.close()

dates = [datetime.strptime(r[0], '%Y-%m-%d %H:%M:%S') for r in rows]
followers = [r[1] for r in rows]

milestones = {
    300: ('2024-08-06 07:06:24', 301),
    400: ('2025-05-30 07:06:26', 401),
    500: ('2025-09-23 06:44:30', 500),
    600: ('2026-06-03 12:19:18', 600),
}

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

# グラデーション塗りつぶし
n_layers = 200
cmap = plt.colormaps['cool']
y_min = min(followers) - 20
for i in range(n_layers):
    frac = i / n_layers
    y_top = y_min + (max(followers) - y_min) * frac
    ax.fill_between(dates, y_min, [min(f, y_top) for f in followers],
                    color=cmap(frac), alpha=0.012)

# グラデーションライン
points = np.array([mdates.date2num(dates), followers]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = LineCollection(segments, cmap='cool', norm=plt.Normalize(0, len(segments)),
                    linewidth=2.5, zorder=5)
lc.set_array(np.arange(len(segments)))
ax.add_collection(lc)

# マイルストーン
milestone_colors = {'300': '#00d4ff', '400': '#7b61ff', '500': '#ff61d8', '600': '#ffd700'}
for val, (dt_str, fval) in milestones.items():
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    color = milestone_colors[str(val)]
    ax.axhline(val, color=color, linestyle='--', linewidth=0.8, alpha=0.5)
    ax.scatter([dt], [fval], s=120, color=color, zorder=10, edgecolors='white', linewidth=1.5)
    offset_x = -40 if val == 600 else 5
    ha = 'right' if val == 600 else 'left'
    ax.annotate(
        f' {val} ',
        xy=(dt, fval), xytext=(offset_x, 14),
        textcoords='offset points',
        fontsize=12, fontweight='bold', color=color, ha=ha,
        bbox=dict(boxstyle='round,pad=0.3', fc='#0d1117', ec=color, lw=1.2),
        arrowprops=dict(arrowstyle='->', color=color, lw=1.5)
    )

# 600到達の星マーク
dt600 = datetime.strptime('2026-06-03 12:19:18', '%Y-%m-%d %H:%M:%S')
ax.scatter([dt600], [600], s=400, color='#ffd700', marker='*', zorder=15)

# お祝いテキスト
ax.text(0.97, 0.93, '600 Reached!', transform=ax.transAxes,
        fontsize=18, fontweight='bold', color='#ffd700',
        ha='right', va='top',
        bbox=dict(boxstyle='round,pad=0.5', fc='#1a1a2e', ec='#ffd700', lw=2))

# 軸の書式設定
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=35, ha='right', fontsize=11, color='#e0e0e0')
plt.yticks(fontsize=11, color='#e0e0e0')

ax.set_xlim(dates[0], dates[-1])
ax.set_ylim(y_min, 650)
ax.set_xlabel('Date', fontsize=13, color='#cccccc', labelpad=10)
ax.set_ylabel('Followers', fontsize=13, color='#cccccc', labelpad=10)
ax.set_title('Instagram Follower Growth', fontsize=20, fontweight='bold',
             color='white', pad=20)

for spine in ax.spines.values():
    spine.set_edgecolor('#444444')
ax.grid(axis='y', color='#222222', linestyle='-', linewidth=0.5)
ax.grid(axis='x', color='#1a1a1a', linestyle='-', linewidth=0.3)

plt.tight_layout()
plt.savefig('instagram_600.png', dpi=150, bbox_inches='tight', facecolor='#0d1117')
plt.show()
