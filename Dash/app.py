import dash
import dash_core_components as dcc
import dash_html_components as html
from ETL.loader import EtlHcp04 
from pandasTesting import dfs_sum
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from itertools import chain

init= False
dfs = None
ageSexe04= None
sexeMatri04 = None
illitSexeEnvir = None
illitAgeSexe = None
educaEnvir = None
actEnv = None
actSexeEnv = None
def ETL():
    global init,dfs,ageSexe04,categToAgeCateg,sexeMatri04,illitSexeEnvir,illitAgeSexe,educaEnvir,actEnv,actSexeEnv
    if not init :
        print("--- RUNNING ETL ---")
        ETL = EtlHcp04()
        ageSexe04 = ETL.extendedDataFrames[0]
        sexeMatri04 = ETL.extendedDataFrames[1]
        illitSexeEnvir = ETL.extendedDataFrames[2]
        illitAgeSexe = ETL.extendedDataFrames[3]
        educaEnvir = ETL.extendedDataFrames[4]
        actEnv = ETL.extendedDataFrames[5]
        actSexeEnv = ETL.extendedDataFrames[6]
    else:
        print("Data has already been loaded")
        return dfs
ETL()
categToAgeCateg = {ageSexe04["Sensoriel"].df.index.values.tolist().index(categ): '{}'.format(categ) for categ in ageSexe04["Sensoriel"].df.index.values.tolist()}



### Dash CONFIG
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout=html.Div([
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






        dcc.Tab(label='Statistiques avancées', children=[
              
        html.Div(style={'padding': 15}),
        html.Div([
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
        dcc.Tab(label='Personnalisé', children=[

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



if __name__ == '__main__':
    
    app.run_server(debug=True)