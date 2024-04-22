import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Load the dataset
countries_data = pd.read_csv('country_wise_latest.csv')
total_confirmed = countries_data['Confirmed'].sum()
total_deaths = countries_data['Deaths'].sum()
total_recovered = countries_data['Recovered'].sum()
total_active = countries_data['Active'].sum()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("COVID-19 Country-wise Dashboard", className="text-center mt-4"),

    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Confirmed", className="card-title"),
                        html.H2(f"{total_confirmed:,}", className="text-primary font-weight-bold")
                    ])
                ], className="mb-4")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Deaths", className="card-title"),
                        html.H2(f"{total_deaths:,}", className="text-danger font-weight-bold")
                    ])
                ], className="mb-4")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Recovered", className="card-title"),
                        html.H2(f"{total_recovered:,}", className="text-success font-weight-bold")
                    ])
                ], className="mb-4")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Active", className="card-title"),
                        html.H2(f"{total_active:,}", className="text-warning font-weight-bold")
                    ])
                ], className="mb-4")
            ], width=3)
        ])
    ], className="container mb-4"),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country_selector',
                options=[{'label': country, 'value': country} for country in countries_data['Country/Region'].unique()],
                value='Worldwide',
                className="mb-4"
            ),
            dcc.Graph(id='country_graph')
        ], className="col-md-12")
    ], className="container mb-4"),

    html.Div([
        html.Div([
            dcc.Graph(id='new_cases_deaths')
        ], className="col-md-12")
    ], className="container mb-4"),

    html.Div([
        html.Div([
            dcc.Graph(id='histogram_week_change', className="mb-4"),
            dcc.Graph(id='histogram_week_increase')
        ], className="row")
    ], className="container")
])


@app.callback(
    Output('country_graph', 'figure'),
    [Input('country_selector', 'value')]
)
def update_country_graph(selected_country):
    if selected_country == 'Worldwide':
        filtered_data = countries_data
    else:
        filtered_data = countries_data[countries_data['Country/Region'] == selected_country]

    fig = px.bar(filtered_data, x='Country/Region', y=['Confirmed', 'Deaths', 'Recovered', 'Active'],
                 title=f"COVID-19 Cases in {selected_country}")
    return fig


@app.callback(
    Output('new_cases_deaths', 'figure'),
    [Input('country_selector', 'value')]
)
def update_new_cases_deaths(selected_country):
    if selected_country == 'Worldwide':
        filtered_data = countries_data
    else:
        filtered_data = countries_data[countries_data['Country/Region'] == selected_country]
    fig = px.bar(filtered_data, x='Country/Region', y=['New cases', 'New deaths'],
                 title="New Cases and Deaths per Country")
    return fig


@app.callback(
    Output('histogram_week_change', 'figure'),
    [Input('country_selector', 'value')]
)
def update_histogram_week_change(selected_country):
    filtered_data = countries_data if selected_country == 'Worldwide' else countries_data[
        countries_data['Country/Region'] == selected_country]
    fig = px.histogram(filtered_data, x="1 week change", nbins=30,
                       title="Histogram of 1 Week Change in Confirmed Cases")
    return fig


@app.callback(
    Output('histogram_week_increase', 'figure'),
    [Input('country_selector', 'value')]
)
def update_histogram_week_increase(selected_country):
    filtered_data = countries_data if selected_country == 'Worldwide' else countries_data[
        countries_data['Country/Region'] == selected_country]
    fig = px.histogram(filtered_data, x="1 week % increase", nbins=30,
                       title="Histogram of 1 Week Percentage Increase in Confirmed Cases")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
