# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import altair as alt
import vega_datasets

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash World!'),

    html.Div(children='''
        Dash is a web application framework for Python.
    '''),

    html.Iframe(
        id='plot',
        height='500',
        width='1000',
        sandbox='allow-scripts',
                
        alt.Chart(vega_datasets.data.cars.url).mark_point().encode(
            alt.X('Displacement:Q'),
            alt.Y('Horsepower:Q')
        ).properties(title='Horsepower vs. Displacement').to_html()
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)