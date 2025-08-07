#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVM：硬间隔 vs. 软间隔（C 权衡）— 交互式可视化（scikit-learn + Plotly）
运行本脚本将生成单文件、离线可用的 HTML：svm_hard_soft_margin_C_demo.html
将该 HTML 放入你的 Quarto 项目（如 assets/ch06/）后，可用 <iframe> 嵌入。
"""

import numpy as np
import plotly.graph_objects as go

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

# ------------------------- 可调参数 -------------------------
RANDOM_SEED       = 20250802     # 固定随机种子，保证课堂可复现
N_PER_CLASS       = 90           # 每类样本数（基础点）
DATA_NOISE_RATE   = 0.03         # 全局标签噪声比例（0~1）
AMB_POINTS        = 20           # 近边界样本数量（融入两类，不单独成图例）
AMB_NORMAL_WIDTH  = 0.22         # 近边界样本：沿法线偏移的带宽（越大越模糊）
AMB_TANGENT_SPAN  = 0.45         # 近边界样本：沿切线方向的分布范围
AMB_FLIP_PROB     = 0.35         # 近边界样本：标签翻转概率（制造高C可见位移）

# C 值网格（离散步进；可自行增删）
C_VALUES = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0]

# 绘图范围
X_MIN, X_MAX = 0.3, 3.3
Y_MIN, Y_MAX = 0.2, 3.1

# 输出文件名
OUT_HTML = "svm_hard_soft_margin_C_demo.html"


# ------------------------- 数据生成 -------------------------
def make_data(seed=RANDOM_SEED):
    np.random.seed(seed)

    # 两个轻微重叠的高斯簇
    mean_pos = np.array([2.2, 2.1])
    cov_pos  = np.array([[0.16, 0.06],[0.06, 0.16]])

    mean_neg = np.array([1.2, 1.1])
    cov_neg  = np.array([[0.16, 0.05],[0.05, 0.16]])

    X_pos = np.random.multivariate_normal(mean_pos, cov_pos, N_PER_CLASS)
    X_neg = np.random.multivariate_normal(mean_neg, cov_neg, N_PER_CLASS)

    y_pos = np.ones(len(X_pos), dtype=int)
    y_neg = -np.ones(len(X_neg), dtype=int)

    X = np.vstack([X_pos, X_neg])
    y = np.concatenate([y_pos, y_neg])

    # 全局少量标签噪声
    n_flip = int(DATA_NOISE_RATE * len(y))
    if n_flip > 0:
        flip_idx = np.random.choice(len(y), size=n_flip, replace=False)
        y = y.copy()
        y[flip_idx] *= -1

    # 近边界模糊带样本（直接融入两类，不单独成图例）
    # 用类中心差向量近似分割方向
    w_dir = mean_pos - mean_neg
    wn = w_dir / (np.linalg.norm(w_dir) + 1e-12)
    mid = 0.5 * (mean_pos + mean_neg)
    t_dir = np.array([-wn[1], wn[0]])  # 与法线正交的切线方向

    amb_points = []
    amb_labels = []
    for _ in range(AMB_POINTS):
        s_n = np.random.uniform(-AMB_NORMAL_WIDTH, AMB_NORMAL_WIDTH)  # 法线方向轻微偏移
        s_t = np.random.uniform(-AMB_TANGENT_SPAN, AMB_TANGENT_SPAN)  # 切线方向铺开
        x = mid + s_n*wn + s_t*t_dir
        # 以 mid 为界的符号决定初始标签，再按概率翻转
        base_label = 1 if np.dot(wn, x - mid) >= 0 else -1
        if np.random.rand() < AMB_FLIP_PROB:
            base_label *= -1
        amb_points.append(x)
        amb_labels.append(base_label)

    if len(amb_points) > 0:
        X = np.vstack([X, np.vstack(amb_points)])
        y = np.concatenate([y, np.array(amb_labels, dtype=int)])

    return X, y


# ------------------------- 训练并提取边界 -------------------------
def train_linear_svc_sequence(X, y, C_values):
    """对一组 C 训练 LinearSVC（带标准化），并返回在原始特征空间的 (w, b)"""
    solutions = []
    for C in C_values:
        pipe = make_pipeline(
            StandardScaler(with_mean=True, with_std=True),
            LinearSVC(C=C, loss="hinge", fit_intercept=True, tol=1e-6,
                      max_iter=200000, dual=True, random_state=42)
        )
        pipe.fit(X, y)
        scaler = pipe.named_steps["standardscaler"]
        clf = pipe.named_steps["linearsvc"]

        # 从标准化空间恢复到原始空间：
        # z = (x - mu)/sigma, f = wz·z + b = (wz/sigma)·x + (b - wz·(mu/sigma))
        wz = clf.coef_.ravel()
        bz = float(clf.intercept_[0])
        sigma = scaler.scale_
        mu = scaler.mean_
        w_eff = wz / sigma
        b_eff = bz - np.dot(wz, mu / sigma)

        f = X @ w_eff + b_eff
        pred = np.where(f >= 0, 1, -1)
        mis_idx = np.where(pred != y)[0]

        solutions.append((C, w_eff, b_eff, mis_idx))
    return solutions


# ------------------------- 可视化 -------------------------
def line_xy_from_wb(w, b, level, x_range=(X_MIN, X_MAX), y_range=(Y_MIN, Y_MAX), npts=600):
    xs = np.linspace(x_range[0], x_range[1], npts)
    if abs(w[1]) > 1e-12:
        ys = (level - b - w[0]*xs) / w[1]
        mask = (ys >= y_range[0]-0.5) & (ys <= y_range[1]+0.5)
        return xs[mask], ys[mask]
    else:
        x_const = np.full(npts, (level - b) / (w[0] + 1e-12))
        ys = np.linspace(y_range[0], y_range[1], npts)
        mask = (x_const >= x_range[0]-0.5) & (x_const <= x_range[1]+0.5)
        return x_const[mask], ys[mask]

def margin_width(w):
    nrm = np.linalg.norm(w)
    return (2.0 / nrm) if nrm > 1e-12 else np.inf

def build_figure(X, y, solutions):
    # 拆分两类用于散点
    X_pos = X[y== 1]; X_neg = X[y==-1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_pos[:,0], y=X_pos[:,1], mode="markers",
                             name="正类 (+1)", marker=dict(size=7, opacity=0.9)))
    fig.add_trace(go.Scatter(x=X_neg[:,0], y=X_neg[:,1], mode="markers",
                             name="负类 (-1)", marker=dict(size=7, opacity=0.9)))

    # 占位：决策线、两条间隔线、误分类点
    fig.add_trace(go.Scatter(x=[], y=[], mode="lines",
                             name="决策边界 f(x)=0", line=dict(width=3)))
    fig.add_trace(go.Scatter(x=[], y=[], mode="lines",
                             name="间隔线 f(x)=+1", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=[], y=[], mode="lines",
                             name="间隔线 f(x)=-1", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=[], y=[], mode="markers",
                             name="误分类点", marker=dict(symbol="x", size=12, line=dict(width=2))))

    fig.update_xaxes(range=[X_MIN, X_MAX], title="特征 1")
    fig.update_yaxes(range=[Y_MIN, Y_MAX], title="特征 2")

    # 动画帧
    frames = []
    for (C, w, b, mis_idx) in solutions:
        xb, yb = line_xy_from_wb(w, b, level=0.0)
        x1, y1 = line_xy_from_wb(w, b, level=+1.0)
        x2, y2 = line_xy_from_wb(w, b, level=-1.0)
        title = f"C={C:g} | 间隔≈{margin_width(w):.2f} | 误分类={len(mis_idx)}"
        frames.append(go.Frame(
            name=f"C={C:g}",
            data=[go.Scatter(x=xb, y=yb),
                  go.Scatter(x=x1, y=y1),
                  go.Scatter(x=x2, y=y2),
                  go.Scatter(x=X[mis_idx,0], y=X[mis_idx,1])],
            traces=[2,3,4,5],
            layout=go.Layout(title_text=title)
        ))
    fig.frames = frames

    # 控件：下移避免与图例冲突
    steps = [dict(method="animate",
                  args=[[f"C={C:g}"],
                        dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))],
                  label=f"{C:g}") for (C, *_rest) in solutions]
    slider = dict(active=2, currentvalue={"prefix":"C："},
                  pad={"t": 40}, steps=steps, x=0.10, xanchor="left",
                  y=-0.34, yanchor="top", len=0.72)
    play_button = dict(label="▶ 播放（从小到大）", method="animate",
                       args=[[f"C={C:g}" for (C, *_rest) in solutions],
                             dict(frame=dict(duration=700, redraw=True), transition=dict(duration=0), mode="immediate")])

    fig.update_layout(
        title="硬间隔 vs. 软间隔（LinearSVC，扩展 C 至 1000）",
        sliders=[slider],
        updatemenus=[dict(type="buttons", direction="right", buttons=[play_button],
                          x=0.10, y=-0.42, xanchor="left", yanchor="top", showactive=False, pad={"t":8})],
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.20, yanchor="top"),
        margin=dict(l=70, r=40, t=80, b=240),
        height=620
    )

    # 初始帧（例如 C=0.3）
    init_w, init_b, init_mis = solutions[2][1], solutions[2][2], solutions[2][3]
    xb, yb = line_xy_from_wb(init_w, init_b, level=0.0)
    x1, y1 = line_xy_from_wb(init_w, init_b, level=+1.0)
    x2, y2 = line_xy_from_wb(init_w, init_b, level=-1.0)
    fig.data[2].x, fig.data[2].y = xb, yb
    fig.data[3].x, fig.data[3].y = x1, y1
    fig.data[4].x, fig.data[4].y = x2, y2
    fig.data[5].x, fig.data[5].y = (X[init_mis,0] if len(init_mis)>0 else []), (X[init_mis,1] if len(init_mis)>0 else [])
    fig.update_layout(title=(f"C=0.3 | 间隔≈{margin_width(init_w):.2f} | 误分类={len(init_mis)}"))

    return fig


def main():
    X, y = make_data()
    solutions = train_linear_svc_sequence(X, y, C_VALUES)
    fig = build_figure(X, y, solutions)
    fig.write_html(OUT_HTML, include_plotlyjs=True, full_html=True)
    print(f"✔ 已生成：{OUT_HTML}")


if __name__ == "__main__":
    main()
