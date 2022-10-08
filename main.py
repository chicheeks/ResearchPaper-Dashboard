# Creates MongoDb database from Jsonfile

# import pymongo
# import json
# from pymongo import MongoClient

# client = pymongo.MongoClient("mongodb+srv://chiamaka:Chiamaka2001@firstmongodb.geippvc.mongodb.net/?retryWrites=true&w=majority")
# db = client.jsondata
# collection = db.fordashboard

# with open('.\\jsondata.json','r', encoding='utf-8') as file:
#    file_data = json.load(file)

# if isinstance(file_data, list):
#    collection.insert_many(file_data)
# else:
#    collection.insert_one(file_data)


import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Output, Input
import pymongo
import plotly.express as px

# Connect to server on cloud
client = pymongo.MongoClient(
    "mongodb+srv://chiamaka:Chiamaka2001@firstmongodb.geippvc.mongodb.net/?retryWrites=true&w=majority")
# the database
datab = client['jsondata']
# the collection
collect = datab['fordashboard']

# Convert fordashboard collection (table) to a pandas DataFrame
data = pd.DataFrame(list(collect.find()))
if data["end_year"] is "":
    data["end_year"] = pd.to_datetime(data["end_year"], format="%Y")
    data.sort_values("end_year", inplace=True)
if data["topic"] is "":
    data["topic"] = "No topic"
if data["likelihood"] is "":
    data["likelihood"] = 0
if data["intensity"] is "":
    data["intensity"] = 0
if data["country"] is 0:
    data["country"] = "No country"

app = dash.Dash(__name__)
app.title = "My Dashboard"

# Dashboard layout
app.layout = html.Div(className="background",
                      children=[html.H1(className="title", children=["🌼 Visualise your Data 🌼"]),
                                    html.Div(className="container", children=[
                                        html.Div(children=[
                                            html.Div(className="dropdown", children=[html.Div(children="Topic"),
                                                                                     dcc.Dropdown(id='topic-filter',
                                                                                                  options=[
                                                                                                      {'label': topic,
                                                                                                       'value': topic}
                                                                                                      for topic in
                                                                                                      np.sort(
                                                                                                          data.topic.unique())
                                                                                                  ], value="oil",
                                                                                                  clearable=False
                                                                                                  )
                                                                                     ]),
                                        ]),
                                        html.Br(),
                                        html.Div(children=[
                                            html.Div(children=dcc.Graph(id='likelihood-topic-chart'),
                                                     ),
                                        ])
                                    ]),
                                    html.Div(className="container", children=[
                                        html.Div(children=[
                                            html.Div(className="dropdown", children=[html.Div(children="Pestle"),
                                                                                     dcc.Dropdown(id='pestle-filter',
                                                                                                  options=[
                                                                                                      {'label': pestle,
                                                                                                       'value': pestle}
                                                                                                      for pestle in
                                                                                                      np.sort(
                                                                                                          data.pestle.unique())
                                                                                                  ], value="Economic",
                                                                                                  clearable=False
                                                                                                  )
                                                                                     ]),
                                        ]),
                                        html.Br(),
                                        html.Div(children=[
                                            html.Div(children=dcc.Graph(id='intensity-start_year-chart'),
                                                     ),
                                        ])
                                    ]),
                                    html.Div(className="container", children=[
                                        html.Div(children=[
                                            html.Div(className="dropdown", children=[html.Div(children="Sector"),
                                                                                     dcc.Dropdown(id='sector-filter',
                                                                                                  options=[
                                                                                                      {'label': sector,
                                                                                                       'value': sector}
                                                                                                      for sector in
                                                                                                      np.sort(
                                                                                                          data.sector.unique())
                                                                                                  ],
                                                                                                  value="Energy",
                                                                                                  clearable=True
                                                                                                  )
                                                                                     ])
                                        ]),
                                        html.Br(),
                                        html.Div(children=[
                                            html.Div(children=dcc.Graph(id='source-relevance-chart'),
                                                     ),
                                        ])
                                    ])
                                ]
                      )


# ...
@app.callback(Output('likelihood-topic-chart', 'figure'),
              [Input('topic-filter', 'value')])
def likelihood_end_year(topic):
    filtered_data = data[(data['topic'] == topic)]
    likelihood_topic_figure = px.bar(filtered_data,
                                     x="end_year", y="likelihood",
                                     color='country',
                                     title="How likely is a topic?"
                                     )
    return likelihood_topic_figure


@app.callback(Output('intensity-start_year-chart', 'figure'),
              [Input('pestle-filter', 'value')])
def intensity_start_year(pestle):
    filtered_data = data[(data['pestle'] == pestle)]
    intensity_start_year_figure = px.bar(filtered_data,
                                         x="start_year", y="intensity",
                                         color="region",
                                         title="What is the intensity over the years?"
                                         )
    intensity_start_year_figure.update_xaxes(range=[2015, 2050])
    return intensity_start_year_figure


@app.callback(Output('source-relevance-chart', 'figure'),
              [Input('sector-filter', 'value')])
def source_relevance(sector):
    filtered_data = data[(data['sector'] == sector)]
    source_relevance_figure = px.bar(filtered_data,
                                     x="source", y="relevance",
                                     title="How relevant is the source?"
                                     )
    return source_relevance_figure


if __name__ == '__main__':
    app.run_server(debug=True)

# background, parent, container 1, container 2, dropdown
