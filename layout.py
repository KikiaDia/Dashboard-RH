from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

def create_layout(df_all):
    return dbc.Container([

        dcc.Markdown("## 📊 Dashboard Reporting RH - 3e trimestre 2024", 
                     style={"textAlign": "center", "marginBottom": "30px"}),

        html.Hr(),

        dcc.Markdown("### KPIs sur le 3e Trimestre 2024 de l'entreprise",
                     style={"textAlign": "center", "marginBottom": "20px"}),

        dash_table.DataTable(
            id="summary-table",
            columns=[{"name":"Indicateur","id":"Indicateur"},
                     {"name":"Valeur","id":"Valeur"}],
            data=[],
            style_cell={"textAlign":"center"},
            style_header={"fontWeight":"bold","backgroundColor":"#f0f0f0"},
            style_table={"width":"60%", "margin": "0 auto" },
        ),

        html.Hr(),
        dcc.Markdown("### 📊 Évolution globale des KPI pour l'entreprise"),

        dcc.RadioItems(
            id="total-kpi-chart-type",
            options=[
                {"label": "📈 Courbe", "value": "line"},
                {"label": "📊 Histogramme", "value": "bar"}
            ],
            value="line",
            inline=True
        ),

        dcc.Graph(id="total-kpi-trimestre"),

        html.Hr(),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id="kpi-picker",
                    options=[{"label": k, "value": k} for k in df_all["KPI"].unique()],
                    value="Nb de candidats contactés",
                    clearable=False
                )
            ], width=6),
            dbc.Col([
                dcc.RadioItems(
                    id="chart-type",
                    options=[
                        {"label": "📊 Histogramme", "value": "bar"},
                        {"label": "📈 Courbe", "value": "line"}
                    ],
                    value="bar",
                    inline=True
                )
            ], width=6)
        ]),

        dcc.Graph(id="trend-chart"),

        html.Hr(),
        dcc.Graph(id="pie-chart"),

        dcc.Markdown("#### Analyse dynamique"),
        dcc.Dropdown(
            id="analyse-indicateur",
            options=[{"label": kpi, "value": kpi} for kpi in df_all["KPI"].unique()],
            value=df_all["KPI"].unique()[0],
            clearable=False,
            style={"Width": "6",}
        ),
        html.Div(id="analyse-texte", style={"maxWidth": "80%", }),

        # Chat widget flottant
        html.Div(
            [
                html.Button("", id="open-chat-btn", n_clicks=0, style={
                    "position": "fixed",
                    "bottom": "20px",
                    "right": "20px",
                    "width": "60px",
                    "height": "60px",
                    "border-radius": "50%",
                    "background-image": "url('assets/bot.jpg')",
                    "background-size": "cover",
                    "border": "none",
                    "box-shadow": "0px 4px 8px rgba(0,0,0,0.2)",
                    "cursor": "pointer",
                    "zIndex": "1000"
                }),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6("🤖 ReportingBot", style={"margin":"0"}),
                                html.Button("✖", id="close-chat-btn", n_clicks=0,
                                            style={"float":"right","border":"none","background":"transparent","fontSize":"18px","cursor":"pointer"})
                            ], style={"display":"flex","justifyContent":"space-between","alignItems":"center",
                                      "padding":"10px","backgroundColor":"#007bff","color":"white",
                                      "borderTopLeftRadius":"10px","borderTopRightRadius":"10px"}
                        ),
                        dbc.Textarea(id="chat-input", placeholder="Posez votre question ici...", style={"width":"100%","height":"60px","marginTop":"10px"}),
                        dbc.Button("Envoyer", id="chat-send-btn", color="primary", style={"width":"100%", "marginTop":"5px"}),
                        dcc.Loading(
                            dcc.Markdown(id="chat-response", style={"whiteSpace":"pre-line","marginTop":"10px",
                                                                   "maxHeight":"300px","overflowY":"auto"}),
                            type="circle"
                        )
                    ],
                    id="chat-widget",
                    style={
                        "position":"fixed",
                        "bottom":"100px",
                        "right":"20px",
                        "width":"300px",
                        "backgroundColor":"white",
                        "border":"1px solid #ccc",
                        "borderRadius":"10px",
                        "boxShadow":"0px 4px 12px rgba(0,0,0,0.15)",
                        "padding":"10px",
                        "display":"none",
                        "zIndex":"1000"
                    }
                )
            ]
        ),
    ])
