import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import numpy as np

# starting values with 11 data points
X = [0,1,2,3,4,5,6,7,8,9,10]
Y = [0,0,0,0,0,0,0,0,0,0,0]

# define the app
app = dash.Dash(__name__)
  
# define the first html block
app.layout = html.Div(
    [
        # contain a graph with a periodic call back thanks to interval
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 1000,
            n_intervals = 0
        ),
    ]
)

# the callback updates the graph
@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)

# the function to update the graph
def update_graph(n):
    
    # add 1 to the x axis
    X.append(X[-1]+1)
    
    # the next y value is a random normal
    Y.append( np.random.normal(0,2))
    
    # define the data for the plot
    data = plotly.graph_objs.Scatter(
            
            # always plot the last 10 values of x and y
            x=list(X[-10:]),
            y=list(Y[-10:]),
            name='Scatter',
            mode= 'lines+markers'
    )
    
    # recompute the x range based on the last 10 points
    x_range = [min(X[-10:]),max(X[-10:])]
    
    # recompute y range for overall min and max of y
    y_range = [min(Y),max(Y)]
  
    # return the plot dictionary
    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=x_range),yaxis = dict(range = y_range),)}

if __name__ == '__main__':
    app.run_server()
