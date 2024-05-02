import dash
from dash import Dash, html, dcc, dash_table,callback
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('./climate_df.csv')
df_new = pd.read_csv('./totals_df.csv')


df['non_lume'] = 100-(df['moon_illumination_num'])


####################################### line graph_lunar_wave

fig=px.bar(df[df['city']=='Dao'], 
                     x='date', 
                     y='moon_illumination_num',
                     color_discrete_sequence=['#fbf5d7'],
                     hover_name='moon_phase',
                     height=600, width=800)

fig.add_trace(px.line(df[df['city']=='Dao'], 
                      x='date', 
                      y='moon_illumination_num',
                      color_discrete_sequence=['#fbf5d7']).data[0])

fig.update_layout(plot_bgcolor= '#afb9c5', showlegend=False)
fig.update_yaxes(showgrid=False)
fig.update_traces(marker_line_width=0)
fig.update_layout(
    title="Annual Lunar Cycle",
    yaxis_title=''
)
graph_lunar_wave = dcc.Graph(figure=fig)

####################################### moving graph_lunar_bar

fig = px.bar(df[df['city']=='Dao'], 
             x=['moon_illumination_num','non_lume'], 
             y='city',
             color_discrete_sequence=['#fbf5d7', '#afb9c5'],
             hover_name="moon_phase",
             hover_data={},
             animation_frame='date',
             labels={'value': 'Illumination (%)'},
             #title='Moon Illumination Through The Year',
             height=350, width=800)

fig.update_layout(plot_bgcolor= '#afb9c5',barmode='stack', showlegend=False)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
fig.update_traces(marker_line_width=0)

graph_lunar_bar = dcc.Graph(figure=fig)

####################################### PRECIP TABLE

df_precip = df_new.sort_values(by='overall_precip_mm')[['city','country','overall_precip_mm', 
                                                        'maxprecip_day_mm','total_precip_days']]

df_precip['Total Precip (mm)'] = round(df_precip['overall_precip_mm'],2)
df_precip['max. Daily Precip (mm)'] = round(df_precip['maxprecip_day_mm'],2)
df_precip['Total Precip Days'] = df_precip['total_precip_days'] 

df_precip = df_precip[['city','country','Total Precip (mm)', 'max. Daily Precip (mm)', 'Total Precip Days']]

precip_table = dash_table.DataTable(df_precip.to_dict('records'),
                               [{"name": i, "id": i} for i in df_precip.columns],
                              style_data={'color': 'black','backgroundColor': '#fcebed'},
                              style_header={
                                  'backgroundColor': '#afb9c5',
                                  'color': 'black','fontWeight': 'bold'}, 
                                     style_table={
                                         'minHeight': '400px', 'height': '400px', 'maxHeight': '400px',
                                         'minWidth': '900px', 'width': '900px', 'maxWidth': '900px', 
                                         'marginLeft': 'auto', 'marginRight': 'auto',
                                     'marginTop': 'auto', 'marginBottom': 'auto'} 
                                     )
                               

####################################### SELECTOR

cities = df['city'].unique().tolist() 

dropdown = dcc.Dropdown(['Ansbach','Argos','Bedburg','Dao','Lerwick',
                         'London','Marvejols','Morgan City','Pamir Post','Window Rock'], 
                        'Ansbach', clearable=False)


radio= dcc.RadioItems(id="city",
                      options=['Ansbach','Argos','Bedburg','Dao',
                               'Lerwick','London','Marvejols',
                               'Morgan City','Pamir Post','Window Rock'], 
                      value='Ansbach', 
                      inline=True, 
                      style ={'paddingLeft': '30px'})


####################################### City line rain

fig = px.line(df, x='date', y='totalprecip_mm', color='city')
fig.update_layout(
    title="All Cities Annually: Daily Rainfall",
    yaxis_title=''
)
graph_precip_line=dcc.Graph(figure=fig)

####################################### World Map

scaler = MinMaxScaler()

df_new['scaled_precip'] = scaler.fit_transform(df_new[['overall_precip_mm']])
df_new['scaled_precip'] = round(df_new['scaled_precip'],2)

alpha = df_new['scaled_precip']

fig = px.scatter_mapbox(df_new, 
                        lat="lat", lon="lon", 
                        hover_name="city",
                        hover_data=["total_precip_days",'overall_precip_mm','lat','lon'],
                        size="total_precip_days",
                        color="overall_precip_mm",
                        color_continuous_scale='Burg', 
                        opacity=alpha,
                        labels='city',
                        zoom=1, center={'lat': 40.910000, 'lon': 3.831000},
                        mapbox_style='carto-positron')
fig.update_layout(
    title="Precipitation Days and Volume")

graph_precip_globe = dcc.Graph(figure=fig)

####################################### TEMP TABLE

df_temp = df_new.sort_values(by='overall_avgtemp')[['city','country','overall_maxtemp',
                                                    'overall_avgtemp', 'overall_mintemp']]
df_temp['max. Temp'] = round(df_temp['overall_maxtemp'],2)
df_temp['avg. Temp'] = round(df_temp['overall_avgtemp'],2)
df_temp['min. Temp'] = round(df_temp['overall_mintemp'],2)

df_temp = df_temp[['city','country','max. Temp', 'avg. Temp', 'min. Temp']]

temp_table = dash_table.DataTable(df_temp.to_dict('records'),
                               [{"name": i, "id": i} for i in df_temp.columns],
                              style_data={'color': 'black','backgroundColor': '#fcebed'},
                              style_header={
                                  'backgroundColor': '#afb9c5',
                                  'color': 'black','fontWeight': 'bold'}, 
                                     style_table={
                                         'minHeight': '400px', 'height': '400px', 'maxHeight': '400px',
                                         'minWidth': '900px', 'width': '900px', 'maxWidth': '900px', 
                                         'marginLeft': 'auto', 'marginRight': 'auto',
                                     'marginTop': 'auto', 'marginBottom': 'auto'} 
                                     )

####################################### DROPDOWN2

dropdown2 = dcc.Dropdown(['Ansbach','Argos','Bedburg','Dao','Lerwick',
                         'London','Marvejols','Morgan City','Pamir Post','Window Rock'], 
                        'Ansbach', clearable=False)

####################################### Heat Lines

pamir_stripes = df[df['city']=='Pamir Post']
pamir_stripes = pd.pivot_table(pamir_stripes, values='avgtemp_c', index=['date'])

fig = px.imshow(
    pamir_stripes.T,  # Transpose the DataFrame for proper orientation
    labels=dict(x="Date", y='Avg Daily Temperature', color="Temperature"),
    color_continuous_scale='RdBu_r',  # Choose a diverging color scale
    color_continuous_midpoint=0,
)

fig.update_layout(
    title="City Temperatures",
    yaxis_title=''
)

graph_heat_stripes = dcc.Graph(figure=fig)

####################################### VIS TABLE

df_vis = df_new.sort_values(by='overall_avg_vis_km')[['city','country','maxvis_day_km',
                                                   'overall_avg_vis_km', 'mnth_minvis_day_km']]
df_vis['max. daily vis (km)'] = round(df_vis['maxvis_day_km'],2)
df_vis['avg. vis (km)'] = round(df_vis['overall_avg_vis_km'],2)
df_vis['min. daily vis (km)'] = round(df_vis['mnth_minvis_day_km'],2)

df_vis = df_vis[['city','country','max. daily vis (km)', 'avg. vis (km)', 'min. daily vis (km)']]


vis_table = dash_table.DataTable(df_vis.to_dict('records'),
                               [{"name": i, "id": i} for i in df_vis.columns],
                              style_data={'color': 'black','backgroundColor': '#fcebed'},
                              style_header={
                                  'backgroundColor': '#afb9c5',
                                  'color': 'black','fontWeight': 'bold'}, 
                                     style_table={
                                         'minHeight': '400px', 'height': '400px', 'maxHeight': '400px',
                                         'minWidth': '900px', 'width': '900px', 'maxWidth': '900px', 
                                         'marginLeft': 'auto', 'marginRight': 'auto',
                                     'marginTop': 'auto', 'marginBottom': 'auto'} 
                                     )


####################################### DROPDOWN3

dropdown3 = dcc.Dropdown(['Ansbach','Argos','Bedburg','Dao','Lerwick',
                         'London','Marvejols','Morgan City','Pamir Post','Window Rock'], 
                        'Ansbach', clearable=False)

####################################### VISIBILITY

ansbach_df = df[df['city']=='Ansbach']

fig = go.Figure()
fig.add_trace(go.Bar(
    x=ansbach_df['date'],
    y=ansbach_df['wk_maxvis_day'] - ansbach_df['wk_minvis_day'],
    base=ansbach_df['wk_minvis_day'],
    name='Visibility Range',
    marker_color= '#fbf5d7',
    opacity=0.8),
    )
fig.update_layout(plot_bgcolor= '#c2c9d4')
fig.update_yaxes(showgrid=False)
fig.update_traces(marker_line_width=0)

fig.add_trace(go.Scatter(
        x=ansbach_df['date'],
        y=ansbach_df['avgvis_km'],
        mode='lines+markers',
        name='Daily Visibility',
        line=dict(color='#d8c073', width=1.6),
        marker=dict(color='#d8c073', size=2),
        hoverinfo='y+name'
    ))
fig.update_layout(
    title="Annual Visibility",
    xaxis_title='Date',
    yaxis_title='Visibility in km'
)
graph_vis_range = dcc.Graph(figure=fig)

####################################### RUNNING APP


app =dash.Dash(external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div([html.H1('Werewolf Weather', 
                               style={'textAlign': 'center', 'color': '#b34b6e'}), 
                       html.H2("Here To Help With Your Werewolf Weather Needs!",
                               style ={'textAlign': 'center', 'color':'#70656a'}),
                       html.Div([html.Div('ANNUAL REVIEW', 
                                          style={'paddingLeft': '45px','backgroundColor': '#b34b6e', 
                                                 'color': 'white', 
                                                 'width': 'What Does The Lunar Cycle Look Like?'}),
                                 graph_lunar_wave, 
                                 graph_lunar_bar,
                                 radio,
                                 graph_precip_line, 
                                 graph_precip_globe,
                                 precip_table,
                                 dropdown3,
                                 graph_vis_range,
                                 vis_table,
                                 dropdown2, 
                                 graph_heat_stripes,
                                 temp_table])])

####################################### precip_lines CALLBACK

#@callback(
#    Output(graph_precip_line, "figure"), 
#    Input(dropdown, "value"))

@callback(
    Output(graph_precip_line, "figure"), 
    Input("city", "value"))

def update_precip_lines(city): 
    mask = df['city'] == city
    #mask = df["city"].isin(cities) # coming from the function parameter
    fig = px.line(df[mask], x='date', y='totalprecip_mm', color='city',
                  color_discrete_map = {'Ansbach': '#2b9e79', 'Argos': '#8690FF', 'Bedburg': '#f19c4d',
                                        'Dao':'#e5244b','Lerwick':'#8155c2','London':'#3aa544',
                                        'Marvejols':'#feb04b', 'Morgan City':'#188eb5', 'Pamir Post':'#ca65bd',
                                        'Window Rock':'#f3455b'})
    fig.update_layout(title = f"{city} Precipitation", yaxis_title='Precipitation in mm')
    fig.update_layout(yaxis_range=[0, 94])
    return fig 

####################################### heat_stripes CALLBACK

@callback(
    Output(graph_heat_stripes, "figure"), 
    Input(dropdown2, "value"))

def update_stripes(city): 
    mask = df['city'] == city
    stripes = df[mask]
    stripes = pd.pivot_table(stripes, values='avgtemp_c', index=['date'])
    fig = px.imshow(
        stripes.T,  
        labels=dict(x="Date", y='Avg Daily Temperature', color="Temperature"),
        color_continuous_scale='RdBu_r',  
        #color_continuous_midpoint=8,
    )
    fig.update_layout(
        title="Temperature",
        yaxis_title='',
        coloraxis_colorbar=dict(
            tickvals=[-40, -20, 0, 20, 40, 60],
            ticktext=[-40, -20, 0, 20, 40, 60]
        ))
    fig.update_layout(
        title=f"{city} Temperature",
        yaxis_title=''
    )
    return fig 

####################################### vis_range CALLBACK

@callback(
    Output(graph_vis_range, "figure"), 
    Input(dropdown3, "value"))

def update_vis_range(city): 
    mask = df['city'] == city
    city_df = df[mask]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = city_df['date'],
        y = city_df['wk_maxvis_day'] - city_df['wk_minvis_day'],
        base = city_df['wk_minvis_day'],
        name='Visibility Range',
        marker_color= '#fbf5d7',
        opacity=0.8),
                 )
    fig.update_layout(plot_bgcolor= '#c2c9d4')
    fig.update_yaxes(showgrid=False)
    fig.update_traces(marker_line_width=0)
    
    fig.add_trace(go.Scatter(
        x = city_df['date'],
        y = city_df['avgvis_km'],
        mode='lines+markers',
        name='Daily Visibility',
        line=dict(color='#d8c073', width=1.6),
        marker=dict(color='#d8c073', size=2),
        hoverinfo='y+name'
    ))
    fig.update_layout(
        title = f'{city} Visibility',
        xaxis_title = 'Date',
        yaxis_title= 'Visibility in km'
    )
    return fig 

#######################################

if __name__ == '__main__':
     app.run_server()