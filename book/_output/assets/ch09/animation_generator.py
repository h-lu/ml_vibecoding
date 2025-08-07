import plotly.graph_objects as go
import numpy as np
from sklearn.datasets import make_moons
import plotly.io as pio

pio.renderers.default = "notebook"

def create_linear_inseparable_animation():
    """
    Creates an interactive animation showing that a linear model
    cannot solve a non-linear problem (moons dataset).
    Saves the animation as an HTML file.
    """
    # 1. Generate non-linear data
    X, y = make_moons(n_samples=200, noise=0.1, random_state=42)

    # 2. Create the main figure
    fig = go.Figure()

    # Add scatter plot of the moons data
    fig.add_trace(go.Scatter(
        x=X[y==0, 0], y=X[y==0, 1],
        mode='markers',
        marker=dict(color='blue', symbol='circle'),
        name='类别 0'
    ))
    fig.add_trace(go.Scatter(
        x=X[y==1, 0], y=X[y==1, 1],
        mode='markers',
        marker=dict(color='red', symbol='square'),
        name='类别 1'
    ))

    # 3. Add a placeholder for the decision boundary line
    fig.add_trace(go.Scatter(
        x=[-2, 3], y=[0, 0], # Initial horizontal line
        mode='lines',
        line=dict(color='green', width=3, dash='dash'),
        name='线性决策边界'
    ))

    # 4. Create frames for the animation
    frames = []
    angles = np.linspace(0, np.pi, 60) # Rotate the line over 180 degrees

    for i, angle in enumerate(angles):
        # Calculate line parameters for the current angle
        # A line is defined by normal vector (cos(a), sin(a)) and passes through the mean point
        mean_point = X.mean(axis=0)
        normal_vector = np.array([np.cos(angle), np.sin(angle)])
        
        # Line equation: normal_vector[0]*x + normal_vector[1]*y - np.dot(normal_vector, mean_point) = 0
        # We need to find two points on this line to draw it.
        x_vals = np.array([-2, 3])
        # Avoid division by zero if the line is vertical
        if np.abs(normal_vector[1]) > 1e-6:
            y_vals = (np.dot(normal_vector, mean_point) - normal_vector[0] * x_vals) / normal_vector[1]
        else: # Handle vertical line
            x_vals = np.array([mean_point[0], mean_point[0]])
            y_vals = np.array([-1.5, 1.5])
            
        frame_data = [
            go.Scatter(x=x_vals, y=y_vals) # Update only the line trace
        ]
        frames.append(go.Frame(
            data=frame_data,
            name=str(i),
            traces=[2] # Update the 3rd trace (index 2)
        ))

    fig.frames = frames

    # 5. Add slider and buttons
    sliders = [
        {
            "steps": [
                {
                    "args": [[str(i)], {"frame": {"duration": 50, "redraw": True}, "mode": "immediate"}],
                    "label": f"{int(np.rad2deg(angles[i]))}°",
                    "method": "animate",
                }
                for i in range(len(angles))
            ],
            "transition": {"duration": 30},
            "x": 0.1, "len": 0.9,
            "currentvalue": {"font": {"size": 15}, "prefix": "决策边界旋转角度: ", "visible": True, "xanchor": "right"},
        }
    ]

    updatemenus = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True, "transition": {"duration": 30, "easing": "linear"}}],
                    "label": "播放",
                    "method": "animate",
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}],
                    "label": "暂停",
                    "method": "animate",
                },
            ],
            "direction": "left", "pad": {"r": 10, "t": 87}, "showactive": False,
            "type": "buttons", "x": 0.1, "xanchor": "right", "y": 0, "yanchor": "top",
        }
    ]

    # 6. Update layout
    fig.update_layout(
        title="线性模型的困境：无法分离非线性数据",
        xaxis_title="特征 1",
        yaxis_title="特征 2",
        xaxis=dict(range=[-2, 3], zeroline=False),
        yaxis=dict(range=[-1.5, 1.5], zeroline=False),
        height=600,
        width=800,
        sliders=sliders,
        updatemenus=updatemenus,
        legend=dict(x=0, y=1.1, orientation='h'),
        annotations=[
            dict(
                text="无论直线如何旋转，都无法找到一条能完美分开红色和蓝色数据点的边界。",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=-0.15,
                font=dict(size=14)
            )
        ]
    )

    fig.write_html("book/assets/ch09/linear_inseparable.html", auto_play=False)
    print("Animation saved to book/assets/ch09/linear_inseparable.html")

if __name__ == "__main__":
    create_linear_inseparable_animation()
