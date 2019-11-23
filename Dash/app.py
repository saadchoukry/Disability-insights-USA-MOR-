import dash
import dash_core_components as dcc
import dash_html_components as html
#from ETL.ETL_HCP04 import loader

dataFrames= None
def ETL():
    global dataFrames
    if dataFrames == None:
        print("------RUNNING ETL------")
        dataFrames = loader.EtlHcp04()
    else:
        return dataFrames
    



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    #ETL()
    app.run_server(debug=True)