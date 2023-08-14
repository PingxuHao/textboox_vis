import plotly.graph_objects as go
import numpy as np
import plotly.offline as pyo

t = np.linspace(0, 10, 50)
x, y, z = np.cos(t), np.sin(t), t

fig2 = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z,
                                   mode='markers')])
fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0))
pyo.plot(fig2, filename='myplot_small_1.html', auto_open=False, auto_play=False, config = {'displayModeBar': False} )