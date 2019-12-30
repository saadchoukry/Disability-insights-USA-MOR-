# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
from ETL.loader import EtlHcp04 
from pandasTesting import dfs_sum
import plotly.graph_objs as go
from itertools import chain
from ETL.ETL_USA.usaLoader import UsaLoader as loader
import appToolz as toolz
from plotly.subplots import make_subplots

# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

## ETLs
init= False
dfs = None
ageSexe04= None
sexeMatri04 = None
illitSexeEnvir = None
illitAgeSexe = None
educaEnvir = None
actEnv = None
actSexeEnv = None
usaData = None

def ETL():
    global init,dfs,ageSexe04,categToAgeCateg,sexeMatri04,illitSexeEnvir,illitAgeSexe,educaEnvir,actEnv,actSexeEnv,usaData
    if not init :
        print("--- RUNNING ETL ---")
        ETL = EtlHcp04()
        usaData = loader()
        ageSexe04 = ETL.extendedDataFrames[0]
        sexeMatri04 = ETL.extendedDataFrames[1]
        illitSexeEnvir = ETL.extendedDataFrames[2]
        illitAgeSexe = ETL.extendedDataFrames[3]
        educaEnvir = ETL.extendedDataFrames[4]
        actEnv = ETL.extendedDataFrames[5]
        actSexeEnv = ETL.extendedDataFrames[6]
        init=True
    else:
        print("Data has already been loaded")
        return usaData
ETL()
categToAgeCateg = {ageSexe04["Sensoriel"].df.index.values.tolist().index(categ): '{}'.format(categ[:2]) for categ in ageSexe04["Sensoriel"].df.index.values.tolist()[:-1]}

print(categToAgeCateg)

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Create global chart template

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),

)



# Create app layout
app.layout = html.Div([
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div([
            html.Div([
                html.Img(
                    src=app.get_asset_url("LOGO.png"),
                    id="plotly-image",
                    style={
                        "height": "60px",
                        "width": "auto",
                        "margin-bottom": "0px",
                    },
            )],className="one-third column"),
            html.Div([
                html.Div([
                    html.H3(
                        "Disability statistics",
                        style={"margin-bottom": "0px"},
                    ),
                    html.H5(
                        "Morocco - United States Of America", style={"margin-top": "0px"}
                    ),
                ])
            ],className="one-half column",id="title",),
                
        ],id="header",className="row flex-display",style={"margin-bottom": "25px"}),
        
        
        dcc.Tabs([
            dcc.Tab(label='Statistiques générales', children=[]),
            dcc.Tab(label='Statistiques avancées (MAR)', children=[
                html.Div([
                    html.Div([
                        html.P(
                            "Filter par années",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="yearMar",
                            options=[{'label':'2004','value':'2004'},{'label':'2014','value':'2014'}],
                            multi=True,
                            value=["2004"],
                            className="dcc_control",
                        ),
                        html.P(
                            "Filter par catégories d'âge",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="ageMar",
                            min=0,
                            max=len(ageSexe04["Sensoriel"].df.index),
                            marks=categToAgeCateg,
                            value=[3,6],
                            className="dcc_control"
                        ),
                        html.Div(style={'padding': 15}),
                        html.P(
                            "Filtrer par situation matrimoniale",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="matri",
                            options=[{"label":matri,"value":matri} for matri in sexeMatri04["Sensoriel"].df.index],
                            value=["Célibataire","Marié","Veuf","Divorcé"],
                            multi=True,
                            clearable=False,
                            style={'width':'24vw','display': 'inline-block'}
                            ),
                        html.P(
                            "Filtrer par sexes",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="sexe",
                            options=[{"label":"Masculin","value":"Masculin"},{"label":"Féminin","value":"Féminin"}],
                            value=["Masculin","Féminin"],
                            clearable=False,
                            multi =True,
                            placeholder="Sexe",
                            className="dcc_control"
                        ),
                        html.P(
                            "Filtrer par types d'handicap",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="disType",
                            options=[{"label":disType,"value":disType} for disType in list(sexeMatri04.keys())],
                            value=["Sensoriel","Chronique","Moteur","Mental"],
                            multi=True,
                            clearable=False,
                            placeholder="Type d'handicap",
                            className='dcc_control'
                        ),   
                        html.P(
                            "Filtrer par environnement",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="envir",
                            options=[{"label":envir,"value":envir} for envir in illitSexeEnvir["Sensoriel"].df.index],
                            value=["Rural","urbain"],
                            multi=True,
                            clearable=False,
                            className='dcc_control'
                        ),   
                    ],className="pretty_container four columns",id="cross-filter-options"), 
                    html.Div([
                            html.Div([
                                html.Div(
                                    [html.H6(id="t23"), html.P("No. of Wells")],
                                    id="wells1",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="t24"), html.P("Gas")],
                                    id="gas1",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="t25"), html.P("Oil")],
                                    id="oil1",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="t26"), html.P("Water")],
                                    id="water1",
                                    className="mini_container",
                                ),
                            ],
                    id="info-container3",
                    className="row container-display",
                            ),
                            html.Div(
                                [dcc.Graph(id="sexAgeMar")],
                                id="countGraphContainer",
                                className="pretty_container",
                            ),
                        ],
                        id="right-column1",
                        className="eight columns",
                    ),
                ],
                className="row flex-display",),
                    html.Div([
                            html.Div(
                                [dcc.Graph(id="workExp66")],
                                className="pretty_container seven columns",
                            ),
                            html.Div(
                                [dcc.Graph(id="emplStatus66")],
                                className="pretty_container five columns",
                            ),
                        ],
                        className="row flex-display",
                    ),
                    html.Div([
                            html.Div(
                                [dcc.Graph(id="ageDisNumber53")],
                                className="pretty_container seven columns",
                            ),
                            html.Div(
                                [dcc.Graph(id="healthIns34")],
                                className="pretty_container five columns",
                            ),
                        ],
                        className="row flex-display",
                        ),
            ]),
            dcc.Tab(label='Statistiques avancées (USA)', children=[
                html.Div([
                    html.Div([
                        html.P(
                            "Filter by year",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="year",
                            options=[{'label':'2015','value':'15'},{'label':'2016','value':'16'}],
                            multi=True,
                            placeholder="Select states",
                            value=["15"],
                            className="dcc_control",
                        ),
                        html.P(
                            "Filter by age categories",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="ageUsa",
                            min=0,
                            max=len(toolz.getAgeCategories(usaData.dfsArray))-1,
                            marks={toolz.getAgeCategories(usaData.dfsArray).index(ageCateg):'{}'.format(ageCateg) for ageCateg in toolz.getAgeCategories(usaData.dfsArray)},
                            value=[1,4],
                            className="dcc_control"
                        ),
                        html.Div(style={'padding': 15}),
                        html.P(
                            "Filter by states",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="states",
                            options=[{'label':state,'value':state} for state in toolz.getAllStatesArray(usaData.dfsArray)
                            ],
                            multi=True,
                            value=["Alabama"],
                            className="dcc_control"
                        ),
                        html.P(
                            "Filter by gender",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="sex",
                            options=[{"label":"Male","value":"male"},{"label":"Female","value":"female"}],
                            value=["male","female"],
                            clearable=False,
                            multi =True,
                            className="dcc_control"
                        ),
                        html.P(
                            "Filter by disability types",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="difTypes",
                            options=[{"label":"{}".format(difType),"value":"{}".format(difType)} for difType in toolz.getDifficultyTypes(usaData.dfsArray) ],
                            value=[ difType for difType in toolz.getDifficultyTypes(usaData.dfsArray) ],
                            clearable=False,
                            multi =True,
                            className='dcc_control'
                        ),   
                    ],
                className="pretty_container four columns",
                id="cross-filter-options2"),
                    html.Div([
                            html.Div([
                                html.Div(
                                    [html.H6(id="t233"), html.P("No. of Wells")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="t243"), html.P("Gas")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="t253"), html.P("Oil")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="t263"), html.P("Water")],
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                    id="info-container",
                    className="row container-display",
                            ),
                            html.Div(
                                [dcc.Graph(id="sexAge")],
                                id="countGraphContainer1651",
                                className="pretty_container",
                            ),
                        ],
                        id="right-column2",
                        className="eight columns",
                    ),
                ],
                className="row flex-display",),
                    html.Div([
                            html.Div(
                                [dcc.Graph(id="workExp")],
                                className="pretty_container seven columns",
                            ),
                            html.Div(
                                [dcc.Graph(id="emplStatus")],
                                className="pretty_container five columns",
                            ),
                        ],
                        className="row flex-display",
                    ),
                    html.Div([
                            html.Div(
                                [dcc.Graph(id="ageDisNumber")],
                                className="pretty_container seven columns",
                            ),
                            html.Div(
                                [dcc.Graph(id="healthIns")],
                                className="pretty_container five columns",
                            ),
                        ],
                        className="row flex-display",
                        ),
            ]), 
        ]),        
        ],id="mainContainer", style={"display": "flex", "flex-direction": "column"})



























# Main
if __name__ == "__main__":
    app.run_server(debug=True)
