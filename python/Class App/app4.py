import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets

### NEW IMPORT
# See Docs here: https://dash-bootstrap-components.opensource.faculty.ai
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app with pure Altair HTML'

def make_plot(xval = 'Displacement',
              yval = 'Horsepower'):
    # Don't forget to include imports

    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default

    typeDict = {'Displacement':['quantitative','Displacement (mm)'],
                'Cylinders':['ordinal', 'Cylinders (#)'],
                'Miles_per_Gallon':['quantitative', 'Fuel Efficiency (mpg)'],
                'Horsepower':['quantitative', 'Horsepower (hp)']
                }

    # Create a plot from the cars dataset

    brush = alt.selection(type='interval')

    chart = alt.Chart(vega_datasets.data.cars.url).mark_point(size=90).encode(
                alt.X(xval,type=typeDict[xval][0], title=typeDict[xval][1]),
                alt.Y(yval,type=typeDict[yval][0], title=typeDict[yval][1]),
                color=alt.condition(brush, 'Origin:N', alt.value('lightgray')),
                tooltip = [{"type":typeDict[xval][0], "field":xval},
                           # {"type":typeDict[yval][0], "field":yval}
                           ] 
            ).properties(title='{0} vs. {1}'.format(xval,yval),
                        width=500, height=350).add_selection(brush)

    bars = alt.Chart(vega_datasets.data.cars.url).mark_bar().encode(
                     y='Origin:N',
                     color='Origin:N',
                     x='count(Origin):Q'
    ).transform_filter(brush)

    return (chart & bars)

jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
                      width='100px'),
                html.H1("Cars! Cars! Explore Cars!", className="display-3"),
                html.P(
                    "Add a description of the dashboard",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)

logo = dbc.Row(dbc.Col(html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
                      width='15%'), width=4))

content = dbc.Container([
    dbc.Row(
                [dbc.Col(
                    html.Iframe(
                        sandbox='allow-scripts',
                        id='plot',
                        height='560',
                        width='700',
                        style={'border-width': '0'},
                        ################ The magic happens here
                        srcDoc=make_plot().to_html()
                        ################ The magic happens here
                        ),width='6'),
                    dbc.Col(
                        dcc.Dropdown(
                            id='dd-chart-x',
                            options=[
                                {'label': 'Fuel Efficiency', 'value': 'Miles_per_Gallon'},
                                {'label': 'Cylinders', 'value': 'Cylinders'},
                                {'label': 'Displacement', 'value': 'Displacement'},
                                {'label': 'Horsepower', 'value': 'Horsepower'}
                            ],
                            value='Horsepower',
                            # style=dict(width='45%',
                            #         verticalAlign="middle")
                            ), width=2
                            ),
                    dbc.Col(        
                        dcc.Dropdown(
                        id='dd-chart-y',
                        options=[
                            {'label': 'Fuel Efficiency', 'value': 'Miles_per_Gallon'},
                            {'label': 'Cylinders', 'value': 'Cylinders'},
                            {'label': 'Displacement', 'value': 'Displacement'},
                            {'label': 'Horsepower', 'value': 'Horsepower'}
                        ],
                        value='Displacement'
                        ), width=2
                    )
                ]
            )
    ]
)

footer = dbc.Container([dbc.Row(dbc.Col(html.P('This Dash app was made collaboratively by the DSCI 532 class in 2019/20!'))),
         ])

app.layout = html.Div([jumbotron,
                       content,
                       footer])

@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart-x', 'value'),
     dash.dependencies.Input('dd-chart-y', 'value')])
def update_plot(xaxis_column_name,
                yaxis_column_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_plot(xaxis_column_name,
                             yaxis_column_name).to_html()
    return updated_plot

if __name__ == '__main__':
    app.run_server(debug=True)
