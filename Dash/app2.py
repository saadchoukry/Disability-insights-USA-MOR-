import dash
import dash_core_components as dcc
import dash_html_components as html
from ETL.loader import EtlHcp04 
from dash.dependencies import Input, Output
import plotly.graph_objs as go

init= False
dfs = None
ageSexe04= None
sexeMatri04 = None
def ETL():
    global init,dfs,ageSexe04,categToAgeCateg,sexeMatri04
    if not init :
        print("--- RUNNING ETL ---")
        ETL = EtlHcp04()
        ageSexe04 = ETL.extendedDataFrames[0]
        sexeMatri04 = ETL.extendedDataFrames[1]
    else:
        print("Data has already been loaded")
        return dfs
ETL()
categToAgeCateg = {ageSexe04["AllTypes"].df.index.values.tolist().index(categ): '{}'.format(categ) for categ in ageSexe04["AllTypes"].df.index.values.tolist()}



###Dash CONFIG
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout=html.Div([
    ## Filters' Div
    html.Div([
        html.Div(dcc.Dropdown(
            id="sexe",
            options=[{"label":"Masculin","value":"Masculin"},{"label":"Féminin","value":"Féminin"},{"label":"Ensemble","value":"Ensemble"}],
            value="Ensemble",
            clearable=False,
            ),className="two columns"),
        html.Div(dcc.Dropdown(
            id="matri",
            options=[{"label":matri,"value":matri} for matri in sexeMatri04["AllTypes"].df.index],
            value=["Célibataire","Marié"],
            multi=True,
            clearable=False,
            placeholder="Statut matrimonial",
            style={'width':'24vw','display': 'inline-block'}
            ),
            className="four columns",),
        html.Div(dcc.Dropdown(
            id="disType",
            options=[{"label":disType,"value":disType} for disType in list(sexeMatri04.keys())[1:]],
            value=["Sensoriel","Chronique"],
            multi=True,
            clearable=False,
            placeholder="Type d'handicap",
            style={'width':'26vw','display': 'inline-block'}
            ),
            className="four columns",)
        
        
    ],className="row"),
    
    
    ## Figures' Div
    html.Div([
        html.Div(dcc.Graph(
            id="ageSexe",
            style={"border":"1px black solid"}),
            className="seven columns"
        ),
        
        html.Div(dcc.Graph(
            id="sexeMatri",
            style={"border":"1px black solid"}),
            className="five columns"
        )
        ],className="row"),
        
        html.Div(
            html.Div(dcc.RangeSlider(
                id="age",
                min=0,
                max=len(ageSexe04["AllTypes"].df.index),
                marks=categToAgeCateg,
                value=[3,6],
        ),className="ten columns offset-by-one column"),
        className="row"
        )
    ])

## CALLBACKS

@app.callback(
    Output('ageSexe','figure'),
    [Input('age','value'),
    Input('sexe','value')
])

def updateFigAgeCateg(categories,sexe):
    global categToAgeCateg
    
    start=ageSexe04["AllTypes"].df.index[0]
    end=categToAgeCateg[categories[1]]
    trace=go.Bar( x=ageSexe04["AllTypes"].df.index.tolist()[categories[0]:categories[1]],y=ageSexe04["AllTypes"].df[sexe])
    return {
        'data':[trace],
        'layout':{
        }
    }

@app.callback(
    Output("sexeMatri","figure"),
    [Input("matri","value"),
    Input("sexe","value"),
    Input("disType","value")
    ])

def updateFigMatri(statuses,sexe,disType):
    print(sexeMatri04["AllTypes"].df.loc[statuses][sexe])
    return {
        "data":[go.Pie(labels=statuses, values=sexeMatri04["AllTypes"].df.loc[statuses][sexe].tolist())],
        'layout':{

        }
    }

if __name__ == '__main__':
    
    app.run_server(debug=True)