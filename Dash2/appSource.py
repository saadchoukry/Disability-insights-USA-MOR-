import dash
import dash_core_components as dcc
import dash_html_components as html
from ETL.loader import EtlHcp04 
from pandasTesting import dfs_sum
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from itertools import chain
from ETL.ETL_USA.usaLoader import UsaLoader as loader
import appToolz as toolz
from plotly.subplots import make_subplots


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
categToAgeCateg = {ageSexe04["Sensoriel"].df.index.values.tolist().index(categ): '{}'.format(categ) for categ in ageSexe04["Sensoriel"].df.index.values.tolist()}
### Dash CONFIG
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout=html.Div([

    dcc.Tabs([

        dcc.Tab(label='Statistiques générales', children=[
            html.Div([
                
                html.Div(dcc.Graph(
                    id="sexeMatri",
                    style={"border":"1px black solid",
                    }),
                    className="five columns"
                ),
                html.Div(dcc.Graph(
                    id="PrevSexe",
                    style={"border":"1px black solid",
                    }),
                    className="five columns"
                ),
        ],className="row"),

        html.Div([
                html.Div(dcc.Graph(
                    id="PrevDisType",
                    style={"border":"1px black solid",
                    }),
                    className="five columns"
                ),
                html.Div(dcc.Graph(
                    id="PrevEnvir",
                    style={"border":"1px black solid",
                    }),
                    className="five columns"
                ),
        ],className="row")
        
        ]),






        dcc.Tab(label='Statistiques avancées (MAR)', children=[
              
        html.Div(style={'padding': 15}),
        html.Div([
            html.Div([
        html.Div(dcc.Dropdown(
            id="sexe",
            options=[{"label":"Masculin","value":"Masculin"},{"label":"Féminin","value":"Féminin"}],
            value=["Masculin","Féminin"],
            clearable=False,
            multi =True,
            placeholder="Sexe",
            style={'width':'24vw','display': 'inline-block'}
            ),className="two columns"),
        html.Div(dcc.Dropdown(
            id="matri",
            options=[{"label":matri,"value":matri} for matri in sexeMatri04["Sensoriel"].df.index],
            value=["Célibataire","Marié","Veuf","Divorcé"],
            multi=True,
            clearable=False,
            placeholder="Statut matrimonial",
            style={'width':'24vw','display': 'inline-block'}
            ),
            className="four columns",),
        html.Div(dcc.Dropdown(
            id="disType",
            options=[{"label":disType,"value":disType} for disType in list(sexeMatri04.keys())],
            value=["Sensoriel","Chronique","Moteur","Mental"],
            multi=True,
            clearable=False,
            placeholder="Type d'handicap",
            style={'width':'26vw','display': 'inline-block'}
            ),
            className="four columns",),
        html.Div(dcc.Dropdown(
            id="envir",
            options=[{"label":envir,"value":envir} for envir in illitSexeEnvir["Sensoriel"].df.index],
            value=["Rural","urbain"],
            multi=True,
            clearable=False,
            placeholder="Environnement",
            style={'width':'13vw','display': 'inline-block'}
            ),
            className="one column",)
    ],className="row"),
            html.Div([
                html.Div(dcc.Graph(
                    id="ageSexe",
                    style={"border":"1px black solid",
                    }),
                    className="seven columns"
                ),
                ],className="row"),
                html.Div(
                    html.Div(dcc.RangeSlider(
                        id="age",
                        min=0,
                        max=len(ageSexe04["Sensoriel"].df.index),
                        marks=categToAgeCateg,
                        value=[3,6],
                ),className="ten columns offset-by-one column"),
                className="row"),
                 html.Div(style={'padding': 15}),
            html.Div(dcc.Graph(
            id="illitSexe",
            style={"border":"1px black solid",
            })
            ,className="five columns"),
            html.Div(dcc.Graph(
            id="illitAge",
            style={"border":"1px black solid",
            })
            ,className="seven columns")
            
            ],className="row"),

        html.Div(style={'padding': 15}),
        html.Div([
            html.Div(dcc.Graph(
            id="educEnvir",
            style={"border":"1px black solid",
            })
            ,className="five columns"),

            html.Div(dcc.Graph(
            id="activityEnv",
            style={"border":"1px black solid",
            })
            ,className="seven columns")

            ],className="row"),
        
        ]),

        # Custom
        dcc.Tab(label='Statistiques avancées (USA)', children=[
            html.Div(
                    html.Div(dcc.Dropdown(
                        id="year",
                        options=[{'label':'2015','value':'15'},{'label':'2016','value':'16'}],
                        multi=True,
                        placeholder="Select states",
                        value=["15"],
                        style={'width':'50vw','display': 'inline-block'}
                    ),className="ten columns offset-by-one column"),
                className="row"),
            html.Div(
                    html.Div(dcc.RangeSlider(
                        id="ageUsa",
                        min=0,
                        max=len(toolz.getAgeCategories(usaData.dfsArray))-1,
                        marks={toolz.getAgeCategories(usaData.dfsArray).index(ageCateg):'{}'.format(ageCateg) for ageCateg in toolz.getAgeCategories(usaData.dfsArray)},
                        value=[1,4],
                ),className="ten columns offset-by-one column"),
                className="row"),
            html.Div(style={'padding': 15}),
            html.Div(
                    html.Div(dcc.Dropdown(
                        id="states",
                        options=[{'label':state,'value':state} for state in toolz.getAllStatesArray(usaData.dfsArray)
                        ],
                        multi=True,
                        placeholder="Select states",
                        value=["Alabama"],
                        style={'width':'50vw','display': 'inline-block'}
                    )  ,className="six columns"),
                className="row"),
            html.Div(
                    html.Div(dcc.Dropdown(
                        id="sex",
                        options=[{"label":"Male","value":"male"},{"label":"Female","value":"female"}],
                        value=["male","female"],
                        clearable=False,
                        multi =True,
                        placeholder="Select genders",
                        style={'width':'24vw','display': 'inline-block'}
                    ),className="two columns")
            ,className ="row"),
            html.Div(
                    html.Div(dcc.Dropdown(
                        id="difTypes",
                        options=[{"label":"{}".format(difType),"value":"{}".format(difType)} for difType in toolz.getDifficultyTypes(usaData.dfsArray) ],
                        value=[ difType for difType in toolz.getDifficultyTypes(usaData.dfsArray) ],
                        clearable=False,
                        multi =True,
                        placeholder="Select difficulty types",
                        style={'width':'60vw','display': 'inline-block'}
                    ),className="two columns")
            ,className ="row"),
            html.Div(
                html.Div(dcc.Graph(
                    id="workExp",
                    style={"border":"1px black solid",
                    }),
                    className="eleven columns"
                ),className='row'),
            html.Div(
                html.Div(dcc.Graph(
                    id="sexAge",
                    style={"border":"1px black solid",
                    }),
                    className="ten columns"
                ),className='row'),
            
            html.Div(
                html.Div(dcc.Graph(
                    id="healthIns",
                    style={"border":"1px black solid",
                    }),
                    className="five columns"
                ),className='row'),
            html.Div(
                html.Div(dcc.Graph(
                    id="ageDisNumber",
                    style={"border":"1px black solid",
                    }),
                    className="seven columns"
                ),className='row'),
            
            html.Div(
                html.Div(dcc.Graph(
                    id="emplStatus",
                    style={"border":"1px black solid",
                    }),
                    className="seven columns"
                ),className='row'),
        ]),
        
    ]),
  
    
    ## Figures' Div

        
      
        
    ])

## CALLBACKS

## General Stats
@app.callback(
       Output('PrevSexe','figure'),
    [Input('sexe','value'),
    ]
)
def updatePrevSexe(sexe):
    df = dfs_sum([illitAgeSexe[dis].df for dis in ["Sensoriel","Chronique","Moteur","Mental"] ])
    trace = [
        go.Bar( x=[s for s in sexe ],y=[df[s].sum()/df["Ensemble"].sum() for s in sexe])
    ]
    return {
        'data':trace,
        'layout':{

        }
    }

@app.callback(
       Output('PrevEnvir','figure'),
    [Input('envir','value'),
    ]
)
def updatePrevEnvir(envir):
    df = dfs_sum([illitSexeEnvir[dis].df for dis in ["Sensoriel","Chronique","Moteur","Mental"] ])
    print(envir)
    trace = [
        go.Bar( x=[e for e in envir ],y=[df.loc[e]["Ensemble"]/df["Ensemble"].sum() for e in envir])
    ]
    return {
        'data':trace,
        'layout':{

        }
    }


@app.callback(
       Output('PrevDisType','figure'),
    [Input('disType','value'),
    ]
)
def updatePrevDisType(disType):
    ensembleDesEnsembles = 0
    for dis in disType:
        ensembleDesEnsembles += illitAgeSexe[dis].df["Ensemble"].sum()
    trace = [
        go.Bar( x=[dis for dis in disType ],y=[illitAgeSexe[dis].df["Ensemble"].sum()/ensembleDesEnsembles for dis in disType])
    ]

    return {
        'data':trace,
        'layout':{

        }
    }


## Advanced Stats

@app.callback(
    Output('educEnvir','figure'),
    [Input('envir','value'),
    Input('disType','value')]
)

def updateFigEducEnvir(envir,disType):
    df= dfs_sum([educaEnvir[dis].df for dis in disType])
    if len(envir)==1:
        trace = go.Pie(labels=df.index.values, values=df[envir[0]].tolist())
        return {
        'data':[trace],
        'layout':{
            'title':"Niveau d'éducation dans le monde "+envir[0].lower(),
            }

        }
    else:
        trace = go.Sunburst(
            ids= [env for env in envir]+[env+" - "+ level for env in envir for level in df.index.values],
            labels=[env for env in envir]+[level for level in df.index.values]*4,
            parents= ["" for i in range(len(envir))] + list(chain.from_iterable((env,env,env,env) for env in envir)),
            values= [df[env].sum() for env in envir] + [df.loc[level][env] for env in envir for level in df.index.values],
            branchvalues="total",
        )
        return {
        'data':[trace],
        'layout':{
            'title':"Niveau d'éducation par environment",
            }

        }
    
    

@app.callback(
    Output('ageSexe','figure'),
    [Input('age','value'),
    Input('sexe','value'),
    Input('disType','value')
])

def updateFigAgeCateg(categories,sexe,disType):
    global categToAgeCateg
    df = dfs_sum([ageSexe04[dis].df[sexe] for dis in disType])
    start=df.index[0]
    end=categToAgeCateg[categories[1]]
    if len(sexe) == 1:
        trace=go.Bar( x=df.index.tolist()[categories[0]:categories[1]],y=df[sexe[0]])
    else:
        trace=go.Bar( x=df.index.tolist()[categories[0]:categories[1]],y=df["Masculin"] + df["Féminin"])
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
    df =dfs_sum([sexeMatri04[dis].df for dis in disType]).loc[statuses]
    if len(sexe) == 1:
        trace  = go.Pie(labels=statuses, values=df[sexe[0]].tolist())
    else:
        trace = go.Pie(labels=statuses, values=(df["Masculin"] + df["Féminin"]).tolist())
    return {
        "data":[trace],
        'layout':{
            'title':"Prévalence selon la situation matrimoniale",
            
        }
    }

@app.callback(
    Output("illitSexe","figure"),
    [Input("sexe","value"),
    Input("disType","value"),
    Input("envir","value")
    ])

def updateFigIllit(sexe,disType,envir):
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
        'layout' : {
            
        }
    }


@app.callback( Output("illitAge","figure"),
    [Input("sexe","value"),
    Input("disType","value")]
)
def updateFigIllitAge(sexe,disType):
    df = dfs_sum([illitAgeSexe[dis].df[sexe] for dis in disType])
    if len(sexe) == 1:
        trace=go.Bar( x=df.index.tolist(),y=df[sexe[0]])
        return {
        "data":[trace],
        "layout":{
            
        }
    }
    else:
        trace=[go.Bar(name="Masculin" , x=df.index.tolist(),y=df["Masculin"]),
        go.Bar(name="Féminin", x=df.index.tolist(),y=df["Féminin"])]
        return {
            "data":trace,
            "layout":{
                "barmode": 'stack',
                
            }
        }

@app.callback(
    Output("activityEnv","figure"),[
        Input("disType",'value'),
        Input("envir",'value')
    ]
)
def updateFigActivityEnv(disType,envir):
    df = dfs_sum([actEnv[dis].df[envir] for dis in disType])
    if len(envir) == 1:
        trace=go.Bar( x=df.index.tolist(), y=df[envir[0]].tolist())
        return {
        'data':[trace],
        'layout':{

        }
    }
    else:
        trace1=go.Bar(name="urbain",x=df.index.tolist(),y = df["urbain"] )
        trace2=go.Bar(name="Rural",x=df.index.tolist(),y = df ["Rural"])
        return {
            'data':[trace1,trace2],
            'layout':{
                
            }
        }

## USA
## USA
## USA
## USA
## USA
## USA
## USA
## USA
## USA
## USA
## USA
## USA
## USA
## USA

@app.callback(
    Output("workExp","figure"),[
        Input("states",'value'),
        Input("year","value")
    ]
)
def updateFigWorkExp(states,years):
    traces = []
    for year in years:
        selectedExtendedDfs = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['WORK EXPERIENCE']),'state',states),'year',[year])
        df = dfs_sum([df['dataFrame'] for df in selectedExtendedDfs])
        traces.append(go.Bar( x=df.index.tolist(), y=df.iloc[:,0].tolist(),name="20"+year))
    return {
        'data':traces,
        'layout':{
            'title': "WORK EXPERIENCE".title()
        }
    }


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
    if len(year) == 1:
        selectedExtendedDfs = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['SEX']),'state',states),'difficulty',difTypes),'year',year)
        df = dfs_sum([df['dataFrame'] for df in selectedExtendedDfs])[toolz.getAgeOptions(usaData.dfsArray,ageCateg)]
        if len(sex) == 2:
            trace1=go.Bar( x=df.columns.tolist(), y=df.loc["Male"].tolist(),name='Male')
            trace2=go.Bar( x=df.columns.tolist(), y=df.loc["Female"].tolist(),name='Female')
            return {
                'data':[trace1,trace2],
                'layout':{
                    'title': "PREVALENCE BY AGE".title()

                }
            }
        else:
            trace=go.Bar( x=df.columns.tolist(), y=df.loc[sex[0].title()].tolist(),name=sex[0].title())
            return {
                'data':[trace],
                'layout':{
                    'title': "PREVALENCE BY AGE".title()
                }
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
            'layout':{
                'title': "PREVALENCE BY AGE".title(),
                
                
            }
        }
        else:
            trace=go.Bar( x=df.columns.tolist(), y=df.loc[sex[0].title()].tolist(),name=sex[0].title())
            return {
                'data':[trace],
                'layout':{
                    'title': "PREVALENCE BY AGE".title()
                }
            }

@app.callback(
    Output("healthIns","figure"),[
        Input("states",'value'),
        Input("ageUsa",'value'),
        Input("year","value")
    ]
)
def updateFigHealthIns(states,ageCateg,year):
    if len(year)>1:
        selectedExtendedDfsForYear1 = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['AGE']),'state',states),"columns",["POPULATION"]),'year',[year[0]])
        selectedExtendedDfsForYear2 = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['AGE']),'state',states),"columns",["POPULATION"]),'year',[year[1]])
        dfYear1 = dfs_sum([df['dataFrame'] for df in selectedExtendedDfsForYear1])
        dfYear2 = dfs_sum([df['dataFrame'] for df in selectedExtendedDfsForYear2])
        trace1=go.Bar( x=[index[:-1] for index in dfYear1.index.tolist()], y=dfYear1.iloc[:,0].tolist(),name="20"+year[0])
        trace2=go.Bar( x=[index[:-1] for index in dfYear2.index.tolist()], y=dfYear2.iloc[:,0].tolist(),name="20"+year[1])
        return {
            'data':[trace1,trace2],
            'layout':{
                'title': "PREVALENCE OF INSURED DISABLED PEOPLE".title()
            }
        }
    else:
        selectedExtendedDfs = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['AGE']),'state',states),"columns",["POPULATION"]),'year',[year[0]])
        df = dfs_sum([df['dataFrame'] for df in selectedExtendedDfs])
        trace = go.Bar( x=[index[:-1] for index in df.index.tolist()], y=df.iloc[:,0].tolist())
        return {
            'data':[trace],
            'layout':{
                'title': "PREVALENCE OF INSURED DISABLED PEOPLE".title()
            }
        }

@app.callback(
    Output("ageDisNumber","figure"),[
        Input("states",'value'),
        Input("ageUsa",'value'),
        Input("year","value")
    ]
)
def updateFigAgeDisNumber(states,ageCateg,year):
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
            'layout':{
                'title': "AGE BY NUMBER OF DISABILITIES".title()
            }
        }

@app.callback(
    Output("emplStatus","figure"),[
        Input("states",'value'),
        Input("year","value")
    ]
)
def updateFigEmplStatus(states,years):
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
            'layout':{
                'title': "EMPLOYMENT STATUS".title()
            }
        }
    else:
        selectedExtendedDfs = toolz.dfSelector(toolz.dfSelector(toolz.dfSelector(usaData.dfsArray,'index',['EMPLOYMENT SECTOR']),'state',states),'year',[years[0]])
        df = dfs_sum([df['dataFrame'] for df in selectedExtendedDfs])
        trace = go.Pie(labels= df.columns.tolist(), values=df.iloc[0].tolist())
        return {
            'data':[trace],
            'layout':{
                'title': "EMPLOYMENT STATUS".title()
            }
        }


if __name__ == '__main__':
    
    app.run_server(debug=True)