import plotly.graph_objs as go
import plotly
from plotly.graph_objs import Scatter, Layout

from datetime import datetime
import pandas_datareader.data as web
import pandas as pd

df = pd.read_csv("../input/test_serie.csv")

# data = [go.Scatter(
#           x=df.Date,
#           y=df['AAPL.Close'])]
#
# py.iplot(data)

plotly.offline.plot({
    "data": [Scatter(x=df.Date,y=df['AAPL.Close'])],
    "layout": Layout(title="hello world")
})

