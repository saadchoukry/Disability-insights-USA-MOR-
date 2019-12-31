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
from ETL.ETL_HCP14.SexeEnvDisType import SexeEnvDisType_HCP14
from ETL.ETL_HCP14.Matrimonial import Matrimonial_HCP14
import plotly.express as px



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
sexeEnvDisType_HCP14= None
matrimonial_HCP14 = None
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
        sexeEnvDisType_HCP14 = SexeEnvDisType_HCP14()
        matrimonial_HCP14 = Matrimonial_HCP14()
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


"""
# Load data
df = pd.read_csv(DATA_PATH.joinpath("wellspublic.csv"), low_memory=False)
df["Date_Well_Completed"] = pd.to_datetime(df["Date_Well_Completed"])
df = df[df["Date_Well_Completed"] > dt.datetime(1960, 1, 1)]

trim = df[["API_WellNo", "Well_Type", "Well_Name"]]
trim.index = trim["API_WellNo"]
dataset = trim.to_dict(orient="index")

points = pickle.load(open(DATA_PATH.joinpath("points.pkl"), "rb"))
"""
## General stats

def getDisTypeGeneral():
    pass
# Create global chart template

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),)

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
            dcc.Tab(label='Statistiques générales', children=[
            html.Div([
                html.Div([
                    dcc.Graph(id="disTypeGenGraph")
                    ],
                    id="disTypeGenGraphDiv",
                    className="pretty_container seven columns",
                    )
            ])    
                ]),
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
                                [dcc.Graph(id="ageSexeMar")],
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
                                [dcc.Graph(id="educEnvir")],
                                className="pretty_container seven columns",
                            ),
                            html.Div(
                                [dcc.Graph(id="illitSexe")],
                                className="pretty_container five columns",
                            ),
                        ],
                        className="row flex-display",
                    ),
                    html.Div([
                            html.Div(
                                [dcc.Graph(id="sexeMatri")],
                                className="pretty_container seven columns",
                            ),
                            html.Div(
                                [dcc.Graph(id="illitAge")],
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


# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("sexAge", "figure")],
)



@app.callback(
    Output("sexAge","figure"),[
        Input("ageUsa",'value'),
        Input("states",'value'),
        Input('sex','value'),
        Input('difTypes','value'),
        Input("year","value")
    ]
)
def updateFigAge(ageCateg,states,sex,difTypes,year):
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] = "PREVALENCE BY AGE".title()
    if len(year) == 1:
        selectedExtendedDfs = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['SEX']),'state',states),'difficulty',difTypes),'year',year)
        df = dfs_sum([df['dataFrame'] for df in selectedExtendedDfs])[toolz.getAgeOptions(usaData.dfsArray,ageCateg)]
        if len(sex) == 2:
            trace1=go.Bar( x=df.columns.tolist(), y=df.loc["Male"].tolist(),name='Male')
            trace2=go.Bar( x=df.columns.tolist(), y=df.loc["Female"].tolist(),name='Female')
            return {
                'data':[trace1,trace2],
                'layout':layout1
                }
        else:
            trace=go.Bar( x=df.columns.tolist(), y=df.loc[sex[0].title()].tolist(),name=sex[0].title())
            return {
                'data':[trace],
                'layout':layout1
            }
    else:
        
        selectedExtendedDfsForYear1 = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['SEX']),'state',states),'difficulty',difTypes),'year',[year[0]])
        selectedExtendedDfsForYear2 = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['SEX']),'state',states),'difficulty',difTypes),'year',[year[1]])
        dfYear1 = dfs_sum([df['dataFrame'] for df in selectedExtendedDfsForYear1])[toolz.getAgeOptions(usaData.dfsArray,ageCateg)]
        dfYear2 = dfs_sum([df['dataFrame'] for df in selectedExtendedDfsForYear2])[toolz.getAgeOptions(usaData.dfsArray,ageCateg)]
        
        if len(sex) == 2:
            trace1=go.Bar( x=dfYear1.columns.tolist(), y=dfYear1.loc["Male"].tolist(),name='Male (20'+year[0]+")", width=0.15)
            trace2=go.Bar( x=dfYear1.columns.tolist(), y=dfYear1.loc["Female"].tolist(),name='Female (20'+year[0]+")", width=0.15)
            trace3=go.Bar( x=dfYear1.columns.tolist(), y=dfYear2.loc["Male"].tolist(),name='Male (20'+year[1]+")", width=0.15)
            trace4=go.Bar( x=dfYear1.columns.tolist(), y=dfYear2.loc["Female"].tolist(),name='Female (20'+year[1]+")", width=0.15)
            
            return {
            'data':[trace1,trace2,trace3,trace4],
            'layout':layout1
        }
        else:
            trace=go.Bar( x=df.columns.tolist(), y=df.loc[sex[0].title()].tolist(),name=sex[0].title())
            return {
                'data':[trace],
                'layout':layout1
            }


@app.callback(
    Output("workExp","figure"),[
        Input("states",'value'),
        Input("year","value")
    ]
)

def updateFigWorkExp(states,years):
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] = "WORK EXPERIENCE".title()
    #layout['margin']=go.Margin(b=300)

    traces = []
    for year in years:
        selectedExtendedDfs = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['WORK EXPERIENCE']),'state',states),'year',[year])
        df = dfs_sum([df['dataFrame'] for df in selectedExtendedDfs])
        traces.append(go.Bar( x=df.index.tolist(), y=df.iloc[:,0].tolist(),name="20"+year,width=0.4))
    return {
        'data':traces,
        'layout':layout1
    }

@app.callback(
    Output("healthIns","figure"),[
        Input("states",'value'),
        Input("ageUsa",'value'),
        Input("year","value")
    ]
)
def updateFigHealthIns(states,ageCateg,year):
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] = "PREVALENCE OF INSURED DISABLED PEOPLE".title()
    if len(year)>1:
        selectedExtendedDfsForYear1 = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['AGE']),'state',states),"columns",["POPULATION"]),'year',[year[0]])
        selectedExtendedDfsForYear2 = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['AGE']),'state',states),"columns",["POPULATION"]),'year',[year[1]])
        dfYear1 = dfs_sum([df['dataFrame'] for df in selectedExtendedDfsForYear1])
        dfYear2 = dfs_sum([df['dataFrame'] for df in selectedExtendedDfsForYear2])
        trace1=go.Bar( x=[index[:-1] for index in dfYear1.index.tolist()], y=dfYear1.iloc[:,0].tolist(),name="20"+year[0])
        trace2=go.Bar( x=[index[:-1] for index in dfYear2.index.tolist()], y=dfYear2.iloc[:,0].tolist(),name="20"+year[1])
        return {
            'data':[trace1,trace2],
            'layout':layout1
        }
    else:
        selectedExtendedDfs = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['AGE']),'state',states),"columns",["POPULATION"]),'year',[year[0]])
        df = dfs_sum([df['dataFrame'] for df in selectedExtendedDfs])
        trace = go.Bar( x=[index[:-1] for index in df.index.tolist()], y=df.iloc[:,0].tolist())
        return {
            'data':[trace],
            'layout':layout1
        }

@app.callback(
    Output("ageDisNumber","figure"),[
        Input("states",'value'),
        Input("ageUsa",'value'),
        Input("year","value")
    ]
)
def updateFigAgeDisNumber(states,ageCateg,year):
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] = "AGE BY NUMBER OF DISABILITIES".title()
    if len(year)>1 :
        selectedExtendedDfsForYear1 = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['AGE']),'state',states),"columns",["NUMBER OF DISABILITIES"]),'year',[year[0]])
        selectedExtendedDfsForYear2 = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['AGE']),'state',states),"columns",["NUMBER OF DISABILITIES"]),'year',[year[1]])
        dfYear1 = dfs_sum([df['dataFrame'] for df in selectedExtendedDfsForYear1])
        dfYear2 = dfs_sum([df['dataFrame'] for df in selectedExtendedDfsForYear2])
        fig = make_subplots(rows=1, cols=2,
        subplot_titles=("20"+str(year[0]),"20"+str(year[1])))
        fig.add_trace(go.Bar( x=[index[:-1] for index in dfYear1.index.tolist()], y=dfYear1.iloc[:,0].tolist(),name=dfYear1.columns.tolist()[0].title()), 
        row=1, col=1)
        fig.add_trace(go.Bar( x=[index[:-1] for index in dfYear1.index.tolist()], y=dfYear1.iloc[:,1].tolist(),name=dfYear1.columns.tolist()[1].title()), 
        row=1, col=1)
        fig.add_trace(go.Bar( x=[index[:-1] for index in dfYear1.index.tolist()], y=dfYear2.iloc[:,0].tolist(),name=dfYear2.columns.tolist()[0].title()), 
        row=1, col=2)
        fig.add_trace(go.Bar( x=[index[:-1] for index in dfYear1.index.tolist()], y=dfYear2.iloc[:,1].tolist(),name=dfYear2.columns.tolist()[1].title()), 
        row=1, col=2)
        return fig
    
    else:
        selectedExtendedDfs = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['AGE']),'state',states),"columns",["NUMBER OF DISABILITIES"])
        df = dfs_sum([df['dataFrame'] for df in selectedExtendedDfs])
        trace1=go.Bar( x=[index[:-1] for index in df.index.tolist()], y=df.iloc[:,0].tolist(),name=df.columns.tolist()[0].title())
        trace2=go.Bar( x=[index[:-1] for index in df.index.tolist()], y=df.iloc[:,1].tolist(),name=df.columns.tolist()[1].title())

        return {
            'data':[trace1,trace2],
            'layout':layout1
        }

@app.callback(
    Output("emplStatus","figure"),[
        Input("states",'value'),
        Input("year","value")
    ]
)
def updateFigEmplStatus(states,years):
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] =  "EMPLOYMENT STATUS".title()
    if len(years)>1:
        selectedExtendedDfsForYear1 = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['EMPLOYMENT SECTOR']),'state',states),'year',[years[0]])
        dfYear1 = dfs_sum([df['dataFrame'] for df in selectedExtendedDfsForYear1])
        selectedExtendedDfsForYear2 = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['EMPLOYMENT SECTOR']),'state',states),'year',[years[1]])
        dfYear2 = dfs_sum([df['dataFrame'] for df in selectedExtendedDfsForYear2])
        trace = go.Sunburst(
            ids= ["20"+year for year in years]+["20"+year+" - "+ status for year in years for status in dfYear1.columns.tolist()],
            labels=["20"+year for year in years]+[status for status in dfYear1.columns.tolist()]*2,
            parents= ["" for i in range(len(years))] + list(chain.from_iterable(("20"+year,"20"+year) for year in years)),
            values= [dfYear1.iloc[0,:].sum(),dfYear2.iloc[0,:].sum()] + [dfYear1.iloc[0,0],dfYear1.iloc[0,1],dfYear2.iloc[0,0],dfYear2.iloc[0,1]],
            branchvalues="total",
        )
        return {
            'data':[trace],
            'layout':layout1
        }
    else:
        selectedExtendedDfs = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['EMPLOYMENT SECTOR']),'state',states),'year',[years[0]])
        df = dfs_sum([df['dataFrame'] for df in selectedExtendedDfs])
        trace = go.Pie(labels= df.columns.tolist(), values=df.iloc[0].tolist())
        return {
            'data':[trace],
            'layout':layout1
        }


@app.callback(
    Output('educEnvir','figure'),
    [Input('envir','value'),
    Input('disType','value')]
)

def updateFigEducEnvir(envir,disType):
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] = "Niveau d'éducation dans le monde "+envir[0].lower()
    df= dfs_sum([educaEnvir[dis].df for dis in disType])
    if len(envir)==1:
        trace = go.Pie(labels=df.index.values, values=df[envir[0]].tolist())
        return {
        'data':[trace],
        'layout':layout1

        }
    else:
        layout1  = copy.deepcopy(layout)
        layout1['title'] = "Niveau d'éducation par environment"
        trace = go.Sunburst(
            ids= [env for env in envir]+[env+" - "+ level for env in envir for level in df.index.values],
            labels=[env for env in envir]+[level for level in df.index.values]*4,
            parents= ["" for i in range(len(envir))] + list(chain.from_iterable((env,env,env,env) for env in envir)),
            values= [df[env].sum() for env in envir] + [df.loc[level][env] for env in envir for level in df.index.values],
            branchvalues="total",
        )
        return {
        'data':[trace],
        'layout':layout1

        }

@app.callback(
    Output('ageSexeMar','figure'),
    [Input('ageMar','value'),
    Input('sexe','value'),
    Input('disType','value')
])

def updateFigAgeCateg(categories,sexe,disType):
    global categToAgeCateg
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] = "Prévalence par catégories d'âge"
    df = dfs_sum([ageSexe04[dis].df[sexe] for dis in disType])
    start=df.index[0]
    end=categToAgeCateg[categories[1]]
    if len(sexe) == 1:
        trace=go.Bar( x=df.index.tolist()[categories[0]:categories[1]],y=df[sexe[0]])
    else:
        trace=go.Bar( x=df.index.tolist()[categories[0]:categories[1]],y=df["Masculin"] + df["Féminin"])
    return {
        'data':[trace],
        'layout':layout1
    }

@app.callback(
    Output("sexeMatri","figure"),
    [Input("matri","value"),
    Input("sexe","value"),
    Input("disType","value")
    ])

def updateFigMatri(statuses,sexe,disType):
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] = "Prévalence selon la situation matrimoniale"
    df =dfs_sum([sexeMatri04[dis].df for dis in disType]).loc[statuses]
    if len(sexe) == 1:
        trace  = go.Pie(labels=statuses, values=df[sexe[0]].tolist())
    else:
        trace = go.Pie(labels=statuses, values=(df["Masculin"] + df["Féminin"]).tolist())
    return {
        "data":[trace],
        'layout':layout1
    }

@app.callback(
    Output("illitSexe","figure"),
    [Input("sexe","value"),
    Input("disType","value"),
    Input("envir","value")
    ])

def updateFigIllit(sexe,disType,envir):
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] = "Analphabétisme par environnement "
    df= dfs_sum([illitSexeEnvir[dis].df for dis in disType]).loc[envir][sexe]
    if len(sexe)==1:
        trace = go.Pie(labels=envir, values=df.loc[envir[0]].tolist() + df.loc[envir[1]].tolist())
    else:
        trace = go.Sunburst(
            ids= [env for env in envir]+[env+" - "+ sex for env in envir for sex in sexe],
            labels=[env for env in envir]+[sex for sex in sexe]*2,
            parents= ["" for i in range(len(envir))] + list(chain.from_iterable((env,env) for env in envir)),
            values= [df.loc[env].sum() for env in envir] + [df.loc[env][sex] for env in envir for sex in sexe],
            branchvalues="total",
        )
        
    return {
        'data' : [trace],
        'layout' : layout1
    }




@app.callback( Output("illitAge","figure"),
    [Input("sexe","value"),
    Input("disType","value")])
def updateFigIllitAge(sexe,disType):
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] = "Analphabétisme par catégories d'âge"
    layout1['barmode'] = 'stack'
    df = dfs_sum([illitAgeSexe[dis].df[sexe] for dis in disType])
    if len(sexe) == 1:
        trace=go.Bar( x=df.index.tolist(),y=df[sexe[0]])
        return {
        "data":[trace],
        "layout":layout1
    }
    else:
        trace=[go.Bar(name="Masculin" , x=df.index.tolist(),y=df["Masculin"]),
        go.Bar(name="Féminin", x=df.index.tolist(),y=df["Féminin"])]
        return {
            "data":trace,
            "layout":layout1,
        }
  

"""
@app.callback(
    Output("activityEnv","figure"),[
        Input("disType",'value'),
        Input("envir",'value')
    ]
)
def updateFigActivityEnv(disType,envir):
    global layout
    layout1  = copy.deepcopy(layout)
    layout1['title'] = "MAZAL 3"
    df = dfs_sum([actEnv[dis].df[envir] for dis in disType])
    if len(envir) == 1:
        trace=go.Bar( x=df.index.tolist(), y=df[envir[0]].tolist())
        return {
        'data':[trace],
        'layout':layout1
    }
    else:
        layout1  = copy.deepcopy(layout)
        layout1['title'] = "MAZAL 3"
        trace1=go.Bar(name="urbain",x=df.index.tolist(),y = df["urbain"] )
        trace2=go.Bar(name="Rural",x=df.index.tolist(),y = df ["Rural"])
        return {
            'data':[trace1,trace2],
            'layout':layout1
        }

"""

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
