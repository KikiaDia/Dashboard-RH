import plotly.express as px
import pandas as pd

def total_kpi_fig(df, chart_type="line"):
    df_total = df.groupby(["Mois", "KPI"])["Valeur"].sum().reset_index()
    mois_order = ["juillet", "août", "septembre"]
    df_total["Mois"] = pd.Categorical(df_total["Mois"].str.lower(), categories=mois_order, ordered=True)
    df_total = df_total.sort_values("Mois")

    if chart_type == "bar":
        return px.bar(df_total, x="Mois", y="Valeur", color="KPI", barmode="group", text_auto=True,
                      title="📊 Évolution globale des KPI pour l'entreprise sur le trimestre")
    else:
        return px.line(df_total, x="Mois", y="Valeur", color="KPI", markers=True,
                       title="📈 Évolution globale des KPI pour l'entreprise sur le trimestre")


def trend_kpi_fig(df, indicateur, chart_type="bar"):
    df_plot = df[df["KPI"] == indicateur].copy()
    mois_order = ["juillet", "août", "septembre"]
    df_plot["Mois"] = pd.Categorical(df_plot["Mois"].str.lower(), categories=mois_order)
    df_grouped = df_plot.groupby(["Mois", "Recruteur"])["Valeur"].sum().reset_index()

    if chart_type == "bar":
        return px.bar(df_grouped, x="Mois", y="Valeur", color="Recruteur", barmode="group",
                      title=f"📊 Évolution sur le trimestre du {indicateur} pour chaque recruteur", text_auto=True)
    else:
        return px.line(df_grouped, x="Mois", y="Valeur", color="Recruteur", markers=True,
                       title=f"📈 Évolution sur le trimestre du {indicateur} pour chaque recruteur")


def pie_kpi_fig(df):
    df_ent = df[df["KPI"].isin([
        "Nb d'entretiens candidats Salariés",
        "Nb d'entretiens candidats Sous-Traitants"
    ])].groupby("KPI")["Valeur"].sum().reset_index()

    if df_ent.empty:
        return px.pie(values=[1], names=["Pas de données"], title="Aucune donnée disponible")

    return px.pie(df_ent, values="Valeur", names="KPI",
                  title="🔄 Répartition des entretiens (Salariés vs Sous-traitants)",
                  hole=0.3)

