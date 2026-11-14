# LINEST 関数の出力を読み解く（理系向け）

Excel の LINEST 関数は、最小二乗法による回帰の結果を最大 5 行の表にまとめて返します。
この資料では、その表の各マスが **何を表し、どんな仮定のもとで、なぜその式で計算されるのか** を説明します。

**前提とする知識**：行列の積・転置・逆行列・トレース、期待値・分散・共分散、正規分布、偏微分。

## 目次

1. [書式と出力の配置](#1-書式と出力の配置)
2. [モデルと記号](#2-モデルと記号)
3. [1 行目：回帰係数](#3-1-行目回帰係数)
4. [3〜5 行目：残差・平方和・決定係数](#4-35-行目残差平方和決定係数)
5. [2 行目：標準誤差](#5-2-行目標準誤差)
6. [4 行目：F 値と自由度](#6-4-行目f-値と自由度)
7. [LINEST が出さないもの：t 値・p 値・信頼区間](#7-linest-が出さないものt-値p-値信頼区間)
8. [行列計算で LINEST を再現する](#8-行列計算で-linest-を再現する)
9. [使うときの注意](#9-使うときの注意)
10. [参考資料](#10-参考資料)

---

## 1. 書式と出力の配置

### 1.1 書式

```
=LINEST(known_y's, known_x's, const, stats)
```

| 引数 | 意味 |
|---|---|
| `known_y's` | 目的変数 $`y`$ の範囲（$`n`$ 個） |
| `known_x's` | 説明変数の範囲（$`n`$ 行 × $`k`$ 列） |
| `const` | `TRUE`：切片を推定する／`FALSE`：切片を 0 に固定する |
| `stats` | `TRUE`：統計量（2〜5 行目）も出す／`FALSE`：係数（1 行目）だけ |

- Microsoft 365 では Enter だけで結果が広がります。古い Excel では、出力範囲（5 行 × $`(k+1)`$ 列）を選んでから **Ctrl + Shift + Enter** で確定します。
- 多項式をあてはめるときは、`A2:A31^{1,2}` のように指数の配列を使うと、$`x`$ と $`x^2`$ の 2 列を作れます。

### 1.2 出力の配置

$`k`$ 個の説明変数 $`x_1, \dots, x_k`$ を使い、`const` と `stats` をどちらも `TRUE` にした場合の出力です。括弧内は Microsoft のヘルプでの名前です。

| | 1 列目 | 2 列目 | … | $`k`$ 列目 | $`k+1`$ 列目 |
|---|---|---|---|---|---|
| **1 行目** | $`b_k`$ | $`b_{k-1}`$ | … | $`b_1`$ | $`b_0`$（切片） |
| **2 行目** | $`\mathrm{SE}(b_k)`$ | $`\mathrm{SE}(b_{k-1})`$ | … | $`\mathrm{SE}(b_1)`$ | $`\mathrm{SE}(b_0)`$ |
| **3 行目** | $`R^2`$（r2） | $`s`$（sey） | #N/A | #N/A | #N/A |
| **4 行目** | $`F`$ | 自由度 $`n-k-1`$（df） | #N/A | #N/A | #N/A |
| **5 行目** | $`\mathrm{SS_{reg}}`$（ssreg） | $`\mathrm{SS_{res}}`$（ssresid） | #N/A | #N/A | #N/A |

> **係数は説明変数と逆の順に並びます。** `known_x's` の 1 列目 $`x_1`$ の係数 $`b_1`$ は、右から 2 番目に出ます。
> 多項式 `x^{1,2}` なら、左から $`x^2`$ の係数、$`x`$ の係数、切片の順です。

### 1.3 例題

この資料では、次のデータ（$`n = 6`$、$`k = 2`$）を使います。

| | A | B | C | D |
|---|---|---|---|---|
| 1 | 1 | $`x_1`$ | $`x_2`$ | $`y`$ |
| 2 | 1 | 1 | 2 | 4 |
| 3 | 1 | 2 | 1 | 5 |
| 4 | 1 | 3 | 4 | 9 |
| 5 | 1 | 4 | 3 | 10 |
| 6 | 1 | 5 | 6 | 15 |
| 7 | 1 | 6 | 5 | 14 |

A 列の 1 は 8. で行列計算に使います。LINEST には使いません。

F2:H6 に `=LINEST(D2:D7, B2:C7, TRUE, TRUE)` を入力すると、次の値が出ます。

| | F | G | H |
|---|---|---|---|
| 2 | $`b_2 = 1.0833`$ | $`b_1 = 1.4167`$ | $`b_0 = 0.75`$ |
| 3 | $`\mathrm{SE}(b_2) = 0.2846`$ | $`\mathrm{SE}(b_1) = 0.2846`$ | $`\mathrm{SE}(b_0) = 0.6437`$ |
| 4 | $`R^2 = 0.9869`$ | $`s = 0.6667`$ | #N/A |
| 5 | $`F = 112.69`$ | $`\mathrm{df} = 3`$ | #N/A |
| 6 | $`\mathrm{SS_{reg}} = 100.17`$ | $`\mathrm{SS_{res}} = 1.3333`$ | #N/A |

厳密な値は $`b_1 = 17/12`$、$`b_2 = 13/12`$、$`b_0 = 3/4`$、$`\mathrm{SS_{res}} = 4/3`$、$`s = 2/3`$ です。

---

## 2. モデルと記号

### 2.1 モデル

$$
y_i = \beta_0 + \beta_1 x_{i1} + \cdots + \beta_k x_{ik} + \varepsilon_i \qquad (i = 1, \dots, n)
$$

行列で書くと、次のようになります。

$$
y = X\beta + \varepsilon, \qquad
X = \begin{bmatrix} 1 & x_{11} & \cdots & x_{1k} \\ \vdots & \vdots & & \vdots \\ 1 & x_{n1} & \cdots & x_{nk} \end{bmatrix}, \qquad
\beta = \begin{bmatrix} \beta_0 \\ \vdots \\ \beta_k \end{bmatrix}
$$

- $`X`$ は $`n \times p`$ の **計画行列** で、$`p = k + 1`$ は推定するパラメータの個数です。先頭の 1 の列が切片に対応します。
- 推定値を $`b = (b_0, \dots, b_k)^\top`$、予測値を $`\hat{y} = Xb`$、残差を $`r = y - \hat{y}`$ と書きます。

### 2.2 仮定

| 記号 | 仮定 | 内容 |
|---|---|---|
| (A1) | 平均 | $`E[\varepsilon] = 0`$（モデルの形が正しい） |
| (A2) | 共分散 | $`\mathrm{Cov}(\varepsilon) = \sigma^2 I_n`$（等分散で、互いに無相関） |
| (A3) | 階数 | $`X`$ の列が 1 次独立（$`\mathrm{rank}\,X = p`$） |
| (A4) | 正規性 | $`\varepsilon \sim N(0, \sigma^2 I_n)`$ |

$`X`$ は確率変数ではなく、決まった値として扱います。

### 2.3 どの出力にどの仮定が必要か

| 出力 | 必要な仮定 | 意味 |
|---|---|---|
| 係数 $`b`$ | (A3) | 計算できるための条件。不偏性 $`E[b] = \beta`$ には (A1) も必要 |
| $`R^2`$、$`\mathrm{SS_{reg}}`$、$`\mathrm{SS_{res}}`$ | (A3) | データを要約した量で、確率の仮定はいらない |
| $`s`$、標準誤差 | (A1)(A2)(A3) | $`s^2`$ が $`\sigma^2`$ の不偏推定量になり、標準誤差が係数のばらつきを表す |
| $`F`$、$`t`$、$`p`$ 値、信頼区間 | (A1)〜(A4) | 分布（$`F`$ 分布、$`t`$ 分布）を使うため正規性が必要 |

LINEST は仮定が成り立つかどうかを確かめずに、数値を計算して返します。仮定の確認は使う側の仕事です（9. を参照）。

---

## 3. 1 行目：回帰係数

**命題 1**　(A3) のもとで、残差平方和 $`S(b) = \lVert y - Xb \rVert^2`$ を最小にする $`b`$ はただ 1 つで、

$$
b = (X^\top X)^{-1} X^\top y
$$

である。

**証明**　$`S(b) = y^\top y - 2 b^\top X^\top y + b^\top X^\top X b`$ を $`b`$ で偏微分して 0 とおくと、

$$
\frac{\partial S}{\partial b} = -2 X^\top y + 2 X^\top X b = 0
\quad\Longleftrightarrow\quad
X^\top X b = X^\top y \qquad \text{（正規方程式）}
$$

となる。(A3) より $`X^\top X`$ は正定値で逆行列を持つので、$`b = (X^\top X)^{-1} X^\top y`$ がただ 1 つの解である。また $`S`$ のヘッセ行列 $`2X^\top X`$ が正定値なので、この点で最小になる。∎

**系（残差の直交性）**　正規方程式は $`X^\top r = X^\top (y - Xb) = 0`$ と同じである。つまり、残差は $`X`$ のすべての列と直交する。特に、1 の列があるので $`\sum_i r_i = 0`$ である。

**不偏性**　(A1) のもとで $`E[b] = (X^\top X)^{-1} X^\top E[y] = (X^\top X)^{-1} X^\top X \beta = \beta`$。

> **補足（幾何的な見方）**　$`\hat{y} = Xb`$ は、$`y`$ を $`X`$ の列が張る空間へ直交射影したものです。射影行列を
> $`P = X (X^\top X)^{-1} X^\top`$、残差を作る行列を $`R = I_n - P`$ とおくと、$`\hat{y} = Py`$、$`r = Ry`$ と書けます。

---

## 4. 3〜5 行目：残差・平方和・決定係数

### 4.1 平方和

$$
\mathrm{SS_{res}} = \sum_i r_i^2, \qquad
\mathrm{SS_{reg}} = \sum_i (\hat{y}_i - \bar{y})^2, \qquad
\mathrm{SS_{tot}} = \sum_i (y_i - \bar{y})^2
$$

**命題 2（平方和の分解）**　切片がある場合、$`\mathrm{SS_{tot}} = \mathrm{SS_{reg}} + \mathrm{SS_{res}}`$。

**証明**　$`y_i - \bar{y} = (\hat{y}_i - \bar{y}) + r_i`$ を 2 乗して和をとると、交差項は

$$
\sum_i (\hat{y}_i - \bar{y})\, r_i = b^\top X^\top r - \bar{y} \sum_i r_i = 0
$$

である（3. の系より $`X^\top r = 0`$、$`\sum_i r_i = 0`$）。∎

**例題で確認**：$`\bar{y} = 9.5`$ で、$`\mathrm{SS_{tot}} = 101.5 = 100.17 + 1.333`$。

### 4.2 決定係数（F4）

$$
R^2 = \frac{\mathrm{SS_{reg}}}{\mathrm{SS_{tot}}} = 1 - \frac{\mathrm{SS_{res}}}{\mathrm{SS_{tot}}}
$$

$`y`$ の平均まわりの変動のうち、回帰で説明できる割合です。説明変数を増やすと $`R^2`$ は下がりません。そのため、$`R^2`$ が大きいことだけでは、モデルがよいとは言えません。

### 4.3 残差の標準偏差 $`s`$（G4）

$$
s = \sqrt{\frac{\mathrm{SS_{res}}}{n - p}}
$$

**補題 3**　$`P`$ と $`R`$ は対称かつべき等で、$`\mathrm{tr}\,P = p`$、$`\mathrm{tr}\,R = n - p`$ である。

**証明**　対称性は定義から明らか。$`P^2 = X(X^\top X)^{-1} X^\top X (X^\top X)^{-1} X^\top = P`$、$`R^2 = I - 2P + P^2 = R`$。トレースは $`\mathrm{tr}(AB) = \mathrm{tr}(BA)`$ を使って
$`\mathrm{tr}\,P = \mathrm{tr}\big((X^\top X)^{-1} X^\top X\big) = \mathrm{tr}\,I_p = p`$。∎

**命題 4**　(A1)(A2)(A3) のもとで $`E[\mathrm{SS_{res}}] = (n - p)\sigma^2`$。したがって $`s^2`$ は $`\sigma^2`$ の不偏推定量である。

**証明**　$`RX = 0`$ より $`r = Ry = R(X\beta + \varepsilon) = R\varepsilon`$。$`R`$ は対称かつべき等なので $`\mathrm{SS_{res}} = \varepsilon^\top R^\top R \varepsilon = \varepsilon^\top R \varepsilon`$。スカラーはトレースに等しいので、

$$
E[\mathrm{SS_{res}}] = E[\mathrm{tr}(R\, \varepsilon \varepsilon^\top)] = \mathrm{tr}\big(R\, E[\varepsilon\varepsilon^\top]\big) = \sigma^2\, \mathrm{tr}\,R = (n - p)\sigma^2 \qquad ∎
$$

この証明は正規性 (A4) を使っていません。

> **補足**
> - $`n`$ ではなく $`n - p`$ で割るのは、$`p`$ 個のパラメータを合わせ込んだ分だけ残差が小さく出るからです。$`n - p`$ を **残差の自由度**（G5）と呼びます。
> - $`s^2`$ は $`\sigma^2`$ の不偏推定量ですが、$`s`$ 自体は $`\sigma`$ の不偏推定量ではありません（$`\sqrt{\ }`$ が凹関数なので、平均すると少し小さく出ます）。

---

## 5. 2 行目：標準誤差

**命題 5**　(A1)(A2)(A3) のもとで、

$$
\mathrm{Cov}(b) = \sigma^2 (X^\top X)^{-1}
$$

**証明**　$`b - \beta = (X^\top X)^{-1} X^\top \varepsilon`$。$`A = (X^\top X)^{-1} X^\top`$ とおくと、$`\mathrm{Cov}(A\varepsilon) = A\, \mathrm{Cov}(\varepsilon)\, A^\top = \sigma^2 A A^\top = \sigma^2 (X^\top X)^{-1}`$。∎

未知の $`\sigma^2`$ を $`s^2`$ で置き換え、対角成分の平方根をとったものが **標準誤差** です。

$$
\mathrm{SE}(b_j) = s \sqrt{\big[(X^\top X)^{-1}\big]_{jj}}
$$

- $`s`$ は、点が回帰式からどれだけばらつくかを表します。
- $`[(X^\top X)^{-1}]_{jj}`$ は $`X`$ だけで決まり、$`y`$ には依存しません。データ点が多いほど、$`x`$ の範囲が広いほど小さくなります。説明変数どうしの相関が強いと大きくなります（9.2）。

### 5.1 単回帰の場合

$`k = 1`$ のとき、$`S_{xx} = \sum_i (x_i - \bar{x})^2`$ とおくと、

$$
(X^\top X)^{-1} = \begin{bmatrix} n & \sum x_i \\ \sum x_i & \sum x_i^2 \end{bmatrix}^{-1}
= \frac{1}{n S_{xx}} \begin{bmatrix} \sum x_i^2 & -\sum x_i \\ -\sum x_i & n \end{bmatrix}
$$

なので、

$$
\mathrm{SE}(b_1) = \frac{s}{\sqrt{S_{xx}}}, \qquad
\mathrm{SE}(b_0) = s \sqrt{\frac{1}{n} + \frac{\bar{x}^2}{S_{xx}}}
$$

となります。教科書によく出てくる式は、この特別な場合です。

### 5.2 例題で確認

$$
(X^\top X)^{-1} = \frac{1}{192} \begin{bmatrix} 179 & -21 & -21 \\ -21 & 35 & -29 \\ -21 & -29 & 35 \end{bmatrix}
$$

（行と列の順は $`b_0, b_1, b_2`$）なので、

$$
\mathrm{SE}(b_1) = \frac{2}{3}\sqrt{\frac{35}{192}} = 0.2846, \qquad
\mathrm{SE}(b_0) = \frac{2}{3}\sqrt{\frac{179}{192}} = 0.6437
$$

となり、G3・H3 と一致します。

> **補足**　非対角成分は係数どうしの共分散です。たとえば $`\mathrm{Cov}(b_1, b_2)`$ の推定値は $`s^2 \times (-29/192)`$ で、負になります。$`x_1`$ と $`x_2`$ の相関が強いため、一方を大きく見積もると他方が小さく見積もられる関係にあります。
> 係数の和や差（たとえば $`b_1 - b_2`$）の標準誤差を求めるときは、この共分散も必要です。LINEST は共分散を出さないので、8. の行列計算で求めます。

### 5.3 二次関数で近似する場合（自由落下）

[自由落下の解説](自由落下_重力加速度推定_Excel解説.md) の 7.4 で使う式

$$
\text{C の標準誤差} = s \sqrt{k}
$$

は、$`y = A + Bx + Cx^2`$ に命題 5 を当てはめたものです。$`X`$ の列は $`1, x, x^2`$ で、$`k = [(X^\top X)^{-1}]_{CC}`$（$`x^2`$ の列に対応する対角成分）です。

**重みの 2 乗の合計との関係**　7.4 では $`k`$ を「C を求めるときに $`y_i`$ にかかる重みの 2 乗の合計」として計算しています。$`b = Ay`$、$`A = (X^\top X)^{-1} X^\top`$ とおくと、$`b_j = \sum_i A_{ji} y_i`$ なので、重みは $`A`$ の第 $`j`$ 行です。その 2 乗の合計は

$$
\sum_i A_{ji}^2 = \big[A A^\top\big]_{jj} = \big[(X^\top X)^{-1}\big]_{jj}
$$

となり、両者は同じ量です。

**例**　$`x = 1, \dots, 5`$ のとき、

$$
X^\top X = \begin{bmatrix} 5 & 15 & 55 \\ 15 & 55 & 225 \\ 55 & 225 & 979 \end{bmatrix}, \qquad
(X^\top X)^{-1} = \frac{1}{70} \begin{bmatrix} 322 & -231 & 35 \\ -231 & 187 & -30 \\ 35 & -30 & 5 \end{bmatrix}
$$

（行と列の順は $`A, B, C`$）なので $`k = 5/70 = 1/14`$ です。$`C`$ にかかる重みは $`A`$ の第 3 行 $`\frac{1}{70}(10, -5, -10, -5, 10)`$ で、2 乗の合計は $`\frac{350}{4900} = \frac{1}{14}`$ と一致します。7.4 の $`y = 2, 3, 6, 10, 16`$ では $`s = 0.1690`$ なので、

$$
\mathrm{SE}(C) = 0.1690\sqrt{\frac{5}{70}} = 0.0452, \quad
\mathrm{SE}(B) = 0.1690\sqrt{\frac{187}{70}} = 0.2763, \quad
\mathrm{SE}(A) = 0.1690\sqrt{\frac{322}{70}} = 0.3625
$$

となり、LINEST の 2 行目と一致します。

> **補足**　7.4 では $`u = x - 3`$ とずらして計算しています。$`(1, u, u^2)`$ は $`(1, x, x^2)`$ と同じ列空間を張り、$`x^2 = u^2 + 6u + 9`$ なので、$`x^2`$ の係数と $`u^2`$ の係数は一致します。したがって $`C`$ とその標準誤差は変わりません（実際、$`u`$ で計算した $`(X^\top X)^{-1}`$ の $`(C, C)`$ 成分も $`5/70`$ です）。$`u`$ を使うと $`\sum u = \sum u^3 = 0`$ となり、$`X^\top X`$ に 0 が増えて手計算が楽になります。

---

## 6. 4 行目：F 値と自由度

$$
F = \frac{\mathrm{SS_{reg}} / k}{\mathrm{SS_{res}} / (n - p)}
$$

帰無仮説 $`H_0: \beta_1 = \cdots = \beta_k = 0`$（切片以外の係数がすべて 0）を検定するための統計量です。(A1)〜(A4) と $`H_0`$ のもとで $`F \sim F(k,\, n - p)`$ に従います。

- G5 の自由度は $`n - p`$（`const` が `TRUE` なら $`n - k - 1`$）です。
- p 値は `=F.DIST.RT(F5, k, G5)` で求めます。例題では $`k = 2`$ で、p 値は 0.0015 です。
- $`R^2`$ との関係は $`F = \dfrac{R^2 / k}{(1 - R^2)/(n - p)}`$ です。

---

## 7. LINEST が出さないもの：t 値・p 値・信頼区間

### 7.1 計算式

係数ごとの検定と信頼区間は、LINEST の出力から次の式で求めます（例題の $`b_1`$、G 列の場合）。

| 量 | 式 | 例題の値 |
|---|---|---|
| t 値 | `=G2/G3` | 4.977 |
| p 値（両側） | `=T.DIST.2T(ABS(G2/G3), G5)` | 0.0156 |
| 95% 信頼区間の下限 | `=G2-T.INV.2T(0.05, G5)*G3` | 0.511 |
| 95% 信頼区間の上限 | `=G2+T.INV.2T(0.05, G5)*G3` | 2.323 |

自由度 3 の t 分布の両側 5% 点は 3.182 です。

### 7.2 なぜ t 分布か

**命題 6**　(A1)〜(A4) のもとで、

$$
T_j = \frac{b_j - \beta_j}{\mathrm{SE}(b_j)} \sim t(n - p)
$$

**証明の流れ**　次の 3 つを示せば、t 分布の定義（標準正規分布 ÷ $`\sqrt{\chi^2 / \text{自由度}}`$、ただし両者は独立）から結論が出る。

1. **分子は正規分布**　$`b - \beta = A\varepsilon`$ は正規ベクトルの線形変換なので、$`b \sim N\big(\beta,\ \sigma^2 (X^\top X)^{-1}\big)`$。したがって $`Z = (b_j - \beta_j) \big/ \big(\sigma \sqrt{[(X^\top X)^{-1}]_{jj}}\big) \sim N(0, 1)`$。
2. **分母は $`\chi^2`$ 分布**　$`R`$ は対称かつべき等で $`\mathrm{tr}\,R = n - p`$ だから、固有値は 1 が $`n - p`$ 個、0 が $`p`$ 個である。直交行列 $`Q`$ で $`R = Q\, \mathrm{diag}(I_{n-p}, 0)\, Q^\top`$ と対角化し、$`w = Q^\top \varepsilon / \sigma`$ とおくと、$`w \sim N(0, I_n)`$。したがって
   $$
   \frac{\mathrm{SS_{res}}}{\sigma^2} = \frac{\varepsilon^\top R\, \varepsilon}{\sigma^2} = \sum_{i=1}^{n-p} w_i^2 \sim \chi^2(n - p)
   $$
3. **分子と分母は独立**　$`b = Ay`$ と $`r = Ry`$ の相互共分散は
   $$
   A\, (\sigma^2 I)\, R^\top = \sigma^2 (X^\top X)^{-1} X^\top (I - P) = 0
   $$
   である（$`X^\top P = X^\top`$ を使った）。$`(b, r)`$ は同じ正規ベクトル $`y`$ の線形変換なので同時に正規分布に従い、相互共分散が 0 なら独立になる。$`\mathrm{SS_{res}}`$ は $`r`$ の関数なので、$`b`$ と独立である。

以上から $`T_j = Z \Big/ \sqrt{\dfrac{\mathrm{SS_{res}}/\sigma^2}{n - p}}`$ で、$`\sigma`$ は分子と分母で約分されて消える。∎

> **補足**
> - 3. の「相互共分散が 0 なら独立」は、残差の共分散 $`\sigma^2 R`$ が正則でなくても成り立ちます。$`(b, r)`$ の積率母関数が、相互共分散の項が消えることで $`b`$ の分と $`r`$ の分の積に分解されるからです。
> - 真の $`\sigma`$ の代わりに推定値 $`s`$ を使うため、分布は正規分布ではなく t 分布になります。$`n - p`$ が大きいと、t 分布は正規分布に近づきます。

---

## 8. 行列計算で LINEST を再現する

1.3 の例題で、A 列の 1 を含めた A2:C7 を計画行列 $`X`$ にします。

| 求めるもの | 範囲 | 式 |
|---|---|---|
| $`(X^\top X)^{-1}`$ | F9:H11 | `=MINVERSE(MMULT(TRANSPOSE(A2:C7), A2:C7))` |
| $`b = (X^\top X)^{-1} X^\top y`$ | J9:J11 | `=MMULT(F9:H11, MMULT(TRANSPOSE(A2:C7), D2:D7))` |
| $`\mathrm{SE}(b_0)`$ | K9 | `=G4*SQRT(INDEX(F9:H11, 1, 1))` |
| $`\mathrm{SE}(b_1)`$ | K10 | `=G4*SQRT(INDEX(F9:H11, 2, 2))` |
| $`\mathrm{SE}(b_2)`$ | K11 | `=G4*SQRT(INDEX(F9:H11, 3, 3))` |
| 係数の共分散行列 $`s^2 (X^\top X)^{-1}`$ | F13:H15 | `=G4^2*F9:H11` |

- 古い Excel では、範囲を選んでから **Ctrl + Shift + Enter** で確定します。
- J9:J11 は上から $`b_0, b_1, b_2`$ の順です。LINEST の 1 行目とは逆の順になります。
- $`s`$（G4）も自分で求めるなら `=SQRT(SUMXMY2(D2:D7, MMULT(A2:C7, J9:J11))/(ROWS(D2:D7)-COLUMNS(A2:C7)))` です。

---

## 9. 使うときの注意

### 9.1 `const` を `FALSE` にしたとき

- 切片を 0 に固定するので、$`p = k`$ になり、自由度は $`n - k`$ です。
- 命題 2 の分解が平均まわりでは成り立たなくなるため、Excel は全平方和を **原点まわり**（$`\mathrm{SS_{tot}} = \sum_i y_i^2`$）で計算し、$`\mathrm{SS_{reg}} = \mathrm{SS_{tot}} - \mathrm{SS_{res}}`$、$`R^2 = \mathrm{SS_{reg}} / \mathrm{SS_{tot}}`$ とします。切片ありのモデルの $`R^2`$ とは比べられません。
- 切片の標準誤差（2 行目の右端）は #N/A になります。

### 9.2 説明変数どうしの相関が強いとき（多重共線性）

- $`X^\top X`$ が特異に近くなり、$`[(X^\top X)^{-1}]_{jj}`$ が大きくなります。そのため、標準誤差も大きくなります。
- 完全に 1 次従属な列があると、Excel はその列を除き、係数と標準誤差を 0 と表示します。除いた列 1 つにつき自由度が 1 増え、$`s`$ と $`F`$ もそれに合わせて変わります。係数 0 が「推定した結果 0」なのか「除かれた」のかに注意してください。

### 9.3 標準誤差が意味を持つ条件

- 標準誤差は「(A1)(A2) が正しいとき、同じ $`X`$ で実験をくり返したら $`b_j`$ がどれだけばらつくか」の推定値です。
- モデルの形が違う（A1 が成り立たない）と、残差に系統的な傾向が出ます。標準誤差は、そのずれを誤差として正しく表しません。**残差を $`\hat{y}`$ や各 $`x_j`$ に対してプロットして、パターンがないことを確認してください。**
- 誤差の大きさが $`x`$ によって変わる（A2 が成り立たない）場合や、時系列で誤差が相関している場合も、標準誤差は信頼できません。重み付き最小二乗法など、別の方法が必要です。
- 測定器の目盛りのずれのように、すべての点に同じ向きにかかる誤差（系統誤差）は、残差に現れないので標準誤差に含まれません。

### 9.4 その他

- `stats` を `FALSE` にすると、1 行目だけが出ます。
- 3〜5 行目の 3 列目以降の #N/A は、仕様どおりの表示です。

---

## 10. 参考資料

- Microsoft サポート「[LINEST 関数](https://support.microsoft.com/ja-jp/excel/functions/linest-function)」：出力の配置、`const = FALSE` の扱い、多重共線性の扱い
- Real Statistics「[Multiple Regression Analysis in Excel](https://real-statistics.com/multiple-regression/multiple-regression-analysis/multiple-regression-analysis-excel/)」：MMULT・MINVERSE による再現
- Real Statistics「[Multiple Regression using Matrices](https://real-statistics.com/multiple-regression/multiple-regression-analysis/multiple-regression-using-matrices/)」：行列による定式化
- The Book of Statistical Proofs（各命題の証明）
  - [mlr-ols](https://statproofbook.github.io/P/mlr-ols)：命題 1
  - [mlr-idem](https://statproofbook.github.io/P/mlr-idem)：補題 3
  - [mlr-olsdist](https://statproofbook.github.io/P/mlr-olsdist)：命題 5、7.2 の 1.
  - [mlr-rssdist](https://statproofbook.github.io/P/mlr-rssdist)：7.2 の 2.
  - [mlr-ind](https://statproofbook.github.io/P/mlr-ind)、[mvn-indprod](https://statproofbook.github.io/P/mvn-indprod)：7.2 の 3.
  - [mlr-t](https://statproofbook.github.io/P/mlr-t)：命題 6
