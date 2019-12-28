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
categToAgeCateg = {ageSexe04["Sensoriel"].df.index.values.tolist().index(categ): '{}'.format(categ) for categ in ageSexe04["Sensoriel"].df.index.values.tolist()}


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Create controls
county_options = [
    {"label": str(COUNTIES[county]), "value": str(county)} for county in COUNTIES
]

well_status_options = [
    {"label": str(WELL_STATUSES[well_status]), "value": str(well_status)}
    for well_status in WELL_STATUSES
]

well_type_options = [
    {"label": str(WELL_TYPES[well_type]), "value": str(well_type)}
    for well_type in WELL_TYPES
]


# Load data
df = pd.read_csv(DATA_PATH.joinpath("wellspublic.csv"), low_memory=False)
df["Date_Well_Completed"] = pd.to_datetime(df["Date_Well_Completed"])
df = df[df["Date_Well_Completed"] > dt.datetime(1960, 1, 1)]

trim = df[["API_WellNo", "Well_Type", "Well_Name"]]
trim.index = trim["API_WellNo"]
dataset = trim.to_dict(orient="index")

points = pickle.load(open(DATA_PATH.joinpath("points.pkl"), "rb"))


# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Disability statistics",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Morocco - United States Of America", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
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
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="well_text"), html.P("No. of Wells")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="gasText"), html.P("Gas")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="oilText"), html.P("Oil")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="waterText"), html.P("Water")],
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="sexAge")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
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
        html.Div(
            [
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
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)



# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("sexAge", "figure")],
)



"""
@app.callback(
    Output("aggregate_data", "data"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
)
def update_production_text(well_statuses, well_types, year_slider):

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)
    selected = dff["API_WellNo"].values
    index, gas, oil, water = produce_aggregate(selected, year_slider)
    return [human_format(sum(gas)), human_format(sum(oil)), human_format(sum(water))]


# Radio -> multi
@app.callback(
    Output("well_statuses", "value"), [Input("well_status_selector", "value")]
)
def display_status(selector):
    if selector == "all":
        return list(WELL_STATUSES.keys())
    elif selector == "active":
        return ["AC"]
    return []


# Radio -> multi
@app.callback(Output("well_types", "value"), [Input("well_type_selector", "value")])
def display_type(selector):
    if selector == "all":
        return list(WELL_TYPES.keys())
    elif selector == "productive":
        return ["GD", "GE", "GW", "IG", "IW", "OD", "OE", "OW"]
    return []


# Slider -> count graph
@app.callback(Output("year_slider", "value"), [Input("count_graph", "selectedData")])
def update_year_slider(count_graph_selected):

    if count_graph_selected is None:
        return [1990, 2010]

    nums = [int(point["pointNumber"]) for point in count_graph_selected["points"]]
    return [min(nums) + 1960, max(nums) + 1961]


# Selectors -> well text
@app.callback(
    Output("well_text", "children"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
)
def update_well_text(well_statuses, well_types, year_slider):

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)
    return dff.shape[0]


@app.callback(
    [
        Output("gasText", "children"),
        Output("oilText", "children"),
        Output("waterText", "children"),
    ],
    [Input("aggregate_data", "data")],
)
def update_text(data):
    return data[0] + " mcf", data[1] + " bbl", data[2] + " bbl"


# Selectors -> main graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
    [State("lock_selector", "value"), State("main_graph", "relayoutData")],
)
def make_main_figure(
    well_statuses, well_types, year_slider, selector, main_graph_layout
):

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    traces = []
    for well_type, dfff in dff.groupby("Well_Type"):
        trace = dict(
            type="scattermapbox",
            lon=dfff["Surface_Longitude"],
            lat=dfff["Surface_latitude"],
            text=dfff["Well_Name"],
            customdata=dfff["API_WellNo"],
            name=WELL_TYPES[well_type],
            marker=dict(size=4, opacity=0.6),
        )
        traces.append(trace)

    # relayoutData is None by default, and {'autosize': True} without relayout action
    if main_graph_layout is not None and selector is not None and "locked" in selector:
        if "mapbox.center" in main_graph_layout.keys():
            lon = float(main_graph_layout["mapbox.center"]["lon"])
            lat = float(main_graph_layout["mapbox.center"]["lat"])
            zoom = float(main_graph_layout["mapbox.zoom"])
            layout["mapbox"]["center"]["lon"] = lon
            layout["mapbox"]["center"]["lat"] = lat
            layout["mapbox"]["zoom"] = zoom

    figure = dict(data=traces, layout=layout)
    return figure


# Main graph -> individual graph
@app.callback(Output("individual_graph", "figure"), [Input("main_graph", "hoverData")])
def make_individual_figure(main_graph_hover):

    layout_individual = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            "points": [
                {"curveNumber": 4, "pointNumber": 569, "customdata": 31101173130000}
            ]
        }

    chosen = [point["customdata"] for point in main_graph_hover["points"]]
    index, gas, oil, water = produce_individual(chosen[0])

    if index is None:
        annotation = dict(
            text="No data available",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_individual["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                name="Gas Produced (mcf)",
                x=index,
                y=gas,
                line=dict(shape="spline", smoothing=2, width=1, color="#fac1b7"),
                marker=dict(symbol="diamond-open"),
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Oil Produced (bbl)",
                x=index,
                y=oil,
                line=dict(shape="spline", smoothing=2, width=1, color="#a9bb95"),
                marker=dict(symbol="diamond-open"),
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Water Produced (bbl)",
                x=index,
                y=water,
                line=dict(shape="spline", smoothing=2, width=1, color="#92d8d8"),
                marker=dict(symbol="diamond-open"),
            ),
        ]
        layout_individual["title"] = dataset[chosen[0]]["Well_Name"]

    figure = dict(data=data, layout=layout_individual)
    return figure


# Selectors, main graph -> aggregate graph
@app.callback(
    Output("aggregate_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
        Input("main_graph", "hoverData"),
    ],
)
def make_aggregate_figure(well_statuses, well_types, year_slider, main_graph_hover):

    layout_aggregate = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            "points": [
                {"curveNumber": 4, "pointNumber": 569, "customdata": 31101173130000}
            ]
        }

    chosen = [point["customdata"] for point in main_graph_hover["points"]]
    well_type = dataset[chosen[0]]["Well_Type"]
    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    selected = dff[dff["Well_Type"] == well_type]["API_WellNo"].values
    index, gas, oil, water = produce_aggregate(selected, year_slider)

    data = [
        dict(
            type="scatter",
            mode="lines",
            name="Gas Produced (mcf)",
            x=index,
            y=gas,
            line=dict(shape="spline", smoothing="2", color="#F9ADA0"),
        ),
        dict(
            type="scatter",
            mode="lines",
            name="Oil Produced (bbl)",
            x=index,
            y=oil,
            line=dict(shape="spline", smoothing="2", color="#849E68"),
        ),
        dict(
            type="scatter",
            mode="lines",
            name="Water Produced (bbl)",
            x=index,
            y=water,
            line=dict(shape="spline", smoothing="2", color="#59C3C3"),
        ),
    ]
    layout_aggregate["title"] = "Aggregate: " + WELL_TYPES[well_type]

    figure = dict(data=data, layout=layout_aggregate)
    return figure


# Selectors, main graph -> pie graph
@app.callback(
    Output("pie_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
)
def make_pie_figure(well_statuses, well_types, year_slider):

    layout_pie = copy.deepcopy(layout)

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    selected = dff["API_WellNo"].values
    index, gas, oil, water = produce_aggregate(selected, year_slider)

    aggregate = dff.groupby(["Well_Type"]).count()

    data = [
        dict(
            type="pie",
            labels=["Gas", "Oil", "Water"],
            values=[sum(gas), sum(oil), sum(water)],
            name="Production Breakdown",
            text=[
                "Total Gas Produced (mcf)",
                "Total Oil Produced (bbl)",
                "Total Water Produced (bbl)",
            ],
            hoverinfo="text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(colors=["#fac1b7", "#a9bb95", "#92d8d8"]),
            domain={"x": [0, 0.45], "y": [0.2, 0.8]},
        ),
        dict(
            type="pie",
            labels=[WELL_TYPES[i] for i in aggregate.index],
            values=aggregate["API_WellNo"],
            name="Well Type Breakdown",
            hoverinfo="label+text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(colors=[WELL_COLORS[i] for i in aggregate.index]),
            domain={"x": [0.55, 1], "y": [0.2, 0.8]},
        ),
    ]
    layout_pie["title"] = "Production Summary: {} to {}".format(
        year_slider[0], year_slider[1]
    )
    layout_pie["font"] = dict(color="#777777")
    layout_pie["legend"] = dict(
        font=dict(color="#CCCCCC", size="10"), orientation="h", bgcolor="rgba(0,0,0,0)"
    )

    figure = dict(data=data, layout=layout_pie)
    return figure


# Selectors -> count graph
@app.callback(
    Output("count_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
)
def make_count_figure(well_statuses, well_types, year_slider):

    layout_count = copy.deepcopy(layout)

    dff = filter_dataframe(df, well_statuses, well_types, [1960, 2017])
    g = dff[["API_WellNo", "Date_Well_Completed"]]
    g.index = g["Date_Well_Completed"]
    g = g.resample("A").count()

    colors = []
    for i in range(1960, 2018):
        if i >= int(year_slider[0]) and i < int(year_slider[1]):
            colors.append("rgb(123, 199, 255)")
        else:
            colors.append("rgba(123, 199, 255, 0.2)")

    data = [
        dict(
            type="scatter",
            mode="markers",
            x=g.index,
            y=g["API_WellNo"] / 2,
            name="All Wells",
            opacity=0,
            hoverinfo="skip",
        ),
        dict(
            type="bar",
            x=g.index,
            y=g["API_WellNo"],
            name="All Wells",
            marker=dict(color=colors),
        ),
    ]

    layout_count["title"] = "Completed Wells/Year"
    layout_count["dragmode"] = "select"
    layout_count["showlegend"] = False
    layout_count["autosize"] = True

    figure = dict(data=data, layout=layout_count)
    return figure
"""

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


# Main
if __name__ == "__main__":
    app.run_server(debug=True)
