from dash import Dash
import dash_bootstrap_components as dbc
from pyngrok import ngrok
from config import NGROK_AUTH_TOKEN
from data_loader import load_data
from layout import create_layout
import callbacks  # importe tous les callbacks

df_all = load_data("/content/App/data/Data Reporting KPI RH Q32024.xlsx")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = create_layout(df_all)

# Enregistrement des callbacks avec le DataFrame
callbacks.register_callbacks(app, df_all)

ngrok.set_auth_token(NGROK_AUTH_TOKEN)
public_url = ngrok.connect(8050)
print("🌍 App accessible ici :", public_url)

if __name__ == "__main__":
    app.run(port=8050)

