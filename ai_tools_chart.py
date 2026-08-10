import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

df = pd.read_excel('AI_tools2026.xlsx')

counts = {}
for val in df['AI_tools'].dropna():
    for tool in val.split('|'):
        tool = tool.strip()
        counts[tool] = counts.get(tool, 0) + 1

order = ['その他', 'あまり使っていない', 'Claude', 'NotebookLM', 'Copilot', 'Gemini', 'Chat-GPT']
labels = [t for t in order if t in counts]
values = [counts[t] for t in labels]

display_labels = {
    'Chat-GPT': 'ChatGPT',
    'Gemini': 'Gemini',
    'Copilot': 'Copilot',
    'あまり使っていない': 'あまり\n使っていない',
    'その他': 'その他',
    'NotebookLM': 'NotebookLM',
    'Claude': 'Claude',
}

# order (bottom→top): その他, あまり使っていない, Claude, NotebookLM, Copilot, Gemini, Chat-GPT
colors = ['#94A3B8', '#64748B', '#D97706', '#F43F5E', '#9B59B6', '#4285F4', '#10A37F']
colors = colors[:len(labels)]

fig = plt.figure(figsize=(9, 9), facecolor='#0F172A')
ax = fig.add_axes([0.18, 0.05, 0.75, 0.90])
ax.set_facecolor('#0F172A')

y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, values, height=0.62, color=colors, zorder=3)

for spine in ax.spines.values():
    spine.set_visible(False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_xlim(0, max(values) * 1.28)

for i, (bar, val) in enumerate(zip(bars, values)):
    ax.text(
        val + max(values) * 0.02, bar.get_y() + bar.get_height() / 2,
        str(val), va='center', ha='left',
        color='white', fontsize=22, fontweight='bold',
        fontfamily='Noto Sans CJK JP'
    )
    ax.text(
        -max(values) * 0.02, bar.get_y() + bar.get_height() / 2,
        display_labels[labels[i]], va='center', ha='right',
        color='#E2E8F0', fontsize=17, fontweight='bold',
        fontfamily='Noto Sans CJK JP'
    )

ax.set_ylim(-0.6, len(labels) - 0.4)

plt.savefig('ai_tools_chart.png', dpi=150, bbox_inches='tight',
            facecolor='#0F172A', edgecolor='none')
print('saved: ai_tools_chart.png')
print(counts)
