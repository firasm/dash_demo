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

def make_plot(xval = 'Displacement'):
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

    typeDict = {'Displacement':'quantitative',
                'Cylinders':'quantitative',
                'Miles_per_Gallon':'quantitative'
    }

    # Create a plot from the cars dataset

    chart = alt.Chart(vega_datasets.data.cars.url).mark_point(size=90).encode(
                alt.X(xval,type=typeDict[xval], title=xval),
                alt.Y('Horsepower:Q', title = 'Horsepower (h.p.)'),
                tooltip = [{"type":typeDict[xval], "field":xval},
                            'Horsepower:Q',]
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

    ### Add Tabs to the top of the page
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Lecture 1', value='tab-1'),
        dcc.Tab(label='Lecture 2', value='tab-2'),
        dcc.Tab(label='Lecture 3', value='tab-3'), 
        dcc.Tab(label='Lecture 4', value='tab-4'), 
    ]),    

    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('This is my first dashboard'),
    html.H2('This is a subtitle'),

    html.H3('Here is an image'),
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
            width='10%'),

    html.H3('Here is our first plot:'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='500',
        width='1000',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),

    dcc.Markdown('''
    ### Dash and Markdown
                '''),

    ## these two components are related to dropdown
    # Let's comment out the demo-dropdown and dd-output to de-clutter our app a bit

    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC',
        style=dict(width='45%',
              verticalAlign="middle"
              )
        ),
        html.Div(id='dd-output'),
        
        # Just to add some space
        html.Iframe(height='50', width='10',style={'border-width': '0'}),

        html.H3('Dropdown to control Altair Chart'),

        dcc.Dropdown(
        id='dd-chart',
        options=[
            {'label': 'Miles_per_Gallon', 'value': 'Miles_per_Gallon'},
            {'label': 'Cylinders', 'value': 'Cylinders'},
            {'label': 'Displacement', 'value': 'Displacement'}
        ],
        value='Displacement',
        style=dict(width='45%',
              verticalAlign="middle"
              )
        ),
        # Just to add some space
        html.Iframe(height='200', width='10',style={'border-width': '0'})
])

# This first callback inserts raw text into an html.Div with id 'dd-output'
#       We normally omit the 'children' property as it is always the first property but this
#       just tells Dash to show the text. Every dash component has a 'children' property
# Note that the input argument needs to be provided as a list
# update_output is simply the function that runs when `demo-dropdown` is changed
# Let's comment out this to de-clutter our app once we know how it works
@app.callback(
    dash.dependencies.Output('dd-output', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return '\n \n You have selected {}\n \n'.format(value)

# This second callback tells Dash the output is the `plot` IFrame; srcDoc is a 
# special property that takes in RAW html as an input and renders it
# As input we take in the values from second dropdown we created (dd-chart) 
# then we run update_plot
@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value')])
def update_plot(xaxis_column_name):

    updated_plot = make_plot(xaxis_column_name).to_html()

    return updated_plot

if __name__ == '__main__':
    app.run_server(debug=True)
