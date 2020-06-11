import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import plotly.graph_objects as go
import seaborn as sns
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly_express as px

## DATA ##
death_df = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
    '/time_series_covid19_deaths_global.csv')
confirmed_df = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
    '/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
    '/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')

## CLEAN UP DATA ##
country_df.columns = map(str.lower, country_df.columns)
confirmed_df.columns = map(str.lower, confirmed_df.columns)
death_df.columns = map(str.lower, death_df.columns)
recovered_df.columns = map(str.lower, recovered_df.columns)

confirmed_df = confirmed_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
recovered_df = confirmed_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
death_df = death_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
country_df = country_df.rename(columns={'country_region': 'country'})

## SOME INTERESTING VALUES ##
confirmed_total = int(country_df['confirmed'].sum())
print('Confirmed Total is: ')
print(confirmed_total)
deaths_total = int(country_df['deaths'].sum())
print(('WorldWide Deaths:'))
print(deaths_total)
recovered_total = int(country_df['recovered'].sum())
print('WorldWide Recovered')
print(deaths_total)
active_total = int(country_df['active'].sum())
print('WorldWide Active')
print(active_total)

## SORTING DATA ##
confirmed_sorted_data = country_df.sort_values('confirmed', ascending=False)
confirmed_sorted_data = confirmed_sorted_data.drop(
    ['last_update', 'lat', 'long_', 'incident_rate', 'people_tested', 'uid', 'iso3', 'people_hospitalized'], axis=1)


confirmed_sorted_data_confirmed = confirmed_sorted_data.sort_values('confirmed', ascending=False).head(10)
confirmed_sorted_data_deaths = confirmed_sorted_data.sort_values('deaths', ascending=False).head(10)
confirmed_sorted_data_recovered = confirmed_sorted_data.sort_values('recovered', ascending=False).head(10)
confirmed_sorted_data_active = confirmed_sorted_data.sort_values('active', ascending=False).head(10)
confirmed_sorted_data_mortality = confirmed_sorted_data.sort_values('mortality_rate', ascending=False).head(10)

# fig = px.scatter(confirmed_sorted_data.head(20),
#                  x='country',
#                  y='confirmed',
#                  log_x=False,
#                  hover_name='country',
#                  hover_data=['country', 'confirmed'],
#                  color='country')
# fig.show()

## DASH ##
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(className="app-header", children=[
    html.Div('COVID-19 Data Dashboard', className="app-header--title"),
    html.Div('Total WorldWide Cases - ' + str(confirmed_total) + '', className="app-header"),
    html.Div('Total WorldWide Deaths - ' + str(deaths_total) + '', className="app-header"),
    html.Div('Total WorldWide Recovered - ' + str(recovered_total) + '', className="app-header"),
    html.Div('Total WorldWide Active - ' + str(active_total) + '', className="app-header"),

    html.Div(dcc.Graph(figure=px.scatter(confirmed_sorted_data_confirmed,
                                         title='Confirmed Cases By Country: -',
                                         x='country',
                                         y='confirmed',
                                         size='confirmed',
                                         color='country',
                                         hover_name='country',
                                         size_max=60))),

    html.Div(dcc.Graph(figure=px.scatter(confirmed_sorted_data_deaths,
                                         title='Deaths By Country: -',
                                         size='deaths',
                                         x='country',
                                         y='deaths',
                                         color='country',
                                         hover_name='country',
                                         size_max=60))),
    html.Div(dcc.Graph(figure=px.bar(confirmed_sorted_data_deaths,
                                     x='country',
                                     y= 'deaths',
                                     color= 'country',
                                     hover_name='country',
                                     ))),

    html.Div(dcc.Graph(figure=px.scatter(confirmed_sorted_data_recovered,
                                         title='Recovered Cases By Country: -',
                                         size='recovered',
                                         x='country',
                                         y='recovered',
                                         color='country',
                                         hover_name='country',
                                         size_max=60))),
    html.Div(dcc.Graph(figure=px.bar(confirmed_sorted_data_recovered,
                                     x= 'country',
                                     y= 'recovered',
                                     color='country'))),

    html.Div(dcc.Graph(figure=px.scatter(confirmed_sorted_data_active,
                                         title='Active Cases By Country: -',
                                         size='active',
                                         x='country',
                                         y = 'active',
                                         color='country',
                                         hover_name='country',
                                         size_max=60))),
    html.Div(dcc.Graph(figure=px.bar(confirmed_sorted_data_mortality,
                                     title='Moratility Rate By Country: -',
                                     x='country',
                                     y='mortality_rate',
                                     color='country',
                                     )))
]

                      )

if __name__ == '__main__':
    app.run_server(debug=True)
