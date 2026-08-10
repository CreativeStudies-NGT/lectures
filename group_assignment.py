import sys
import math
import pandas as pd
import numpy as np
from gurobipy import Model, GRB, quicksum


def extract_program(affiliation):
    for kw, label in [
        ('アニメ',          'アニメ・映像'),
        ('日本酒',          '日本酒学'),
        ('ひと脳',          'ひと脳・健康'),
        ('情報社会デザイン', '情報社会デザイン'),
        ('システム創成',    'システム創成'),
    ]:
        if kw in affiliation:
            return label
    return 'その他'


# ── データ読み込み ────────────────────────────────────
df = pd.read_excel('学際的科学総論ⅠD.xlsx')
df.columns = ['id', 'name', 'kana', 'affiliation', 'gender']
n = len(df)

is_female = (df['gender'] == '女性').astype(int).values
df['prog'] = df['affiliation'].apply(extract_program)
programs = sorted(df['prog'].unique())
P = len(programs)
prog_map = {p: i for i, p in enumerate(programs)}
prog_idx = np.array([prog_map[p] for p in df['prog']])
members_by_prog = {p: [i for i in range(n) if prog_idx[i] == p] for p in range(P)}
prog_totals = np.array([len(members_by_prog[p]) for p in range(P)])
females = [i for i in range(n) if is_female[i]]

G = math.ceil(n / 5)   # 各グループ 4〜5 名

print(f'履修者: {n}名  →  {G}グループ（4〜5名）')
print(f'女性: {len(females)}名  プログラム別: ' +
      '  '.join(f'{programs[p]}:{prog_totals[p]}' for p in range(P)))

# ── Gurobi モデル ─────────────────────────────────────
m = Model('groups')
m.Params.TimeLimit = 300   # 5分
m.Params.MIPGap   = 0.01   # 1%以内で打ち切り

x = m.addVars(n, G, vtype=GRB.BINARY, name='x')

# 各学生は1グループのみ
for i in range(n):
    m.addConstr(quicksum(x[i, g] for g in range(G)) == 1)

# グループサイズ 4〜5 名
for g in range(G):
    m.addConstr(quicksum(x[i, g] for i in range(n)) >= 4)
    m.addConstr(quicksum(x[i, g] for i in range(n)) <= 5)

# 性別偏差（各グループの女性数と理想値の差を最小化）
ideal_f = len(females) / G
d_f = m.addVars(G, lb=0, name='df')
for g in range(G):
    fg = quicksum(x[i, g] for i in females)
    m.addConstr(d_f[g] >= fg - ideal_f)
    m.addConstr(d_f[g] >= ideal_f - fg)

# プログラム偏差（各グループのプログラム人数と理想値の差を最小化）
d_p = m.addVars(P, G, lb=0, name='dp')
for p in range(P):
    ideal_p = float(prog_totals[p]) / G
    for g in range(G):
        pg = quicksum(x[i, g] for i in members_by_prog[p])
        m.addConstr(d_p[p, g] >= pg - ideal_p)
        m.addConstr(d_p[p, g] >= ideal_p - pg)

# 目的関数: 性別偏差 + プログラム偏差の総和を最小化
obj = (quicksum(d_f[g] for g in range(G)) +
       quicksum(d_p[p, g] for p in range(P) for g in range(G)))
m.setObjective(obj, GRB.MINIMIZE)

# ウォームスタート: プログラム→女性優先→学籍番号順にソートして交互割り当て
order = sorted(range(n), key=lambda i: (prog_idx[i], -is_female[i], i))
for pos, i in enumerate(order):
    x[i, pos % G].Start = 1

m.optimize()

if m.Status not in [GRB.OPTIMAL, GRB.SUBOPTIMAL, GRB.TIME_LIMIT]:
    print('実行可能解が見つかりませんでした')
    sys.exit(1)

# ── 解の取り出し ──────────────────────────────────────
assignment = {}
for i in range(n):
    for g in range(G):
        if x[i, g].X > 0.5:
            assignment[i] = g + 1
            break

# ── 結果 DataFrame ────────────────────────────────────
rows = []
for i in range(n):
    rows.append({
        'グループ':   assignment[i],
        '在籍番号':   df['id'].iloc[i],
        '氏名':       df['name'].iloc[i],
        '性別':       df['gender'].iloc[i],
        'プログラム': df['prog'].iloc[i],
        '所属':       df['affiliation'].iloc[i],
    })

result = pd.DataFrame(rows).sort_values(['グループ', 'プログラム', '性別'])

# ── コンソール表示 ────────────────────────────────────
print('\n' + '=' * 62)
print('グループ分け結果')
print('=' * 62)
for g in range(1, G + 1):
    grp = result[result['グループ'] == g]
    f_cnt = (grp['性別'] == '女性').sum()
    prog_str = '  '.join(
        f'{k[:5]}:{v}' for k, v in grp['プログラム'].value_counts().items()
    )
    print(f'\n【G{g:02d}】{len(grp)}名 / 女性{f_cnt}名 / {prog_str}')
    for _, row in grp.iterrows():
        mark = '女' if row['性別'] == '女性' else '男'
        print(f'  {row["在籍番号"]}  {row["氏名"]}（{mark}）')

# ── Excel 保存 ────────────────────────────────────────
result.to_excel('グループ分け結果.xlsx', index=False)
print(f'\nグループ分け結果.xlsx に保存しました')
