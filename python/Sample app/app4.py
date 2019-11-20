# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import sqlalchemy
import altair as alt
import numpy as np
import pandas as pd
import io
from vega_datasets import data

# Don't need this with the cars dataset
alt.data_transformers.enable('default', max_rows=10000)

# Not using sql here
# conn = sqlalchemy.create_engine()

cars = data.cars()

app = dash.Dash(__name__, assets_folder='assets')

app.title = 'Test dash and altair'

app.layout = html.Div([
    html.Div([

    html.P([
        html.Label('x-axis'),
        dcc.Dropdown(
            id='x_axis',
            options=[{'label': i, 'value':i} for i in cars.columns],
            value='Acceleration'
        )
    ],
    style={'width': '250px', 'margin-right': 'auto',
           'margin-left': 'auto', 'text-align': 'center'}),
    html.P([
        html.Label('y-axis'),
        dcc.Dropdown(
            id='y_axis',
            options=[{'label': i, 'value':i} for i in cars.columns],
            value='Miles_per_Gallon'
        )
    ],
    style={'width': '250px', 'margin-right': 'auto',
           'margin-left': 'auto', 'text-align': 'center'})],
           className='input-wrapper'),

    html.Iframe(
        id='plot',
        height='500',
        width='1000',
        sandbox='allow-scripts',

        # This is where we will pass the html
        
        # Get rid of the border box
        style={'border-width': '0px'}
    )
])

@app.callback(
    dash.dependencies.Output('plot','srcDoc'),
    [dash.dependencies.Input('x_axis', 'value'),
     dash.dependencies.Input('y_axis', 'value')]
)
def pick_figure(x_axis, y_axis):
    
    brush = alt.selection_interval()

    points_cars = alt.Chart(cars).mark_point().encode(
        x=x_axis,
        y=y_axis,
    ).properties(
        width=450,
        height=350,
        selection=brush
    )

    bars = alt.Chart(cars).mark_bar().encode(
        x='Horsepower:Q',
        y='count()'
    ).transform_filter(
        brush.ref()
    ).properties(
        width=450,
        height=350)
    
    ### interactive plot
    np.random.seed(42)
    source = pd.DataFrame(np.cumsum(np.random.randn(100, 3), 0).round(2),
                        columns=['A', 'B', 'C'], index=pd.RangeIndex(100, name='x'))
    source = source.reset_index().melt('x', var_name='category', value_name='y')

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['x'], empty='none')

    # The basic line
    line = alt.Chart(source).mark_line(interpolate='basis').encode(
        x='x:Q',
        y='y:Q',
        color='category:N'
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(source).mark_point().encode(
        x='x:Q',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'y:Q', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(source).mark_rule(color='gray').encode(
        x='x:Q',
    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data
    chart = alt.layer(
                line, selectors, points, rules, text
            ).properties(
                width=600, height=300
            )

    ### interactive plot

    #chart = alt.hconcat(points_cars, bars)
    
    # Save html as a StringIO object in memory
    cars_html = io.StringIO()
    chart.save(cars_html, 'html')
        
    # Return the html from StringIO object
    return cars_html.getvalue()


if __name__ == '__main__':
    app.run_server(debug=True)