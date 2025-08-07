import plotly.graph_objects as go
import numpy as np
from scipy.signal import convolve2d
from skimage import data
from skimage.color import rgb2gray
import plotly.io as pio

pio.renderers.default = "notebook"

def create_convolution_animation():
    """
    Creates an interactive animation to demonstrate the convolution operation.
    Saves the animation as an HTML file.
    """
    # Load a sample image and convert to grayscale
    image = data.camera()
    image = image[::2, ::2]  # Downsample for speed
    img_height, img_width = image.shape

    # Define some common kernels
    kernels = {
        "Identity": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        "Edge Detection": np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]),
        "Sharpen": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
        "Box Blur": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9.0,
    }

    fig = go.Figure()

    # Create initial traces for image and feature map
    fig.add_trace(go.Heatmap(z=image, colorscale='gray', showscale=False, name='Input Image'))
    
    # Add traces for each kernel's feature map, initially invisible
    for name, kernel in kernels.items():
        feature_map = convolve2d(image, kernel, mode='same', boundary='symm')
        fig.add_trace(go.Heatmap(z=feature_map, colorscale='gray', showscale=False, visible=False, name=name))
        
    # Create buttons to switch between kernels
    buttons = []
    for i, name in enumerate(kernels.keys()):
        visibility = [False] * (len(kernels) + 1)
        visibility[0] = True  # Keep original image visible
        visibility[i + 1] = True # Make the selected feature map visible
        
        button = dict(
            label=name,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"Feature Map (Kernel: {name})"}])
        buttons.append(button)

    fig.update_layout(
        title_text="Convolution Demo: Select a Kernel",
        updatemenus=[
            dict(
                active=0,
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ],
        xaxis=dict(title="Input Image", domain=[0, 0.45]),
        xaxis2=dict(title="Feature Map", domain=[0.55, 1.0]),
        yaxis=dict(scaleanchor="x"),
        yaxis2=dict(scaleanchor="x2"),
        annotations=[
            dict(text="Kernel Type:", showarrow=False,
                 x=0, y=1.08, yref="paper", align="left")
        ]
    )
    
    # The second heatmap needs to be explicitly linked to the second x/y axes
    for i in range(1, len(kernels) + 1):
        fig.data[i].update(xaxis='x2', yaxis='y2')
        
    # Set initial state
    fig.data[1].visible = True
    fig.update_layout(title_text="Feature Map (Kernel: Identity)")

    fig.write_html("book/assets/ch11/convolution_animation.html", include_plotlyjs='cdn')
    print("Convolution animation saved to book/assets/ch11/convolution_animation.html")


def create_maxpooling_animation():
    """
    Creates an interactive animation to demonstrate the max pooling operation.
    Saves the animation as an HTML file.
    """
    # Create a sample 4x4 feature map
    z = np.array([
        [5, 8, 1, 3],
        [6, 2, 7, 4],
        [9, 5, 3, 2],
        [4, 6, 8, 1]
    ])
    
    pooled_z = np.array([
        [8, 7],
        [9, 8]
    ])

    fig = go.Figure()

    # Input feature map
    fig.add_trace(go.Heatmap(
        z=z,
        colorscale='Viridis',
        showscale=False,
        text=z,
        texttemplate="%{text}",
        name='Input Feature Map'
    ))

    # Pooled feature map
    fig.add_trace(go.Heatmap(
        z=pooled_z,
        colorscale='Viridis',
        showscale=False,
        text=pooled_z,
        texttemplate="%{text}",
        xaxis='x2',
        yaxis='y2',
        name='Pooled Map'
    ))
    
    # Create frames for animation
    frames = []
    steps = [
        (0, 0, 0, 0, 8), (0, 2, 0, 1, 7),
        (2, 0, 1, 0, 9), (2, 2, 1, 1, 8)
    ]
    for i, (r_start, c_start, pr, pc, val) in enumerate(steps):
        frame = go.Frame(
            name=f"frame{i}",
            layout=go.Layout(
                shapes=[
                    # Highlight rectangle on input map
                    go.layout.Shape(
                        type="rect",
                        x0=c_start - 0.5, y0=r_start - 0.5,
                        x1=c_start + 1.5, y1=r_start + 1.5,
                        line=dict(color="red", width=4)
                    ),
                    # Highlight cell on pooled map
                    go.layout.Shape(
                        type="rect",
                        xref="x2", yref="y2",
                        x0=pc - 0.5, y0=pr - 0.5,
                        x1=pc + 0.5, y1=pr + 0.5,
                        line=dict(color="lime", width=4)
                    )
                ]
            )
        )
        frames.append(frame)

    fig.frames = frames

    # Create slider
    sliders = [dict(
        steps=[
            dict(method='animate', args=[[f'frame{i}'], dict(mode='immediate', frame=dict(duration=500, redraw=True), transition=dict(duration=0))]),
        ] * len(steps),
        transition=dict(duration=0),
        x=0.1,
        xanchor="left",
        len=0.9,
    )]
    
    # Create play button
    updatemenus = [dict(
        type='buttons',
        showactive=False,
        buttons=[dict(
            label='Play',
            method='animate',
            args=[None, dict(frame=dict(duration=1000, redraw=True), fromcurrent=True, transition=dict(duration=0))]
        ), dict(
            label='Pause',
            method='animate',
            args=[[None], dict(mode='immediate', frame=dict(duration=0, redraw=False), transition=dict(duration=0))]
        )]
    )]
    
    fig.update_layout(
        title="Max Pooling (2x2 Pool with Stride 2)",
        xaxis=dict(title="Input Feature Map", domain=[0, 0.6]),
        yaxis=dict(autorange='reversed'),
        xaxis2=dict(title="Pooled Map", domain=[0.7, 1.0]),
        yaxis2=dict(autorange='reversed', scaleanchor='x2'),
        updatemenus=updatemenus,
        # sliders=sliders # The slider is a bit clunky for this simple case
    )
    
    # Set initial state with the first highlight
    fig.update_layout(shapes=fig.frames[0].layout.shapes)

    fig.write_html("book/assets/ch11/maxpooling_animation.html", include_plotlyjs='cdn')
    print("Max pooling animation saved to book/assets/ch11/maxpooling_animation.html")

if __name__ == '__main__':
    create_convolution_animation()
    create_maxpooling_animation()

