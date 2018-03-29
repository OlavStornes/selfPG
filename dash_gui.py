import main 
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from loremipsum import get_sentences


app = dash.Dash()
server = app.server
app.scripts.config.serve_locally = True

app.layout = html.Div([
    dcc.Interval(id='game_update', interval=1000, n_intervals=0),
    dcc.Tabs(
        tabs=[
            {'label': 'Overview', 'value': 1},
            {'label': 'Main map', 'value': 2},
            {'label': 'Party view', 'value': 3},
            {'label': 'Towns', 'value': 4},
            {'label': 'Admin', 'value': 5}
            ],
        value=2,
        id='tab_id',
    ),
    html.Div(id='tab-output'),
    html.Div(id='hidden-div', hidden= True)
], style={
    'width': '80%',
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto'
})

unitlist = ["unit 1", "unit 2", "unit 3"]


@app.callback(Output('tab-output', 'children'), [Input('tab_id', 'value')])
def display_content(value):
    if value == 1:
        # OVERWIEW
        optionlist = []
        for item in unitlist:
            optionlist.append({"label":item , "value": item})


        return dcc.RadioItems(
        options=optionlist,
        labelStyle={'display': 'inline-block'}
        )

    elif value == 2:
        # MAIN MAP
        return 2


@app.callback(Output('hidden-div', 'children'),[Input('game_update', 'n_intervals')])
def game_tick(interval):
    print("updating")
    #app.game.test_tick()

if __name__ == '__main__':
    #app.game = main.Game()
    app.run_server(debug=True,port=8050, host='0.0.0.0')