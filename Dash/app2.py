import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from ETL.ETL_USA.usaLoader import UsaLoader as loader
from pandasTesting import dfs_sum

init= False
ETL = None

def ETLUSA():
    global init,ETL
    if not init :
        print("--- RUNNING ETL ---")
        ETL = loader()

    else:
        print("Data has already been loaded")
        return ETL
ETLUSA()



###Dash CONFIG
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout=html.Div([
    html.Div([
        dcc.Dropdown(
            id="sexe",
            options=[],
            value=[],
            clearable=False,
            multi =True,
            placeholder="Sexe",
            style={'width':'50vw','display': 'inline-block'}
            ,className="two columns")
            ],
    )
]
)






if __name__ == '__main__':
    
    app.run_server(debug=True)