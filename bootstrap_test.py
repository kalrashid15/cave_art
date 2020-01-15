import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

tab1_content = dbc.Card(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2("Grupo"),
                            html.P(
                                """\
                                    Pedro Pedro Pedro"""
                                    ),
                                    dbc.Button("View details", color="secondary"),
                        ],
                        
                        md=4,
                                        ),
                                        dbc.Col(
                                            [
                                                html.H2("Aprendizagem de Data Viz nos últimos dois dias"),
                                                dcc.Graph(
                                                    figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ],
    className="mt-3",
)
)






###############################################
tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
        dbc.Tab(
            "This tab's content is never seen", label="Tab 3", disabled=True
        ),
    ]
)



navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    brand="Demo",
    brand_href="#",
    sticky="top",
)



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([navbar, tabs])#body])

if __name__ == "__main__":
    app.run_server()
