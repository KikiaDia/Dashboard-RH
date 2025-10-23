from dash import Input, Output, State
# from main import app 
from visualizations import total_kpi_fig, trend_kpi_fig, pie_kpi_fig
from config import setup_tracing, llm
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dash import html
from data_loader import load_data
import dash

# df_all = load_data("/content/App/data/Data Reporting KPI RH Q32024.xlsx")

def register_callbacks(app, df_all):
    # Graphiques KPI
    @app.callback(
        Output("total-kpi-trimestre", "figure"),
        Input("total-kpi-chart-type", "value")
    )
    def update_total_kpi(chart_type):
        return total_kpi_fig(df_all, chart_type)


    @app.callback(
        Output("trend-chart", "figure"),
        Input("kpi-picker", "value"),
        Input("chart-type", "value")
    )
    def update_trend_chart(indicateur, chart_type):
        return trend_kpi_fig(df_all, indicateur, chart_type)


    @app.callback(
        Output("pie-chart", "figure"),
        Input("kpi-picker", "value")
    )
    def update_pie_chart(_):
        return pie_kpi_fig(df_all)


    # Tableau récapitulatif
    @app.callback(
        Output("summary-table","data"),
        Input("summary-table","id")
    )
    def update_summary(_):
        total_contactes = df_all[df_all["KPI"] == "Nb de candidats contactés"]["Valeur"].sum()
        total_entretiens_salaries = df_all[df_all["KPI"] == "Nb d'entretiens candidats Salariés"]["Valeur"].sum()
        total_entretiens_soustraitants = df_all[df_all["KPI"] == "Nb d'entretiens candidats Sous-Traitants"]["Valeur"].sum()
        total_recrutements = df_all[df_all["KPI"].isin(["Nb de candidats recrutés Salariés", "Nb de candidats intégrés Sous Traitants"])]["Valeur"].sum()

        contactes_par_recruteur = df_all[df_all["KPI"] == "Nb de candidats contactés"].groupby("Recruteur")["Valeur"].sum()
        recrutements_par_recruteur = df_all[df_all["KPI"].isin(["Nb de candidats recrutés Salariés", "Nb de candidats intégrés Sous Traitants"])].groupby("Recruteur")["Valeur"].sum()

        recruteur_max_contactes = contactes_par_recruteur.idxmax()
        max_contactes = contactes_par_recruteur.max()
        recruteur_max_recrutements = recrutements_par_recruteur.idxmax()
        max_recrutements = recrutements_par_recruteur.max()

        df_summary = [
            {"Indicateur": "👥 Total candidats contactés", "Valeur": total_contactes},
            {"Indicateur": "🧑‍💼 Total entretiens salariés", "Valeur": total_entretiens_salaries},
            {"Indicateur": "🤝 Total entretiens sous-traitants", "Valeur": total_entretiens_soustraitants},
            {"Indicateur": "✅ Total recrutements aboutis", "Valeur": total_recrutements},
            {"Indicateur": f"🏅 RH avec le plus de candidats contactés : {recruteur_max_contactes}", "Valeur": max_contactes},
            {"Indicateur": f"🏆 RH avec le plus de recrutements : {recruteur_max_recrutements}", "Valeur": max_recrutements}
        ]
        return df_summary


    # Analyse dynamique
    @app.callback(
        Output("analyse-texte", "children"),
        Input("analyse-indicateur", "value")
    )
    def update_analyse(indicateur):
        df_plot = df_all[df_all["KPI"] == indicateur].copy()
        if df_plot.empty:
            return "Aucune donnée pour cet indicateur."

        grouped_month = df_plot.groupby("Mois")["Valeur"].sum().reset_index()
        mois_max = grouped_month.loc[grouped_month["Valeur"].idxmax()]
        mois_min = grouped_month.loc[grouped_month["Valeur"].idxmin()]
        grouped_recruteur = df_plot.groupby("Recruteur")["Valeur"].sum().reset_index()
        recruteur_max = grouped_recruteur.loc[grouped_recruteur["Valeur"].idxmax()]

        return [
            html.P(f"📈 Le mois le plus actif a été {mois_max['Mois']}, avec un total de {mois_max['Valeur']} {indicateur.lower()}."),
            html.P(f"📉 Le mois le plus faible a été {mois_min['Mois']}, avec seulement {mois_min['Valeur']} {indicateur.lower()}."),
            html.P(f"🏆 Le recruteur le plus actif sur la période est {recruteur_max['Recruteur']}, avec {recruteur_max['Valeur']} {indicateur.lower()} au total.")
        ]


    # Chatbot
    @app.callback(
    Output("chat-widget", "style"),
    Input("open-chat-btn", "n_clicks"),
    Input("close-chat-btn", "n_clicks"),
    State("chat-widget", "style"),
    )
    def toggle_chat(open_clicks, close_clicks, current_style):
        if current_style is None:
            # style par défaut si jamais il est None
            current_style = {
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

        ctx = dash.callback_context
        if not ctx.triggered:
            return current_style
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "open-chat-btn":
            current_style["display"] = "block"
        elif button_id == "close-chat-btn":
            current_style["display"] = "none"

        return current_style



    @app.callback(
        Output("chat-response", "children"),
        Input("chat-send-btn", "n_clicks"),
        State("chat-input", "value"),
        prevent_initial_call=True
    )
    def ask_bot(n_clicks, question):
        tracer = setup_tracing()
        if not question:
            return "❌ Veuillez poser une question."
        try:
            with tracer.start_as_current_span("OpenAI-Trace") as span:
                span.set_attribute("langfuse.user.id", "user-2601")
                span.set_attribute("langfuse.session.id", "887354487")
                agent = create_pandas_dataframe_agent(
                    llm=llm,
                    df=df_all,
                    max_iterations=3,
                    verbose=True,
                    agent_type="tool-calling",
                    handle_parsing_errors=True,
                    allow_dangerous_code=True
                )
                response = agent.invoke(question)
                answer_text = str(response.get("output", "❌ Pas de réponse du bot."))
                span.set_attribute("output.value", answer_text)
        except Exception as e:
            answer_text = f"❌ Une erreur est survenue : {e}"

        return answer_text
