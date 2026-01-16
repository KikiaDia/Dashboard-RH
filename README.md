# Dashboard RH – 3ᵉ Trimestre 2024

## Présentation du projet

Ce projet est un **tableau de bord interactif en Python** pour analyser les données RH du **3ᵉ trimestre 2024**.  
Il permet de consolider les KPI de recrutement, de visualiser les tendances mensuelles et d’interagir avec un **agent conversationnel** pour consulter facilement les données.

Technologies utilisées :  
- [Dash](https://dash.plotly.com/) pour l’interface web  
- [Plotly](https://plotly.com/python/) pour les graphiques  
- [pandas](https://pandas.pydata.org/) pour la manipulation des données  
- [Pyngrok](https://pyngrok.readthedocs.io/) (optionnel pour exposer le dashboard sur le web)  
- [LangChain + GPT-4](https://www.langchain.com/) pour l’agent conversationnel  

---

## Objectifs

1. **Consolidation des indicateurs du trimestre**  
   - Nombre total de candidats contactés par l’ensemble de l’équipe  
   - Nombre total d’entretiens réalisés (salariés / sous-traitants)  
   - Nombre total de recrutements aboutis  
   - Identifier le recruteur ayant contacté le plus de candidats et celui ayant réalisé le plus de recrutements  

2. **Visualisation des tendances mensuelles**  
   - Évolution du nombre de candidats contactés par mois pour chaque recruteur  
   - Graphiques interactifs avec titres, légendes et annotations  
   - Analyse rapide des tendances (mois le plus actif, comparaisons entre recruteurs)  

3. **Agent conversationnel (GPT-4)**  
   - Interroger les données RH en langage naturel  
   - Obtenir des réponses basées sur le DataFrame du trimestre  
   - Chat interactif avec ouverture/fermeture et affichage en bas à droite du dashboard  

---

## Structure du projet

```text
Dashboard-RH/
│── main.py                # Script principal pour lancer l’application
│── data/
│    └── Data Reporting KPI RH Q32024.xlsx
│── layout.py              # Structure et design du dashboard
│── data_loader.py         # Chargement et préparation des données
│── callbacks.py           # Définition des callbacks Dash et chatbot
│── config.py              # Token NGROK_AUTH_TOKEN (optionnel)
│── requirements.txt       # Dépendances Python

```

# Installation

## Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/Dashboard-RH.git
cd Dashboard-RH
```

# Utilisation
## Lancer le dashboard
```bash
python main.py
```

## Exemple de code minimal pour le chatbot
```python
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent

llm = ChatOpenAI(model_name="gpt-4")
agent = create_pandas_dataframe_agent(
    llm=llm,
    df=df_all,
    max_iterations=3,
    verbose=True,
    agent_type="tool-calling",
    allow_dangerous_code=True
)

question = "Qui a contacté le plus de candidats ?"
response = agent.invoke(question)
print(response.get("output"))
```
