## 1. Import packages

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

## 2. Setup app
app = dash.Dash(__name__)
server = app.server
app.title = 'Dash app with pure Altair HTML'

## 3. Data Analysis

...

## 4. Layout (dash components)

app.layout = html.Div([

    html.H1('This is a level 1 heading'),
    html.H2('This is a level 2 subheading'),
    dcc.Markdown('''

        Inside this, I can *write* normally! 

        ## Headings are also respected

        '''),

    html.H3('Here is an image'),
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
            width='10%'),
    html.H3('Here is our first plot:'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='450',
        width='625',
        style={'border-width': '0'},

        ################ The magic happens here
        srcDoc=open('chart.html').read()
        ################ 
        ),
])

if __name__ == '__main__':
    app.run_server(debug=True)











