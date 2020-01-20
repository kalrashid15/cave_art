## Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import datetime as dt

## Data
#reading data
input_folder = "./input/"

data = pd.read_csv(input_folder+'africa-economic-banking-and-systemic-crisis-data.zip', compression='zip')
df = data.copy()

#data selections and data transformations
#selecting data since 1910.
df = df[df['year']>=1910].reset_index(drop=True)

#coverting string categoical values in banking_crisis to numerics
replace_values = {'no_crisis' : 0, 'crisis' : 1}
df = df.replace({"banking_crisis": replace_values}) 

#creating additional variables
df['text'] = '<b>' + df['country'] + '</b>' + '<br>' + \
    'Systemic Crisis ' + df['systemic_crisis'].astype(str) +'<br>' + \
    'Currency Crises ' + df['currency_crises'].astype(str) + '<br>' + \
    'Banking Crises ' + df['banking_crisis'].astype(str) + '<br>' + \
    'Inflation Crises ' + df['inflation_crises'].astype(str)

#just adding this     
df['total_crises'] = df[['systemic_crisis', 'currency_crises', 'inflation_crises', 'banking_crisis']].sum(axis=1)
crises = ['systemic_crisis', 'currency_crises', 'inflation_crises', 'banking_crisis']
indicators= ['exch_usd', 'gdp_weighted_default', 'inflation_annual_cpi']

## Interactive Components

country_options = [dict(label=country, value=country) for country in df['country'].unique()]
crises_options = [dict(label=crisis.replace('_', ' '), value=crisis) for crisis in crises]
indicators_options = [dict(label=indicator.replace('_', ' '), value=indicator) for indicator in indicators]

## APP

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

home_page = html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Data Visualization Final Project - 2019/2020', className='row'),
                    html.Br(),
                    html.P("A visualization of the dataset named “Africa Economic, Banking and Systemic Crisis Data”."),
                    dcc.Markdown('''
                    Source: [Kaggle](https://www.kaggle.com/chirin/africa-economic-banking-and-systemic-crisis-data)
                    '''),
                    html.Br(),
                    dcc.Markdown(
                    '''
                    #### Github
                    Enjoy the code behind this app at [Github](https://github.com/kalrashid15/cave_arts).
                    '''),
                    html.Br(),
                    dcc.Markdown('''
                    #### Members
                    **Group 11**:
                    - **Kauser Al Rashid**, M20190543
                    - **Pedro Reis**, M20180428''')
                    ],className="row",style={'width': '98%', 'display': 'inline-block'})
                ]),

            html.Div([
                dcc.Markdown('''
                ## An Exploratory Dashboard for African Systemic and Other Crises.
                
                ### A description of main variables
                |     Variable     |   Description                                                |
                |-------------------------|:-----------------------------------------------------------------------|
                |  |
                | **Crises** |
                | systemic_crisis | Indicates a situation where a country faces large-scale economic Crisis. "0" means that no systemic crisis and "1" means that a systemic crisis occurred in the year. |
                | currency_crises | Indicates market perception that central bank does not have sufficient foreign exchange reserves to maintained country's fixed exchange rate. "0" means that no currency crisis occurred in the year and value greater than "0" indicates number of currency crisis occurred in that year. |
                | inflation_crises | Indicates hyper-inflation. "0" means that no inflation crisis occurred in the year and "1" means that an inflation crisis occurred in the year. |
                | banking_crisis | Indicates serious solvency or liquidity problems in the country's banks. "no_crisis" means that no banking crisis occurred in the year and "crisis" means that a banking crisis occurred in the year. |
                | . |
                | **Crisis Indicators** |
                | exch_usd | The exchange rate of the country compared to the US Dollars. |
                | domestic_debt_in_default | "0" means that no sovereign domestic debt default occurred in the year and "1" means that a sovereign domestic debt default occurred in the year. |
                | sovereign_external_debt_default | "0" means that no sovereign external debt default occurred in the year and "1" means that a sovereign external debt default occurred in the year. |
                | gdp_weighted_default | The total debt in default vis-a-vis the GDP. |
                | inflation_annual_cpi | The annual Consumer Price Index (CPI) Inflation rate. |
                | independence | "0" means "no independence" and "1" means "independence". |
                '''),
                ],
                className="row", style={'width': '80%', 'display': 'inline-block'}),
        ],className="row"),
        ])
                        
                        
dash_board = html.Div([
                html.Div([
                    html.Div([
                        html.H4('Country Choice', className='h4'),
                        dcc.Dropdown(
                            id='country_drop',
                            options=country_options,
                            value=['Egypt'],
                            multi=True
                        ),
                        html.Br(),
                        html.H4('Crises', className='h4'),
                        html.P(
                            'Select a particular crisis to inspect in the given country' 
                        ),
                        dcc.Dropdown(
                            id='crises_options',
                            options=crises_options,
                            value='systemic_crisis',
                        ),
                        html.Br(),
                        html.H4('Indicator Choice', className = 'h4'),
                        html.P(
                            'The list of predictors for financial crisis in a country' 
                        ),
                        dcc.Dropdown(
                            id='indicators_options',
                            options=indicators_options,
                            value=['gdp_weighted_default', 'inflation_annual_cpi', 'exch_usd'],
                            multi=True
                        ),
                        html.Br(),
                        html.H4('Year', className = 'h4'),
                        html.P(
                            'Scroll to select year to inspect all available data' 
                        ),
                        dcc.Slider(
                            id='year',
                            min= df['year'].min(),
                            max= df['year'].max(),
                            marks={str(i): '{}'.format(str(i)) for i in [1910, 1930, 1950, 1970, 
                                                                           1990, 2014]},
                            value=1959,
                            step=1
                        ),
            
                        html.Br(),
                        html.H4('Linear Log', className = 'h4'),
                        html.P(
                            'Selecting log transforms continous indicators variables to better measure' 
                        ),
                        dcc.RadioItems(
                            id='lin_log',
                            options=[dict(label='Linear', value=0), dict(label='log', value=1)],
                            value=0
                        ),
                    ], className='column1 pretty'),
            
                    html.Div([
                        html.H3([
                                html.Label('Crises in the selected Country(s) on the select year')
                                ], className='h3'),
                        html.Div([
                            html.Div([html.Label(id='crisis_1')], className='mini pretty'),
                            html.Div([html.Label(id='crisis_2')], className='mini pretty'),
                            html.Div([html.Label(id='crisis_3')], className='mini pretty'),
                            html.Div([html.Label(id='crisis_4')], className='mini pretty')
                        ], className='4 containers row'),
                        html.Div([dcc.Graph(id='choropleth')], className='bar_plot pretty'),
                    ], className='column2')
            
                ], className='row'),
            
                html.Div([
                    html.Div([dcc.Graph(id='bar_graph')], className='column3 pretty'),
                    html.Div([dcc.Graph(id='aggregate_graph')], className='column3 pretty'),
            
            
                ], className='row'),
                html.Div([
            
                    html.Div([dcc.Graph(id='aggregate_graph2')], className='column3 pretty'),
                    html.Div([dcc.Graph(id='heat_map')], className='column3 pretty')
            
                ], className='row'),
                #html.Div([
            
                html.Div([
                    html.Div([
                        html.H4('Country', className='h4'),
                        dcc.Dropdown(
                            id='country_drop2',
                            options=country_options,
                            value=['Angola'],
                            multi=True
                        ),
                        html.Br(),
                        html.H4('Between years', className='h4'),
                        dcc.RangeSlider(
                            id='year_range',
                            min= df['year'].min(),
                            max= df['year'].max(),
                            marks={str(i): '{}'.format(str(i)) for i in [1910, 1930, 1950, 1970, 
                                                                           1990, 2014]},
                            value=[1910, 1970],
                            step=1
                        ),
            
                        html.Br(),
                    ], className='column1 pretty'),#end of second input field
                                
                    #seocond heatmap div    
                    html.Div([dcc.Graph(id='heat_map2')], className='column3 pretty')
            
                ], className='row') #end of second heatmap div
            
    ])
      

    
## organising Tabs in the app     
app.layout = html.Div([
    html.H1('African Financial Crisis Over the Years', className='Title'),
    dcc.Tabs([
            dcc.Tab(label='Home', children=[
                home_page
            ]),
            dcc.Tab(label='Dashboard', children=[
                dash_board                      
            ]),
        ])
    ])

## Callbacks
@app.callback(
    [
         Output("choropleth", "figure"),   
         Output("bar_graph", "figure"),
         Output("aggregate_graph", "figure"),
         Output("aggregate_graph2", "figure"),
         Output("heat_map", "figure"),
         Output("heat_map2", "figure")

    ],
    [
        Input("year", "value"),
        Input("country_drop", "value"),
        Input("crises_options", "value"),
        Input("lin_log", "value"),
        Input("indicators_options", "value"),
        Input("country_drop2", "value"),
        Input("year_range", "value")
    ]
)

def plots(year, countries, crisis, scale, indicator, country2, year_range):
################################################################################################
        ## First Choropleth
    projection = 0 #equirectangular is preferred
    dff = df.loc[df['year'] == year]
    z = dff['total_crises']

    data_choropleth = dict(type='choropleth',
                           locations=dff['country'],
                           # There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='country names',
                           z=z,
                           text=dff['text'],
                           colorscale='Reds',
                           colorbar=dict(title='# of Crises',
                                         tickmode = 'array',
                                         tickvals = [0, 1, 2, 3, 4, 5]),
                           hovertemplate='Country: %{text} <br>' + 'Total Crises' ': %{z}',
                           )

    layout_choropleth = dict(geo=dict(scope='africa',  # default
                                      projection=dict(type=['equirectangular', 'orthographic'][projection]),
                                      landcolor='white',
                                      lakecolor='#1f77b4',
                                      showocean=True,  # default = False
                                      oceancolor='azure',
                                      bgcolor='#f9f9f9',
                                      ),

                             title=dict(text='Choropleth Map of Financial Crises by African countries on <b>' + str(year) +'</b>',
                                        x=.5  # Title relative position according to the xaxis, range (0,1)
                                        ),
                             paper_bgcolor='#f9f9f9'
                             )
######################################################################################################################
    ## second Bar Plot
    data_bar = []
    for country in countries:
        df_bar = df.loc[(df['country'] == country)]

        x_bar = df_bar['year']
        y_bar = df_bar[crisis]

        data_bar.append(dict(type='bar', x=x_bar, y=y_bar, name=country))

    layout_bar = dict(title=dict(text='Historical ' + crisis + ' <i> in </i>' + ','.join(countries)),
                  yaxis=dict(title=crisis),
                  paper_bgcolor='#f9f9f9')

    ## Third Scatter Plot
    df_loc = df.loc[df['country'].isin(countries)].groupby('year').mean().reset_index()
    data_agg = []
    
    for place in indicator:
        data_agg.append(dict(type='scatter',
                         x=df_loc['year'].unique(),
                         y=df_loc[place],
                         name=place.replace('_', ' ')
                         )
                    )

    layout_agg = dict(title=dict(text='Crisis Indicators for '+ ','.join(countries)),
                     yaxis=dict(title=['Indicators', 'Indicators (log scaled)'][scale],
                                type=['linear', 'log'][scale]),
                     xaxis=dict(title='Year', rangeslider=dict(visible=True)),
                     paper_bgcolor='#f9f9f9'
                     )


################## TODO: CHANGE GRAPH TO SCATTER (?)
    ## fourth Scatter Plot
    # df_loc2 = df.loc[df['country'].isin(countries)].groupby('year').mean().reset_index()

    d2_agg = []

    #hard coded these values
    cat_variables = ['domestic_debt_in_default', 'sovereign_external_debt_default', 'independence']

    for country in countries:
        df_loc2 = df.loc[df["country"] == country].copy()

        for place in cat_variables:

            # animals=['giraffes', 'orangutans', 'monkeys']

            # d2_agg.append(
            #     go.Bar(name=str(place), x=df_loc2.loc[df_loc2["country"]==country, 'year'], y=df_loc2.loc[df_loc2["country"]==country, place]),
            # )

            # # Change the bar mode
            # # fig.update_layout(barmode='stack')
            # # fig.show()

            # d2_agg.update_layout(barmode='stack')


            # d2_agg.append(dict(type='scatter',
            #                 x=df_loc2['year'].unique(),
            #                 y=df_loc2[place],
            #                 name=place.replace('_', ' ')
            #                 )
            #             )

            d2_agg.append(
                go.Bar(name=place, x=df_loc2['year'], y=df_loc2[place])
            )




            ####################
    # d2_agg_fig = go.Figure(data = d2_agg_data)

    # d2_agg_fig.update_layout(barmode='stack')
    
    layout_agg2 = dict(title=dict(text='Categorical Crisis Indicators for '+','.join(countries)),
                     yaxis=dict(title=['categoricals', 'Indicators (log scaled)'][0],
                                type=['linear', 'log'][0]),
                     xaxis=dict(title='Year', rangeslider=dict(visible=True)),
                     paper_bgcolor='#f9f9f9', barmode='stack', boxmode="group"
                     )

    ## fifth heatmap
    heat_df = df.loc[df['country'].isin(countries)].groupby('year').mean().reset_index()
    heat_df = heat_df.loc[heat_df[crisis]==1]
    
    y_data = heat_df[indicators]
    dates = heat_df['year']
    z=y_data.T
    fig_heat = go.Figure(data=go.Heatmap(
        z=z,
        x=dates,
        y=indicators,
        colorscale='Viridis'))

    layout_heatmap = dict(title=dict(text='Categorical Crisis Indicators for '+','.join(countries)),
                     yaxis=dict(title=['categoricals', 'Indicators (log scaled)'][0],
                                type=['linear', 'log'][0]),
                     xaxis=dict(title='Year', rangeslider=dict(visible=True)),
                     paper_bgcolor='#f9f9f9'
                     )
    fig_heat.update_layout(
            title= 'How ' +crisis +' correlates with crisis indicators in ' + ','.join(countries),
            xaxis_nticks=36)
    
    #####################################################################################################
    #sixth second heatmap
    heat_df2 = df.loc[df['country'].isin(country2)].groupby('year').mean().reset_index()
    
    heat_df2 = heat_df2[(year_range[0] <= heat_df2['year']) & (heat_df2['year'] <= year_range[1])]

    #dropping unncessary columns for heat_map
    heat_df2.drop(['case',  'year'], axis = 1, inplace = True)    
    
    heat_df2.loc[heat_df2["currency_crises"]==2, "currency_crises"] = 1

    corr = heat_df2.corr()
    #y_data = heat_df2
    fig_heat2 = go.Figure(data=go.Heatmap(
        z=corr,
        x = corr.columns,
        y = corr.columns,
        colorscale='Cividis'))
    
    layout_heatmap2 = dict(title=dict(text='How variables are correlated with each other in '+','.join(country2)),
                     yaxis=dict(title='variables'),
                     xaxis=dict(title='variables'),
                     paper_bgcolor='#f9f9f9'
                     )
    fig_heat2.update_layout(
            title= 'How variables are correlated with each other in ' + ','.join(country2))
    
    #'How variables are correlated with each other in ' + ','.join(country_list), xaxis_nticks=36
    #returning all the charts
    return go.Figure(data=data_choropleth, layout=layout_choropleth), \
           go.Figure(data=data_bar, layout=layout_bar),\
           go.Figure(data=data_agg, layout=layout_agg), \
           go.Figure(data=d2_agg, layout=layout_agg2), \
           go.Figure(data=fig_heat, layout=layout_heatmap), \
           go.Figure(data=fig_heat2, layout = layout_heatmap2)


@app.callback(
    [
        Output("crisis_1", "children"),
        Output("crisis_2", "children"),
        Output("crisis_3", "children"),
        Output("crisis_4", "children"),
    ],
    [
        Input("country_drop", "value"),
        Input("year", "value"),
    ]
)

def indicator(countries, year):
    df_loc = df.loc[df['country'].isin(countries)].groupby('year').sum().reset_index()
        
    value_1 = round(df_loc.loc[df_loc['year'] == year][crises[0]].values[0], 2)
    value_2 = round(df_loc.loc[df_loc['year'] == year][crises[1]].values[0], 2)
    value_3 = round(df_loc.loc[df_loc['year'] == year][crises[2]].values[0], 2)
    value_4 = round(df_loc.loc[df_loc['year'] == year][crises[3]].values[0], 2)

    return str(crises[0]).replace('_', ' ') + ': ' + str(value_1),\
           str(crises[1]).replace('_', ' ') + ': ' + str(value_2), \
           str(crises[2]).replace('_', ' ') + ': ' + str(value_3), \
           str(crises[3]).replace('_', ' ') + ': ' + str(value_4)

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)