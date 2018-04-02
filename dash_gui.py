import main
import dash
from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
#from loremipsum import get_sentences
import db_api
import json


app = dash.Dash()
server = app.server
app.scripts.config.serve_locally = True

app.layout = html.Div([
    dcc.Interval(id='game_update', interval=1500, n_intervals=0),
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


@app.callback(
    Output('tab-output', 'children'),
    [Input('tab_id', 'value')],
    [State('hidden-div', 'children')],
    events=[Event('game_update', 'interval')])
def display_content(tab_value, jsoninfo):
    parties_list = json.loads(jsoninfo)

    if tab_value == 1:
        # OVERWIEW
        return html.Table(
        # Header
        [1, 2, 3, 4, 5] +

        # Body
        [1, 2, 3]
    )
            


    elif tab_value == 2:
        # MAIN MAP

        def get_mappos(grade):
            poslist = []
            for index, pos in enumerate(parties_list):
                poslist.append(parties_list[index]["pos"][grade])
            return poslist

        def get_mapname():
            namelist = []
            for index, party in enumerate(parties_list):
                namelist.append(parties_list[index]["partyname"])
            return namelist

        return dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scattergeo(
                        lat=get_mappos("x"),
                        lon=get_mappos("y"),
                        text=get_mapname(),
                        marker=go.Marker(
                            color='rgb(200, 118, 255)'
                        )
                    )
                ],
                layout={
                    "width": 1000,
                    "geo": {
                        "showframe": True,
                        "showcoastlines": False,
                        "bgcolor": 0x000FF,
                        "lonaxis": {
                            "showgrid": True
                        },
                        "lataxis": {
                            "showgrid": True
                        }

                    }
                }

            ),
            id='main-map'
            #style={'width': 700}
        )

    elif tab_value == 3:
        optionlist = []
        for number, party in enumerate(parties_list):
            optionlist.append(
                {"label": party["partyname"], "tab_value": number})

        return dcc.RadioItems(
            options=optionlist,
            labelStyle={'display': 'inline-block'}
        )

@app.callback(Output('hidden-div', 'children'),
    events=[Event('game_update', 'interval')])
def update_tick():
    db = db_api.Database()
    output = db.select_last_entry()
    return (str(output))


if __name__ == '__main__':
    #app.game = main.Game()
    app.run_server(debug=True, port=8050, host='0.0.0.0')
