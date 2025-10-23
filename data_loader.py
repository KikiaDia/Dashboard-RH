import pandas as pd

def load_data(fichier_excel, recruteurs= ["Inès", "Mariéme", "Pauline", "Samya"]):
    """
    Charge et prétraite les données KPI RH depuis un fichier Excel contenant un onglet par recruteur.

    Paramètres
    ----------
    fichier_excel : str
        Chemin vers le fichier Excel.
    recruteurs : list[str], optionnel
        Liste des noms d'onglets/recruteurs à traiter. Si None, tous les onglets du fichier seront utilisés.

    Retour
    ------
    pd.DataFrame
        DataFrame concaténé et prétraité avec les colonnes :
        ['KPI', 'Recruteur', 'Mois', 'Valeur']
    """
    
    # Charger le fichier Excel
    xls = pd.ExcelFile(fichier_excel)

    # Si aucun recruteur spécifié, prendre tous les onglets
    if recruteurs is None:
        recruteurs = xls.sheet_names

    frames = []

    for r in recruteurs:
        df = pd.read_excel(xls, sheet_name=r, skiprows=2)
        
        # Suppression des colonnes indésirables
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.loc[:, ~df.columns.str.contains('^Valeur')]

        # Garde les colonnes à partir de "KPI"
        if "KPI" in df.columns:
            df = df.iloc[:, df.columns.get_loc('KPI'):]
        else:
            continue  # Passe ce recruteur si la colonne KPI est absente

        # Supprime les lignes inutiles
        df = df[df['KPI'] != 'Nb de présentations aux clients']

        # Nettoyage du texte
        df["KPI"] = df["KPI"].astype(str).str.strip()

        # Corrige 'Juilet' → 'Juillet' si présent
        if 'Juilet' in df.columns:
            df.rename(columns={'Juilet': 'Juillet'}, inplace=True)

        # Ajout du nom du recruteur
        df["Recruteur"] = r

        # Transformation des mois en format long
        mois = [m for m in ["Juillet", "Août", "Septembre"] if m in df.columns]
        df_melt = df.melt(
            id_vars=["KPI", "Recruteur"],
            value_vars=mois,
            var_name="Mois",
            value_name="Valeur"
        )

        frames.append(df_melt)

    # Concaténation finale
    df_all = pd.concat(frames, ignore_index=True)
    return df_all
