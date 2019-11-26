import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets')
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
                'Cylinders':['quantitative', 'Cylinders (#)'],
                'Miles_per_Gallon':['quantitative', 'Fuel Efficiency (mpg)'],
                'Horsepower':['quantitative', 'Horsepower (hp)']
                }

    # Create a plot from the cars dataset

    chart = alt.Chart(vega_datasets.data.cars.url).mark_point(size=90).encode(
                alt.X(xval,type=typeDict[xval][0], title=typeDict[xval][1]),
                alt.Y(yval,type=typeDict[yval][0], title=typeDict[yval][1]),
                tooltip = [{"type":typeDict[xval][0], "field":xval},
                           # {"type":typeDict[yval][0], "field":yval}
                           ] 
            ).properties(title='Horsepower vs. Displacement',
                        width=500, height=350).interactive()

    return chart

app.layout = html.Div([

    html.Div(
        className="app-header",
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),

    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('This is my first dashboard'),
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
            width='10%'),

    html.H3('Here is our first plot:'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='460',
        width='1000',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),
        html.H3('Dropdown to control Altair Chart'),

        dcc.Dropdown(
        id='dd-chart-x',
        options=[
            {'label': 'Fuel Efficiency', 'value': 'Miles_per_Gallon'},
            {'label': 'Cylinders', 'value': 'Cylinders'},
            {'label': 'Displacement', 'value': 'Displacement'},
            {'label': 'Horsepower', 'value': 'Horsepower'}
        ],
        value='Horsepower',
        style=dict(width='45%',
                   verticalAlign="middle")
        ),
        
        dcc.Dropdown(
        id='dd-chart-y',
        options=[
            {'label': 'Fuel Efficiency', 'value': 'Miles_per_Gallon'},
            {'label': 'Cylinders', 'value': 'Cylinders'},
            {'label': 'Displacement', 'value': 'Displacement'},
            {'label': 'Horsepower', 'value': 'Horsepower'}
        ],
        value='Displacement',
        style=dict(width='45%',
                   verticalAlign="middle")
        ),
        # Just to add some space
        html.Iframe(height='200', width='10',style={'border-width': '0'})
])

# This callback tells Dash the output is the `plot` IFrame; srcDoc is a 
# special property that takes in RAW html as an input and renders it
# As input we take in the values from second dropdown we created (dd-chart) 
# then we run update_plot
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
