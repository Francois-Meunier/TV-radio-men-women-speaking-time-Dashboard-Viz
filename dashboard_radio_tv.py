

import plotly_express as px

#for the dataset cleaning
import pandas as pd
import numpy as np


#for the map
import geoviews as gv
import geopandas as gpd #to read the geojson #conda install geopandas
from geoviews import dim

#to create the gorgraphic zones
from shapely.geometry import Polygon
from shapely.ops import cascaded_union

#for map interactions
gv.extension('bokeh') #bokeh as backend

import pandas.testing as tm

#for the dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc #for the navbar




#
# Data modified (in the notebook using jupyter)
#
df=pd.read_csv("https://git.esiee.fr/meunierf/python_dashboard/-/raw/master/processed_data.csv",error_bad_lines=False)
#df=pd.read_csv(r"C:\Users\loren\Desktop\Python_Dashboard\processed_data.csv")

df_zone = pd.read_csv("https://git.esiee.fr/meunierf/python_dashboard/-/raw/master/df_zone.csv",error_bad_lines=False)
#df_zone=pd.read_csv(r"C:\Users\loren\Desktop\Python_Dashboard\df_zone.csv")

sf=gpd.read_file("https://git.esiee.fr/meunierf/python_dashboard/-/raw/master/regions.geojson")
#sf=gpd.read_file(r"C:\Users\loren\Desktop\Python_Dashboard\regions.geojson")

#processing 

polygons_A = [sf["geometry"][2], #27
              sf["geometry"][8], #75
              sf["geometry"][10]] #84

polygons_B = [sf["geometry"][1], #24
              sf["geometry"][3], #28
              sf["geometry"][4], #32
              sf["geometry"][5], #44
              sf["geometry"][6], #52
              sf["geometry"][7], #53
              sf["geometry"][11]] #93

polygons_C = [sf["geometry"][0], #11
              sf["geometry"][9]] #76

u_A = cascaded_union(polygons_A)
u_B = cascaded_union(polygons_B)
u_C = cascaded_union(polygons_C)

sf_zone = sf[:3]
sf_zone = sf_zone.drop(['code'], axis=1)
sf_zone['nom'] = ["A", "B", "C"]
sf_zone['geometry'] = [u_A, u_B, u_C]

sf_zone['value'] = [df_zone["Zone_A_male_p"][2], df_zone["Zone_B_male_p"][2], df_zone["Zone_C_male_p"][2]]

deps = gv.Polygons(sf_zone, vdims=['nom','value'])
#input for the first layout
Year= 2011
Month = 11
Day= 22
#
# Main
#

#for the navbar
navbar = dbc.NavbarSimple(
    brand="Répartition du temps de paroles à la radio et à la télévision, hommes et femmes",
    brand_href="",
    color="primary",
    dark=True)

if __name__ == '__main__':
    
    #definition of the app with the dash themes we decided
    app = dash.Dash(external_stylesheets=["https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/sandstone/bootstrap.min.css"]) # (3)

    dg = df.loc[(df["year"] == Year) & (df["month"] == Month) & (df["day"] == Day)]

    #definition of the diferent graphs that will be plot in the dashboard page
    fig1 = px.histogram(dg, x="female_percent",
                        color="media_type",)
    fig2 = px.histogram(dg, x="male_percent",
                        color="media_type",)
    fig3 = px.bar(dg, x="channel_name", y=["female_percent","male_percent","music_percent"])
    fig4 = px.choropleth(df_zone,geojson=sf)
    fig4.update_geos(fitbounds="locations", visible=False)

    #creation of the different layout of the page with sliders,dropdowns and graphs
    app.layout = html.Div(style={'textAlign': 'center'},children=[

                            navbar,
                            html.Label('Année'),
                            dcc.Slider( 
                                id='year-slider',
                                min=2001,
                                max=2018,
                                step=1,
                                value=Year,
                                marks={
                                    str(year): str(year) for year in df['year'].unique()
                                }
                            ),
                            html.Label('Mois'),
                            dcc.Slider(
                                id='month-slider',
                                min=1,
                                max=12,
                                step=1,
                                value=Month,
                                marks={
                                    str(month): str(month) for month in df['month'].unique()
                                }
                            ),
                            html.Label('Jour'),
                            dcc.Slider(
                                id='day-slider',
                                min=1,
                                max=31,
                                step=1,
                                value=Day,
                                marks={
                                    str(day): str(day) for day in df['day'].unique()
                                }
                            ),
                            html.Label("Nombre d\'heure en fonction du pourcentage de paroles"),
                            dcc.Graph(
                                id='graph1',
                                figure=fig1
                            ),
                            dcc.Graph(
                                id='graph2',
                                figure=fig2
                            ),

                            html.Div(children=f'''
                                Ces graphiques montrent que le temps de paroles des femmes et plus faibles que le temps de paroles des hommes en moyenne
                                
                                
                            '''),
                            dcc.Dropdown(
                                id='media_dropdown',
                                options=[
                                    {'label': 'Radio', 'value': 'radio'},
                                    {'label': 'Télévision', 'value': 'tv'}
                                ],
                                value='radio'
                            ),
                            html.Label("Nombre d'heure pour chaque radio ou chaîne de télévision, séparé en fonctions des hommes,femmes et de la musique"),
                            dcc.Graph(
                                id='graph3',
                                figure=fig3
                            ),
                            dcc.Dropdown(
                                id='mfm_dropdown',
                                options=[
                                    {'label': 'Homme', 'value': 'male_p'},
                                    {'label': 'Femme', 'value': 'female_p'},
                                    {'label': 'Musique', 'value': 'music_p'}
                                ],
                                value='male_p'
                            ),
                            dcc.Dropdown(
                                id='year_dropdown',
                                options=[
                                    {'label': '2001', 'value': 0},
                                    {'label': '2002', 'value': 1},
                                    {'label': '2003', 'value': 2},
                                    {'label': '2004', 'value': 3},
                                    {'label': '2005', 'value': 4},
                                    {'label': '2006', 'value': 5},
                                    {'label': '2007', 'value': 6},
                                    {'label': '2008', 'value': 7},
                                    {'label': '2009', 'value': 8},
                                    {'label': '2010', 'value': 9},
                                    {'label': '2011', 'value': 10},
                                    {'label': '2012', 'value': 11},
                                    {'label': '2013', 'value': 12},
                                    {'label': '2014', 'value': 13},
                                    {'label': '2015', 'value': 14},
                                    {'label': '2016', 'value': 15},
                                    {'label': '2017', 'value': 16},
                                    {'label': '2018', 'value': 17},
                                    {'label': '2019', 'value': 18}
                                ],
                                value=0
                            ),
                            dcc.Graph(
                                id='graph4',
                                figure=fig4
                            ),

                            html.Div(children=f'''
                                Cette carte montre que la plus part du temps toutes les zones ont un temps de paroles équivalent et que le temps de paroles des hommes et en moyenne beaucoup plus élevé
                            '''),
                            
                            
                            
                            

    ]
    )
    #function callback that defines each output and input, that will be refreshed or be used to refresh the page with different value
    @app.callback(
        [Output('graph1', 'figure'),
        Output('graph2', 'figure'),
        Output('graph3', 'figure'),
        Output('graph4', 'figure')
        ],
        [Input('year-slider', 'value'),
         Input('month-slider', 'value'),
         Input('day-slider', 'value'),
         Input('media_dropdown', 'value'),
         Input('mfm_dropdown', 'value'),
         Input('year_dropdown', 'value')])
         
    #this function is called when an input is modified and change the output of graphs that are to be changed 
    def update_figure(year_slider,month_slider,day_slider,media_dropdown,mfm_dropdown,year_dropdown):

        dg=df.loc[(df["year"] == year_slider) & (df["month"] == month_slider) & (df["day"] == day_slider)]

        fig1 = px.histogram(dg, x="female_percent",
                        color="media_type",)

        fig2 = px.histogram(dg, x="male_percent",
                        color="media_type",)

        fig3 = px.bar(dg.loc[(dg["media_type"] == media_dropdown)], x="channel_name", y=["female_percent","male_percent","music_percent"])
        
        #the definition of the new dataframe for the map
        sf_zone['value'][0] = df_zone["Zone_A_"+mfm_dropdown][year_dropdown]
        sf_zone['value'][1] = df_zone["Zone_B_"+mfm_dropdown][year_dropdown]
        sf_zone['value'][2] = df_zone["Zone_C_"+mfm_dropdown][year_dropdown]

        fig4 = px.choropleth(sf_zone,
                            geojson=sf_zone.geometry,
                            locations=sf_zone.index,
                            color='value',
                            scope="europe",
                            title = "Proportions par zones de vacances",
                            hover_name="nom")
        fig4.update_geos(fitbounds="locations", visible=False)

        return (fig1,fig2,fig3,fig4)

    #to run the server
    app.run_server(debug=True)
