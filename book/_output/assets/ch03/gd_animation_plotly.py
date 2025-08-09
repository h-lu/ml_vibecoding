"""
Generate a pre-rendered Plotly HTML animation that illustrates Gradient Descent
on y = x^2 with a fixed learning rate. The output is saved as 'gd_animation.html'
under the same directory. This HTML can be embedded in Quarto via an <iframe>.

Usage:
  python gd_animation_plotly.py

Dependencies:
  - plotly>=5
  - numpy
"""

from __future__ import annotations

import os
from pathlib import Path
import numpy as np
import plotly.graph_objects as go


def compute_gd_path(
    initial_x: float = -4.0,
    learning_rate: float = 0.2,
    num_steps: int = 30,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute the x and y path for gradient descent on y=x^2.

    y(x) = x^2, dy/dx = 2x
    x_{t+1} = x_t - lr * 2x_t = x_t * (1 - 2*lr)
    """
    xs = [initial_x]
    for _ in range(num_steps):
        xs.append(xs[-1] - learning_rate * 2.0 * xs[-1])
    xs_arr = np.array(xs)
    ys_arr = xs_arr**2
    return xs_arr, ys_arr


def build_figure(
    initial_x: float = -4.0,
    learning_rate: float = 0.2,
    num_steps: int = 30,
) -> go.Figure:
    # Domain for function curve
    x_domain = np.linspace(-5, 5, 400)
    y_domain = x_domain**2

    # GD path
    x_path, y_path = compute_gd_path(initial_x, learning_rate, num_steps)

    # Base traces
    curve_trace = go.Scatter(
        x=x_domain,
        y=y_domain,
        mode="lines",
        name="y = x^2",
        line=dict(color="#1f77b4", width=2),
    )

    point_trace = go.Scatter(
        x=[x_path[0]],
        y=[y_path[0]],
        mode="markers",
        name="当前点",
        marker=dict(color="crimson", size=10),
        showlegend=True,
    )

    path_trace = go.Scatter(
        x=[x_path[0]],
        y=[y_path[0]],
        mode="lines",
        name="轨迹",
        line=dict(color="crimson", width=2, dash="dot"),
        showlegend=True,
    )

    # Frames for animation
    frames = []
    for i in range(1, len(x_path)):
        frames.append(
            go.Frame(
                data=[
                    curve_trace,
                    go.Scatter(x=[x_path[i]], y=[y_path[i]], mode="markers", marker=dict(color="crimson", size=10)),
                    go.Scatter(x=x_path[: i + 1], y=y_path[: i + 1], mode="lines", line=dict(color="crimson", width=2, dash="dot")),
                ],
                name=f"step_{i}",
                traces=[0, 1, 2],
                layout=go.Layout(
                    title=dict(
                        text=f"梯度下降示意 (学习率={learning_rate}, 步数={i}/{len(x_path)-1})",
                        x=0.5,
                    )
                ),
            )
        )

    fig = go.Figure(
        data=[curve_trace, point_trace, path_trace],
        frames=frames,
    )

    fig.update_layout(
        title=dict(text=f"梯度下降示意 (学习率={learning_rate}, 初始点={initial_x})", x=0.5),
        xaxis_title="x（模型参数）",
        yaxis_title="y / 损失（Loss）",
        width=800,
        height=500,
        template="plotly_white",
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.05,
                y=1.12,
                xanchor="left",
                buttons=[
                    dict(
                        label="播放",
                        method="animate",
                        args=[None, {"frame": {"duration": 300, "redraw": True}, "fromcurrent": True, "mode": "immediate"}],
                    ),
                    dict(
                        label="暂停",
                        method="animate",
                        args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    ),
                ],
            )
        ],
    )

    # Fix axis ranges for consistent view
    fig.update_xaxes(range=[-5, 5])
    fig.update_yaxes(range=[0, 26])
    return fig


def main() -> None:
    fig = build_figure(initial_x=-4.0, learning_rate=0.2, num_steps=30)
    out_dir = Path(__file__).parent
    out_file = out_dir / "gd_animation.html"
    fig.write_html(str(out_file), include_plotlyjs="cdn", full_html=True)
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    # Ensure working directory does not affect output path
    os.chdir(Path(__file__).parent)
    main()


