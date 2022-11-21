#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import pandas_gbq

from google.cloud import bigquery

import dash

import dash_bootstrap_components as dbc

from dash import dcc, html

from dash.dependencies import Input, Output

from datetime import datetime

from pyorbital.orbital import Orbital

import plotly.graph_objects as go


# In[2]:


api_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


# In[3]:

client = bigquery.Client()

query_string = "SELECT * FROM `leo-satellite-overview-project.dataset.active satellites table` "

df = pandas_gbq.read_gbq(query_string, project_id = 'leo-satellite-overview-project')


# In[ ]:


df_1 = df['YearOfLaunch'].value_counts().rename_axis('YearOfLaunch').reset_index(name = 'Counts')


# In[ ]:


df_1 = df_1.sort_values(by = ['YearOfLaunch'])


# In[7]:


df_2 = df.groupby('YearOfLaunch')['Purpose'].value_counts().rename_axis(['YearOfLaunch','Purpose']).reset_index(name = 'Counts')


# In[8]:


def make_break(num_breaks):
    
    br_list = ([html.Br()]*num_breaks)
    
    return br_list


# In[26]:


_app = dash.Dash(__name__, external_stylesheets = [dbc.themes.GRID])

app = _app.server

_app.layout = html.Div([
    
    dcc.Interval(
        
        id = 'interval-component',
        
        interval = 10*1000
        
    ),
    
    dbc.Row([dbc.Col([html.Div([

        html.H1('Overview of Active Satellites in Low Earth Orbit',
        
        style = {'textAlign':'center', 'font-family':'Open Sans'})


    ])


    ], md = 12)


    ]),
    
    html.Div(make_break(1)),
    
    dbc.Row([dbc.Col([html.Div([
        
        html.Span(str(df['ObjectName'].count()),
                  
                  style = {'font-family':'Open Sans', 'font-size':'34px', 'color':'rgb(96,96,96)'}
    
    ),
        
        html.Div(make_break(2)),
        
        
        html.Span('active satellites in Low Earth Orbit ',
                  
                  style = {'font-family':'Open Sans', 'font-size':'13.6px', 'color':'rgb(96,96,96)'}
        
        )
        
        
        
    ], style = {'background-color': 'rgb(255,255,255)', 'padding': '4px'})
        
        
    ], md = 1)
            
            ]),
    
    html.Div(make_break(2)),
    
    dbc.Row([dbc.Col([html.Div([
        
        html.Label('Search for a satellite',
                  
                  style = {'font-family':'Open Sans', 'font-size':'16px', 'color':'rgb(96,96,96)'}),
        
        html.Div(make_break(1)),
        
        dcc.Dropdown(id = 'satellites dropdown',
                     
                     options = [{'label': i, 'value': i} for i in df['ObjectName'].unique()],
                     
                     value = df['ObjectName'][0],
                     
                     style = {'width':'25%','font-family':'Open Sans','color':'black'}
            
            
        )
    ])
        
        
    ])
            
            ]),
    
    html.Div(make_break(2)),
    
    dbc.Row([dbc.Col([html.Div(
        
        dcc.Graph(id = 'satellite map')
        
        
    )
        
        
        
    ], md = 8),
             
             dbc.Col([html.Div(
             
             dcc.Graph(id = 'altitude chart'))
                     
                     ], md = 4),
             
            
            ]),
    
    html.Div(make_break(2)),
    
    dbc.Row([dbc.Col([html.Div(
        
    )
                      
                     ], md = 8),
             
             dbc.Col([html.Div([
                 
                 html.Label('Select a Year',
                            
                            style = {'font-family':'Open Sans', 'font-size':'16px', 'color':'rgb(96,96,96)'}),
                 
                 html.Div(make_break(1)),
                 
                 dcc.Dropdown(id = 'year of launch dropdown',
                              
                              options = [{'label': i, 'value': i} for i in df['YearOfLaunch'].unique()],
                              
                              value = df['YearOfLaunch'][df.index[-1]],
                              
                              style = {'width':'30%','font-family':'Open Sans','color':'black'})
             
             ])
                     
                     ], md = 4)
            
            ]),
    
    html.Div(make_break(2)),
    
    dbc.Row([dbc.Col([html.Div(
        
        dcc.Graph(
            
            figure = go.Figure([go.Bar(x = df_1['YearOfLaunch'], 
                                       
                                       y = df_1['Counts'], marker_color = 'rgb(99,110,250)')]).update_layout(margin = dict(l = 20, r = 20, t = 20, b = 20),
                                                                                     
                                                                                     plot_bgcolor = 'rgb(255,255,255)',paper_bgcolor='rgb(255,255,255)', title = {'text':'Count of Active Low Earth Orbit Satellites vs Year of Launch','x':0.5, 'y':0.98},
                                                                                     
                                                                                     height = 700).update_yaxes(gridcolor = 'rgb(243,243,243)', 
                                                                                                                
                                                                                                                title ='Counts').update_xaxes(title = 'Year', linecolor = 'rgb(243,243,243)')
        
        )
    
    
    )
        
        
    ], md = 8),
             
             dbc.Col([html.Div(
                 
                 dcc.Graph(
                     
                     id = 'satellite purpose pie chart'
                 
                 )
             
             
             )
                     
                     ], md = 4),
        
        
    ])
    
    
   

])



@_app.callback(
    
    Output('satellite purpose pie chart', 'figure'),
    
    Input('year of launch dropdown', 'value'))

def plot_piechart(year):
    
    df_3 = df_2[df_2['YearOfLaunch'] == year]
    
    colors = {'colors':['rgb(99,110,250)', 'rgb(239,85,59)', 'rgb(255,215,0)',
                               
                               'rgb(171,99,250)', 'rgb(0,204,150)', 'rgb(255,140,0)']}
    
    fig = go.Figure(data = [go.Pie(labels = df_3['Purpose'].unique(), values = df_3['Counts'])])
    
    fig.update_layout(height = 700, title = {'text':'Proportion of Active Low Earth Orbit Satellites by Purpose','x':0.5, 'y':0.98})
    
    fig.update_traces(textinfo = 'label+value', textfont_size = 20, textfont_color = 'rgb(0,0,0)',
                     
                     marker = colors)
    
    return fig

@_app.callback(
    
    Output('satellite map', 'figure'),
    
    Output('altitude chart', 'figure'),
    
    Input('interval-component', 'n_intervals'),
    
    Input('satellites dropdown', 'value'))

def plot_map(n, satellite_name):
    
    try:

        time = datetime.now()

        orb = Orbital(satellite_name)

        lon, lat = orb.get_lonlatalt(time)[0], orb.get_lonlatalt(time)[1]
        
        lon_list = [lon]

        lat_list = [lat]

        obj_name_list = [satellite_name]

        time_list = [time-timedelta(minutes = i) for i in range(121)]

        alt_list = [orb.get_lonlatalt(i)[2] for i in time_list]
        
        df_4 = pd.DataFrame({'ObjectName': obj_name_list, 'Latitude': lat_list, 'Longitude': lon_list})
        
        df_5 = pd.DataFrame({'TimeStamp': time_list, 'Altitude': alt_list})

        lon_list.clear()

        lat_list.clear()

        alt_list.clear()
        
        time_list.clear()
        
        obj_name_list.clear()

        df_4_copy = df_4.copy()
        
        df_5_copy = df_5.copy()

        fig =go.Figure(go.Scattermapbox(

            lat = df_4_copy['Latitude'], lon = df_4_copy['Longitude'], marker = {'size': 20, 'symbol':'rocket'},

            hovertext = df_4_copy['ObjectName'],


        )
                      )

        fig.update_layout(

        mapbox = {'accesstoken':api_token,

                 'style': 'light', 'zoom': 0,

                 },

        margin = dict(l = 0, r =0, t = 0, b = 0),

        height = 800, hovermode = 'closest')
        
        fig2 = go.Figure(go.Scatter(x = df_5_copy['TimeStamp'], y = df_5_copy['Altitude']))
        
        fig2.update_layout(margin = dict(l = 20, r = 20, t = 20, b = 20),
                          
                          plot_bgcolor = 'rgb(255,255,255)', paper_bgcolor = 'rgb(255,255,255)',
                          
                          height = 800, title = {'text': 'Altitude Trend of' + ' ' + str(satellite_name) + ' ' + 'in near real time', 'x':0.5, 'y':0.98}, 
                          
                          ).update_yaxes(gridcolor = 'rgb(243,243,243)', title ='Altitude (km)').update_xaxes(title = 'Timestamp', linecolor = 'rgb(243,243,243)')
        
        
        
        return fig, fig2
    
    except NotImplementedError:
        
        pass
    
if __name__ == '__main__':

    _app.run_server(debug=True)


# In[ ]:




