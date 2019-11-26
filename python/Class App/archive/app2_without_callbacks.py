import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'

## Magic happens here
def make_plot():

    # Create a plot of the Displacement and the Horsepower of the cars dataset
    # Add theme here
    
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
    chart = alt.Chart(vega_datasets.data.cars.url).mark_circle(size=90).encode(
                alt.X('Displacement:Q', title = 'Displacement (mm)'),
                alt.Y('Horsepower:Q', title = 'Horsepower (h.p.)'),
                tooltip = ['Horsepower:Q', 'Displacement:Q']
            ).properties(title='Horsepower vs. Displacement',
                        width=500, height=350).interactive()

    return chart
## Magic ends here


app.layout = html.Div([

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
        height='470',
        width='655',
        style={'border-width': '0'},

        ################ The magic happens here
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),
    dcc.Markdown('''
    ### Here is a markdown cell
    <!-- ![Image](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png)-->
    ```
    print('Hello World')
    ```
    '''),
    html.H3('This is a Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
    value='MTL', style=dict(width='55%')
        ),
    html.H3('This is a slider bar'),
    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) for i in range(10)},
        value=5
        )  
])

if __name__ == '__main__':
    app.run_server(debug=True)