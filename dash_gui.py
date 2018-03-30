import main 
import dash
from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from loremipsum import get_sentences
import db_api
import json


app = dash.Dash()
server = app.server
app.scripts.config.serve_locally = True

app.layout = html.Div([
    dcc.Interval(id='game_update', interval=5000, n_intervals=0),
    dcc.Tabs(
        tabs=[
            {'label': 'Overview', 'value': 1},
            {'label': 'Main map', 'value': 2},
            {'label': 'Party view', 'value': 3},
            {'label': 'Towns', 'value': 4},
            {'label': 'Admin', 'value': 5}
            ],
        value=1,
        id='tab_id',
    ),
    html.Div(id='tab-output'),
    html.Div(id='hidden-div')
], style={
    'width': '80%',
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto'
})

unitlist = ["unit 1", "unit 2", "unit 3"]


@app.callback(
    Output('tab-output', 'children'), 
    [Input('tab_id', 'value')], 
    [State('hidden-div', 'children')])
def display_content(tab_value, jsoninfo):
    json_out = json.loads(jsoninfo)
    if tab_value == 1:
        # OVERWIEW
        optionlist = []
        for number, party in enumerate(json_out):
            optionlist.append({"label":party["partyname"] , "tab_value": number})


        return dcc.RadioItems(
        options=optionlist,
        value= 1,
        labelStyle={'display': 'inline-block'}
        )

    elif tab_value == 2:
        # MAIN MAP
        return dcc.Graph(
            id='main-map',
            figure=go.Scattergeo(
                {
                'data': [
                    {
                        'lat': [1, 2, 3, 4],
                        'lon': [4, 1, 3, 5],
                        'text': ['a', 'b', 'c', 'd'],
                        'customdata': ['c.a', 'c.b', 'c.c', 'c.d'],
                        'name': 'Trace 1',
                        'mode': 'markers',
                        'marker': {'size': 12}
                    }
                ]
            }
            )
        )


@app.callback(Output('hidden-div', 'children'), 
    events = [Event('game_update', 'interval')])
def update_tick():
    db = db_api.Database()
    output = db.select_last_entry()
    return (str(output))

if __name__ == '__main__':
    #app.game = main.Game()
    app.run_server(debug=True,port=8050, host='0.0.0.0')